"""
Unit Tests for Thermal Analysis
열 해석 단위 테스트
"""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from thermal_analysis import (
    MaterialProperties,
    ThermalAnalyzer,
    PeltierModule,
    HeatSinkDesigner,
    MATERIAL_DATABASE
)


class TestMaterialProperties:
    """재료 물성 테스트"""
    
    def test_thermal_diffusivity_calculation(self):
        """열확산율 계산 테스트"""
        mat = MATERIAL_DATABASE["Copper"]
        
        diffusivity = mat.thermal_diffusivity()
        
        # 구리의 열확산율: ~1.16e-4 m²/s
        expected = mat.thermal_conductivity / (mat.density * mat.specific_heat)
        assert abs(diffusivity - expected) < 1e-10
    
    def test_material_database_completeness(self):
        """재료 데이터베이스 완전성 테스트"""
        required_materials = ["BK7", "Aluminum", "Copper"]
        
        for material in required_materials:
            assert material in MATERIAL_DATABASE, f"{material} not in database"
            mat = MATERIAL_DATABASE[material]
            assert mat.thermal_conductivity > 0
            assert mat.density > 0
            assert mat.specific_heat > 0


class TestThermalAnalyzer:
    """열 해석기 테스트"""
    
    def setup_method(self):
        self.analyzer = ThermalAnalyzer()
    
    def test_conduction_1d(self):
        """1차원 열전도 테스트"""
        k = 400  # W/m·K (Copper)
        area = 0.001  # m² (10mm x 10mm)
        temp_diff = 50  # K
        length = 0.1  # m (100mm)
        
        heat_flux = self.analyzer.conduction_1d(k, area, temp_diff, length)
        
        # Q = k * A * ΔT / L = 400 * 0.001 * 50 / 0.1 = 200 W
        expected = 200
        assert abs(heat_flux - expected) < 1, f"Expected {expected}, got {heat_flux}"
    
    def test_convection(self):
        """대류 열전달 테스트"""
        h = 10  # W/m²·K (natural convection)
        area = 0.01  # m²
        temp_diff = 30  # K
        
        heat_flux = self.analyzer.convection(h, area, temp_diff)
        
        # Q = h * A * ΔT = 10 * 0.01 * 30 = 3 W
        expected = 3
        assert abs(heat_flux - expected) < 0.1
    
    def test_thermal_resistance_series(self):
        """직렬 열저항 테스트"""
        # 두 재료가 직렬로 연결된 경우
        length1 = 0.01  # m
        k1 = 400  # W/m·K (Copper)
        length2 = 0.01  # m
        k2 = 167  # W/m·K (Aluminum)
        area = 0.001  # m²
        
        r1 = self.analyzer.thermal_resistance_conduction(length1, k1, area)
        r2 = self.analyzer.thermal_resistance_conduction(length2, k2, area)
        
        total_resistance = r1 + r2
        
        # 직렬 연결이므로 저항이 더해짐
        assert total_resistance > r1
        assert total_resistance > r2
        assert abs(total_resistance - (r1 + r2)) < 1e-10


class TestPeltierModule:
    """펠티어 모듈 테스트"""
    
    def setup_method(self):
        # 일반적인 2단 펠티어 사양
        self.peltier = PeltierModule(
            qmax=25,        # W
            delta_tmax=70,  # K
            imax=4.0,       # A
            vmax=15.4       # V
        )
    
    def test_max_cooling_at_zero_delta_t(self):
        """ΔT=0일 때 최대 냉각 능력"""
        qc = self.peltier.cooling_power(delta_t=0, current=self.peltier.imax)
        
        # ΔT=0, I=Imax일 때 Qmax에 근접해야 함
        assert qc > 0.9 * self.peltier.qmax, f"Expected ~{self.peltier.qmax}, got {qc}"
    
    def test_zero_cooling_at_max_delta_t(self):
        """최대 ΔT에서 냉각 능력"""
        qc = self.peltier.cooling_power(
            delta_t=self.peltier.delta_tmax,
            current=self.peltier.imax
        )
        
        # 최대 온도차에서는 냉각 능력이 거의 0
        assert qc < 1, f"Expected ~0, got {qc}"
    
    def test_cop_realistic_range(self):
        """COP가 현실적인 범위인지 확인"""
        delta_t = 30  # K
        current = 3.0  # A
        
        cop = self.peltier.cop(delta_t, current)
        
        # 펠티어의 COP는 일반적으로 0.3~1.5 범위
        assert 0.1 < cop < 2.0, f"COP out of realistic range: {cop}"
    
    def test_power_consumption_increases_with_current(self):
        """전류 증가 시 소비 전력 증가"""
        delta_t = 25
        
        power1 = self.peltier.voltage(delta_t, 2.0) * 2.0
        power2 = self.peltier.voltage(delta_t, 3.0) * 3.0
        
        assert power2 > power1, "Power should increase with current"


