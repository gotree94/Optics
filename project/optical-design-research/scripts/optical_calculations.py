"""
Optical Calculations Module
광학 계산 모듈

This module provides common optical calculations for lens design and analysis.
렌즈 설계 및 분석을 위한 일반적인 광학 계산을 제공합니다.
"""

import numpy as np
from typing import Tuple, Optional


class OpticalCalculator:
    """광학 계산을 위한 유틸리티 클래스"""
    
    @staticmethod
    def focal_length(radius: float, n1: float, n2: float) -> float:
        """
        단일 곡면의 초점거리 계산
        
        Args:
            radius: 곡률 반경 (mm)
            n1: 입사측 굴절률
            n2: 굴절측 굴절률
            
        Returns:
            초점거리 (mm)
        """
        return radius / (n2 - n1)
    
    @staticmethod
    def thin_lens_focal_length(r1: float, r2: float, n: float) -> float:
        """
        얇은 렌즈 초점거리 계산 (Lensmaker's equation)
        
        Args:
            r1: 첫 번째 면 곡률 반경 (mm)
            r2: 두 번째 면 곡률 반경 (mm)
            n: 렌즈 굴절률
            
        Returns:
            초점거리 (mm)
        """
        return 1 / ((n - 1) * (1/r1 - 1/r2))
    
    @staticmethod
    def f_number(focal_length: float, aperture_diameter: float) -> float:
        """
        F-number 계산
        
        Args:
            focal_length: 초점거리 (mm)
            aperture_diameter: 조리개 직경 (mm)
            
        Returns:
            F-number
        """
        return focal_length / aperture_diameter
    
    @staticmethod
    def numerical_aperture(n: float, half_angle_deg: float) -> float:
        """
        개구수(NA) 계산
        
        Args:
            n: 굴절률
            half_angle_deg: 반각 (도)
            
        Returns:
            개구수 (NA)
        """
        half_angle_rad = np.radians(half_angle_deg)
        return n * np.sin(half_angle_rad)
    
    @staticmethod
    def magnification(object_distance: float, image_distance: float) -> float:
        """
        배율 계산
        
        Args:
            object_distance: 물체 거리 (mm)
            image_distance: 상 거리 (mm)
            
        Returns:
            배율
        """
        return -image_distance / object_distance
    
    @staticmethod
    def rayleigh_resolution(wavelength: float, f_number: float) -> float:
        """
        레이리 분해능 계산
        
        Args:
            wavelength: 파장 (μm)
            f_number: F-number
            
        Returns:
            분해능 (μm)
        """
        return 1.22 * wavelength * f_number
    
    @staticmethod
    def airy_disk_diameter(wavelength: float, f_number: float) -> float:
        """
        에어리 디스크 직경 계산
        
        Args:
            wavelength: 파장 (μm)
            f_number: F-number
            
        Returns:
            에어리 디스크 직경 (μm)
        """
        return 2.44 * wavelength * f_number
    
    @staticmethod
    def hyperfocal_distance(focal_length: float, f_number: float, 
                           coc: float = 0.03) -> float:
        """
        과초점 거리 계산
        
        Args:
            focal_length: 초점거리 (mm)
            f_number: F-number
            coc: 허용 착란원 직경 (mm), 기본값 0.03mm
            
        Returns:
            과초점 거리 (mm)
        """
        return (focal_length ** 2) / (f_number * coc) + focal_length
    
    @staticmethod
    def depth_of_field(object_distance: float, focal_length: float,
                       f_number: float, coc: float = 0.03) -> Tuple[float, float]:
        """
        피사계 심도 계산
        
        Args:
            object_distance: 물체 거리 (mm)
            focal_length: 초점거리 (mm)
            f_number: F-number
            coc: 허용 착란원 직경 (mm)
            
        Returns:
            (근점 거리, 원점 거리) (mm)
        """
        h = (focal_length ** 2) / (f_number * coc) + focal_length
        
        dn = (h * object_distance) / (h + object_distance - focal_length)
        df = (h * object_distance) / (h - object_distance + focal_length)
        
        return dn, df
    
    @staticmethod
    def beam_divergence(wavelength: float, beam_diameter: float) -> float:
        """
        빔 발산각 계산 (가우시안 빔)
        
        Args:
            wavelength: 파장 (μm)
            beam_diameter: 빔 직경 (mm)
            
        Returns:
            발산 반각 (mrad)
        """
        theta_rad = (4 * wavelength * 1e-3) / (np.pi * beam_diameter)
        return theta_rad * 1000  # mrad로 변환
    
    @staticmethod
    def gaussian_beam_waist(wavelength: float, divergence_mrad: float) -> float:
        """
        가우시안 빔 웨이스트 계산
        
        Args:
            wavelength: 파장 (μm)
            divergence_mrad: 발산 반각 (mrad)
            
        Returns:
            빔 웨이스트 반경 (μm)
        """
        divergence_rad = divergence_mrad / 1000
        return (wavelength / np.pi) / divergence_rad


