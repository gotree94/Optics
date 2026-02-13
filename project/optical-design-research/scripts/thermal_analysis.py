"""
Thermal Analysis Module
열 해석 모듈

This module provides thermal analysis calculations for optical modules.
광학 모듈의 열 해석 계산을 제공합니다.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List
from dataclasses import dataclass


@dataclass
class MaterialProperties:
    """재료 물성 데이터 클래스"""
    name: str
    thermal_conductivity: float  # W/m·K
    density: float               # kg/m³
    specific_heat: float         # J/kg·K
    thermal_expansion: float     # 1/K
    
    def thermal_diffusivity(self) -> float:
        """열확산율 계산 (m²/s)"""
        return self.thermal_conductivity / (self.density * self.specific_heat)


# 일반적인 광학 재료 물성
MATERIAL_DATABASE = {
    "BK7": MaterialProperties(
        name="BK7 Glass",
        thermal_conductivity=1.114,
        density=2510,
        specific_heat=858,
        thermal_expansion=7.1e-6
    ),
    "Fused Silica": MaterialProperties(
        name="Fused Silica",
        thermal_conductivity=1.38,
        density=2203,
        specific_heat=703,
        thermal_expansion=0.55e-6
    ),
    "Aluminum": MaterialProperties(
        name="Aluminum 6061-T6",
        thermal_conductivity=167,
        density=2700,
        specific_heat=896,
        thermal_expansion=23.6e-6
    ),
    "Copper": MaterialProperties(
        name="Copper",
        thermal_conductivity=400,
        density=8960,
        specific_heat=385,
        thermal_expansion=16.5e-6
    ),
    "Invar": MaterialProperties(
        name="Invar",
        thermal_conductivity=10.7,
        density=8050,
        specific_heat=515,
        thermal_expansion=1.2e-6
    )
}


class ThermalAnalyzer:
    """열 해석 계산 클래스"""
    
    @staticmethod
    def conduction_1d(k: float, area: float, temp_diff: float, 
                      length: float) -> float:
        """
        1차원 정상 상태 열전도 계산 (Fourier's Law)
        
        Args:
            k: 열전도율 (W/m·K)
            area: 단면적 (m²)
            temp_diff: 온도차 (K)
            length: 길이 (m)
            
        Returns:
            열유속 (W)
        """
        return k * area * temp_diff / length
    
    @staticmethod
    def convection(h: float, area: float, temp_diff: float) -> float:
        """
        대류 열전달 계산 (Newton's Law of Cooling)
        
        Args:
            h: 대류 열전달계수 (W/m²·K)
            area: 표면적 (m²)
            temp_diff: 온도차 (K)
            
        Returns:
            열유속 (W)
        """
        return h * area * temp_diff
    
    @staticmethod
    def radiation(emissivity: float, area: float, 
                 temp_hot: float, temp_cold: float) -> float:
        """
        복사 열전달 계산 (Stefan-Boltzmann Law)
        
        Args:
            emissivity: 방사율
            area: 표면적 (m²)
            temp_hot: 고온 표면 온도 (K)
            temp_cold: 저온 주변 온도 (K)
            
        Returns:
            열유속 (W)
        """
        sigma = 5.67e-8  # Stefan-Boltzmann constant (W/m²·K⁴)
        return emissivity * sigma * area * (temp_hot**4 - temp_cold**4)
    
    @staticmethod
    def thermal_resistance_conduction(length: float, k: float, 
                                     area: float) -> float:
        """
        전도 열저항 계산
        
        Args:
            length: 길이 (m)
            k: 열전도율 (W/m·K)
            area: 단면적 (m²)
            
        Returns:
            열저항 (K/W)
        """
        return length / (k * area)
    
    @staticmethod
    def thermal_resistance_convection(h: float, area: float) -> float:
        """
        대류 열저항 계산
        
        Args:
            h: 대류 열전달계수 (W/m²·K)
            area: 표면적 (m²)
            
        Returns:
            열저항 (K/W)
        """
        return 1 / (h * area)


class PeltierModule:
    """펠티어 모듈 성능 계산 클래스"""
    
    def __init__(self, qmax: float, delta_tmax: float, imax: float, vmax: float):
        """
        Args:
            qmax: 최대 냉각 능력 (W) at ΔT=0
            delta_tmax: 최대 온도차 (K) at Q=0
            imax: 최대 전류 (A)
            vmax: 최대 전압 (V)
        """
        self.qmax = qmax
        self.delta_tmax = delta_tmax
        self.imax = imax
        self.vmax = vmax
    
    def cooling_power(self, delta_t: float, current: float) -> float:
        """
        냉각 능력 계산
        
        Args:
            delta_t: 온도차 (K)
            current: 전류 (A)
            
        Returns:
            냉각 능력 (W)
        """
        qc = self.qmax * (current / self.imax) - \
             self.delta_tmax * (current / self.imax)**2 * (delta_t / self.delta_tmax)
        return max(0, qc)
    
    def voltage(self, delta_t: float, current: float) -> float:
        """
        필요 전압 계산
        
        Args:
            delta_t: 온도차 (K)
            current: 전류 (A)
            
        Returns:
            전압 (V)
        """
        return self.vmax * (current / self.imax) * (1 + delta_t / self.delta_tmax)
    
    def cop(self, delta_t: float, current: float) -> float:
        """
        성능계수(COP) 계산
        
        Args:
            delta_t: 온도차 (K)
            current: 전류 (A)
            
        Returns:
            COP (무차원)
        """
        qc = self.cooling_power(delta_t, current)
        power = self.voltage(delta_t, current) * current
        return qc / power if power > 0 else 0


class HeatSinkDesigner:
    """히트싱크 설계 도구"""
    
    @staticmethod
    def natural_convection_h(temp_diff: float, length: float) -> float:
        """
        자연 대류 열전달계수 추정 (수직 평판)
        
        Args:
            temp_diff: 온도차 (K)
            length: 특성 길이 (m)
            
        Returns:
            열전달계수 (W/m²·K)
        """
        # 간단한 경험식 사용
        return 1.42 * (temp_diff / length)**0.25
    
    @staticmethod
    def forced_convection_h(velocity: float, length: float) -> float:
        """
        강제 대류 열전달계수 추정 (평판)
        
        Args:
            velocity: 유속 (m/s)
            length: 특성 길이 (m)
            
        Returns:
            열전달계수 (W/m²·K)
        """
        # 간단한 경험식 사용 (공기)
        return 10.45 - velocity + 10 * velocity**0.5
    
    @staticmethod
    def fin_efficiency(fin_height: float, fin_thickness: float,
                      k: float, h: float) -> float:
        """
        핀 효율 계산
        
        Args:
            fin_height: 핀 높이 (m)
            fin_thickness: 핀 두께 (m)
            k: 열전도율 (W/m·K)
            h: 열전달계수 (W/m²·K)
            
        Returns:
            핀 효율 (0~1)
        """
        m = np.sqrt(2 * h / (k * fin_thickness))
        ml = m * fin_height
        efficiency = np.tanh(ml) / ml
        return efficiency


def transient_temperature(initial_temp: float, ambient_temp: float,
                         thermal_mass: float, thermal_resistance: float,
                         time: np.ndarray, heat_input: float = 0) -> np.ndarray:
    """
    과도 상태 온도 응답 계산 (1차 시스템)
    
    Args:
        initial_temp: 초기 온도 (°C)
        ambient_temp: 주변 온도 (°C)
        thermal_mass: 열용량 (J/K)
        thermal_resistance: 열저항 (K/W)
        time: 시간 배열 (s)
        heat_input: 열입력 (W)
        
    Returns:
        온도 배열 (°C)
    """
    tau = thermal_mass * thermal_resistance
    steady_state_temp = ambient_temp + heat_input * thermal_resistance
    
    temp = steady_state_temp + (initial_temp - steady_state_temp) * np.exp(-time / tau)
    return temp


if __name__ == "__main__":
    # 예제: 펠티어 모듈 성능 분석
    print("=" * 60)
    print("Peltier Module Performance Analysis")
    print("=" * 60)
    
    # 일반적인 2단 펠티어 사양
    peltier = PeltierModule(qmax=25, delta_tmax=70, imax=4.0, vmax=15.4)
    
    # 작동 조건
    delta_t = 30  # K
    current = 3.0  # A
    
    qc = peltier.cooling_power(delta_t, current)
    voltage = peltier.voltage(delta_t, current)
    cop = peltier.cop(delta_t, current)
    
    print(f"온도차: {delta_t} K")
    print(f"전류: {current} A")
    print(f"냉각 능력: {qc:.2f} W")
    print(f"전압: {voltage:.2f} V")
    print(f"소비 전력: {voltage * current:.2f} W")
    print(f"COP: {cop:.3f}")
    
    # 예제: 과도 상태 온도 응답
    print("\n" + "=" * 60)
    print("Transient Temperature Response")
    print("=" * 60)
    
    # 광학 모듈 예제 (알루미늄 하우징)
    mass = 0.1  # kg
    cp = MATERIAL_DATABASE["Aluminum"].specific_heat  # J/kg·K
    thermal_mass = mass * cp
    thermal_resistance = 5.0  # K/W
    heat_input = 10  # W
    
    time = np.linspace(0, 600, 1000)  # 10분간
    temp = transient_temperature(25, 25, thermal_mass, thermal_resistance, 
                                time, heat_input)
    
    # 플롯
    plt.figure(figsize=(10, 6))
    plt.plot(time, temp, linewidth=2)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.title('Transient Temperature Response', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=temp[-1], color='r', linestyle='--', 
                label=f'Steady-state: {temp[-1]:.1f}°C')
    plt.legend()
    plt.tight_layout()
    
    # 결과 출력
    tau = thermal_mass * thermal_resistance
    print(f"열용량: {thermal_mass:.0f} J/K")
    print(f"열저항: {thermal_resistance:.1f} K/W")
    print(f"시정수: {tau:.1f} s")
    print(f"정상 상태 온도: {temp[-1]:.1f}°C")
    print(f"63.2% 도달 시간: {tau:.1f} s")
    
    plt.savefig('/home/claude/temp_transient.png', dpi=150)
    print(f"\n그래프 저장 완료: temp_transient.png")
