"""
Unit Tests for Optical Calculations
광학 계산 단위 테스트
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# 스크립트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from optical_calculations import (
    OpticalCalculator,
    ThermalOpticsCalculator,
    calculate_f_theta_distortion,
    calculate_spot_size
)


class TestOpticalCalculator:
    """광학 계산기 테스트"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.calc = OpticalCalculator()
    
    def test_thin_lens_focal_length(self):
        """얇은 렌즈 초점거리 계산 테스트"""
        # BK7 렌즈, 양볼록
        r1 = 50  # mm
        r2 = -50  # mm
        n = 1.5168  # BK7 @ 587.6nm
        
        f = self.calc.thin_lens_focal_length(r1, r2, n)
        
        # 예상 값: f ≈ 48.4 mm
        assert abs(f - 48.4) < 1.0, f"Expected ~48.4, got {f}"
    
    def test_f_number(self):
        """F-number 계산 테스트"""
        focal_length = 100  # mm
        aperture = 25  # mm
        
        f_num = self.calc.f_number(focal_length, aperture)
        
        assert f_num == 4.0, f"Expected 4.0, got {f_num}"
    
    def test_numerical_aperture(self):
        """개구수 계산 테스트"""
        n = 1.0  # 공기
        half_angle = 30  # degrees
        
        na = self.calc.numerical_aperture(n, half_angle)
        
        expected = 0.5  # sin(30°)
        assert abs(na - expected) < 0.01, f"Expected {expected}, got {na}"
    
    def test_rayleigh_resolution(self):
        """레이리 분해능 테스트"""
        wavelength = 0.55  # μm (green light)
        f_number = 2.8
        
        resolution = self.calc.rayleigh_resolution(wavelength, f_number)
        
        # 예상 값: ~1.88 μm
        assert 1.8 < resolution < 2.0, f"Expected ~1.88, got {resolution}"
    
    def test_beam_divergence(self):
        """빔 발산각 테스트"""
        wavelength = 1.064  # μm
        beam_diameter = 10  # mm
        
        divergence = self.calc.beam_divergence(wavelength, beam_diameter)
        
        # 발산각이 양수이고 합리적인 범위인지 확인
        assert 0 < divergence < 1, f"Divergence out of range: {divergence}"


class TestThermalOpticsCalculator:
    """열-광학 계산기 테스트"""
    
    def setup_method(self):
        self.calc = ThermalOpticsCalculator()
    
    def test_thermal_focal_shift(self):
        """열적 초점 이동 테스트"""
        focal_length = 100  # mm
        dn_dt = -1.0e-6  # BK7의 대략적인 값
        temp_change = 20  # K
        
        shift = self.calc.thermal_focal_shift(focal_length, dn_dt, temp_change)
        
        # 음수 값 (온도 증가 시 초점거리 감소)
        assert shift < 0, f"Expected negative shift, got {shift}"
    
    def test_thermal_expansion(self):
        """열팽창 테스트"""
        length = 100  # mm
        alpha = 23e-6  # Aluminum
        temp_change = 50  # K
        
        expansion = self.calc.thermal_expansion(length, alpha, temp_change)
        
        expected = 0.115  # mm
        assert abs(expansion - expected) < 0.01, f"Expected {expected}, got {expansion}"


class TestFThetaDistortion:
    """F-theta 왜곡 테스트"""
    
    def test_zero_distortion(self):
        """왜곡이 없는 경우"""
        focal_length = 160  # mm
        field_angle = 10  # degrees
        
        # 이상적인 상고
        ideal_height = focal_length * np.radians(field_angle)
        
        # 왜곡이 0이어야 함
        distortion = calculate_f_theta_distortion(focal_length, field_angle, ideal_height)
        
        assert abs(distortion) < 0.01, f"Expected ~0, got {distortion}"
    
    def test_positive_distortion(self):
        """양의 왜곡"""
        focal_length = 160
        field_angle = 10
        
        ideal_height = focal_length * np.radians(field_angle)
        actual_height = ideal_height * 1.02  # 2% 더 큼
        
        distortion = calculate_f_theta_distortion(focal_length, field_angle, actual_height)
        
        assert 1.9 < distortion < 2.1, f"Expected ~2%, got {distortion}%"


class TestSpotSize:
    """스팟 크기 계산 테스트"""
    
    def test_diffraction_limited_spot(self):
        """회절 한계 스팟"""
        wavelength = 1.064  # μm
        focal_length = 160  # mm
        beam_diameter = 10  # mm
        m_squared = 1.0
        
        spot_size = calculate_spot_size(wavelength, focal_length, beam_diameter, m_squared)
        
        # 대략 43 μm 예상
        assert 40 < spot_size < 50, f"Expected ~43 μm, got {spot_size}"
    
    def test_beam_quality_effect(self):
        """빔 품질의 영향"""
        wavelength = 1.064
        focal_length = 160
        beam_diameter = 10
        
        spot_m1 = calculate_spot_size(wavelength, focal_length, beam_diameter, 1.0)
        spot_m2 = calculate_spot_size(wavelength, focal_length, beam_diameter, 2.0)
        
        # M²=2일 때 스팟이 2배 커야 함
        assert abs(spot_m2 / spot_m1 - 2.0) < 0.01, "Spot size should double with M²=2"


# pytest 실행 시 사용할 픽스처
@pytest.fixture
def sample_lens_data():
    """샘플 렌즈 데이터"""
    return {
        'focal_length': 100,  # mm
        'f_number': 2.8,
        'wavelength': 0.55,  # μm
        'material': 'BK7'
    }


def test_with_fixture(sample_lens_data):
    """픽스처를 사용한 테스트 예제"""
    calc = OpticalCalculator()
    
    resolution = calc.rayleigh_resolution(
        sample_lens_data['wavelength'],
        sample_lens_data['f_number']
    )
    
    assert resolution > 0, "Resolution must be positive"


if __name__ == "__main__":
    # pytest를 프로그래밍 방식으로 실행
    pytest.main([__file__, "-v"])