class ThermalOpticsCalculator:
    """열-광학 효과 계산 클래스"""
    
    @staticmethod
    def thermal_focal_shift(focal_length: float, dn_dt: float, 
                           temp_change: float) -> float:
        """
        온도 변화에 따른 초점 이동량 계산
        
        Args:
            focal_length: 초점거리 (mm)
            dn_dt: 굴절률 온도계수 (1/°C)
            temp_change: 온도 변화 (°C)
            
        Returns:
            초점 이동량 (mm)
        """
        return focal_length * dn_dt * temp_change
    
    @staticmethod
    def thermal_expansion(length: float, alpha: float, 
                         temp_change: float) -> float:
        """
        열팽창에 의한 길이 변화 계산
        
        Args:
            length: 원래 길이 (mm)
            alpha: 열팽창계수 (1/°C)
            temp_change: 온도 변화 (°C)
            
        Returns:
            길이 변화량 (mm)
        """
        return length * alpha * temp_change


def calculate_f_theta_distortion(focal_length: float, field_angle_deg: float,
                                 actual_height: float) -> float:
    """
    F-theta 렌즈의 왜곡 계산
    
    Args:
        focal_length: 초점거리 (mm)
        field_angle_deg: 시야각 (도)
        actual_height: 실제 상고 (mm)
        
    Returns:
        왜곡률 (%)
    """
    field_angle_rad = np.radians(field_angle_deg)
    ideal_height = focal_length * field_angle_rad
    distortion = ((actual_height - ideal_height) / ideal_height) * 100
    return distortion


def calculate_spot_size(wavelength: float, focal_length: float,
                       beam_diameter: float, m_squared: float = 1.0) -> float:
    """
    집광 스팟 크기 계산
    
    Args:
        wavelength: 파장 (μm)
        focal_length: 초점거리 (mm)
        beam_diameter: 입사 빔 직경 (mm)
        m_squared: 빔 품질 인자 (기본값 1.0)
        
    Returns:
        스팟 직경 (μm)
    """
    spot_radius = (4 * m_squared * wavelength * focal_length) / (np.pi * beam_diameter)
    return 2 * spot_radius


if __name__ == "__main__":
    # 예제 사용법
    calc = OpticalCalculator()
    
    # F-theta 렌즈 예제
    print("=" * 60)
    print("F-theta Lens Example")
    print("=" * 60)
    
    focal_length = 160  # mm
    field_angle = 12    # degrees
    
    f_theta_height = focal_length * np.radians(field_angle)
    print(f"초점거리: {focal_length} mm")
    print(f"시야각: ±{field_angle}°")
    print(f"이상적인 상고: {f_theta_height:.2f} mm")
    
    # 빔 발산각 계산
    print("\n" + "=" * 60)
    print("Beam Divergence Example")
    print("=" * 60)
    
    wavelength = 1.064  # μm (Nd:YAG)
    beam_dia = 10       # mm
    
    divergence = calc.beam_divergence(wavelength, beam_dia)
    print(f"파장: {wavelength} μm")
    print(f"빔 직경: {beam_dia} mm")
    print(f"빔 발산각: {divergence:.3f} mrad")
    
    # 스팟 크기 계산
    print("\n" + "=" * 60)
    print("Spot Size Example")
    print("=" * 60)
    
    spot_size = calculate_spot_size(wavelength, focal_length, beam_dia, m_squared=1.2)
    print(f"집광 스팟 크기: {spot_size:.1f} μm")