class TestHeatSinkDesigner:
    """히트싱크 설계 도구 테스트"""
    
    def setup_method(self):
        self.designer = HeatSinkDesigner()
    
    def test_natural_convection_h_positive(self):
        """자연 대류 열전달계수가 양수인지 확인"""
        temp_diff = 30  # K
        length = 0.1  # m
        
        h = self.designer.natural_convection_h(temp_diff, length)
        
        assert h > 0, "Heat transfer coefficient must be positive"
        # 일반적으로 5-25 W/m²·K 범위
        assert 1 < h < 50, f"h out of typical range: {h}"
    
    def test_forced_convection_higher_than_natural(self):
        """강제 대류가 자연 대류보다 높은 열전달계수"""
        length = 0.1
        velocity = 2.0  # m/s
        temp_diff = 30
        
        h_forced = self.designer.forced_convection_h(velocity, length)
        h_natural = self.designer.natural_convection_h(temp_diff, length)
        
        # 강제 대류가 더 효과적
        assert h_forced > h_natural, "Forced convection should be better"
    
    def test_fin_efficiency_range(self):
        """핀 효율이 0~1 범위인지 확인"""
        fin_height = 0.02  # m (20mm)
        fin_thickness = 0.001  # m (1mm)
        k = 167  # W/m·K (Aluminum)
        h = 10  # W/m²·K
        
        efficiency = self.designer.fin_efficiency(fin_height, fin_thickness, k, h)
        
        assert 0 < efficiency <= 1, f"Efficiency out of range: {efficiency}"
    
    def test_fin_efficiency_decreases_with_height(self):
        """핀 높이가 증가하면 효율 감소"""
        fin_thickness = 0.001
        k = 167
        h = 10
        
        eff_short = self.designer.fin_efficiency(0.01, fin_thickness, k, h)
        eff_tall = self.designer.fin_efficiency(0.04, fin_thickness, k, h)
        
        assert eff_short > eff_tall, "Shorter fins should be more efficient"


@pytest.fixture
def copper_material():
    """구리 재료 픽스처"""
    return MATERIAL_DATABASE["Copper"]


@pytest.fixture
def standard_peltier():
    """표준 펠티어 모듈 픽스처"""
    return PeltierModule(qmax=25, delta_tmax=70, imax=4.0, vmax=15.4)


def test_thermal_resistance_with_materials(copper_material):
    """재료 물성을 사용한 열저항 계산"""
    analyzer = ThermalAnalyzer()
    
    length = 0.05  # m
    area = 0.001  # m²
    
    r_thermal = analyzer.thermal_resistance_conduction(
        length,
        copper_material.thermal_conductivity,
        area
    )
    
    # 구리는 열전도율이 높으므로 열저항이 낮음
    assert r_thermal < 1, "Copper should have low thermal resistance"


def test_peltier_optimal_current(standard_peltier):
    """최적 작동 전류 찾기"""
    delta_t = 30  # K
    
    # 여러 전류에서 COP 계산
    currents = np.linspace(1, 4, 20)
    cops = [standard_peltier.cop(delta_t, i) for i in currents]
    
    # 최적 COP를 가지는 전류가 존재해야 함
    max_cop = max(cops)
    assert max_cop > 0, "Should have positive COP"
    
    # 최적 전류는 Imax보다 작아야 함
    optimal_current = currents[cops.index(max_cop)]
    assert optimal_current < standard_peltier.imax


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
