"""
Data Processing Module
데이터 처리 모듈

This module provides utilities for processing measurement and simulation data.
측정 및 시뮬레이션 데이터 처리를 위한 유틸리티를 제공합니다.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Union, List, Dict, Tuple
import json


class ZemaxDataProcessor:
    """Zemax 출력 데이터 처리 클래스"""
    
    @staticmethod
    def read_spot_diagram(filepath: Union[str, Path]) -> pd.DataFrame:
        """
        Zemax Spot Diagram 데이터 읽기
        
        Args:
            filepath: 파일 경로
            
        Returns:
            DataFrame with columns: [x, y, wavelength, field]
        """
        # Zemax 텍스트 출력 파일 파싱 예제
        # 실제 구현은 파일 형식에 따라 조정 필요
        try:
            df = pd.read_csv(filepath, sep='\t', skiprows=10)
            return df
        except Exception as e:
            print(f"Error reading file: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def calculate_rms_spot_size(x: np.ndarray, y: np.ndarray) -> float:
        """
        RMS 스팟 크기 계산
        
        Args:
            x: x 좌표 배열
            y: y 좌표 배열
            
        Returns:
            RMS 스팟 반경 (같은 단위)
        """
        centroid_x = np.mean(x)
        centroid_y = np.mean(y)
        
        r_squared = (x - centroid_x)**2 + (y - centroid_y)**2
        rms = np.sqrt(np.mean(r_squared))
        
        return rms
    
    @staticmethod
    def calculate_geometric_spot_size(x: np.ndarray, y: np.ndarray) -> float:
        """
        기하학적 스팟 크기 계산 (최대 반경)
        
        Args:
            x: x 좌표 배열
            y: y 좌표 배열
            
        Returns:
            최대 반경 (같은 단위)
        """
        centroid_x = np.mean(x)
        centroid_y = np.mean(y)
        
        r = np.sqrt((x - centroid_x)**2 + (y - centroid_y)**2)
        return np.max(r)


class MTFAnalyzer:
    """MTF (Modulation Transfer Function) 분석 클래스"""
    
    @staticmethod
    def calculate_mtf(image: np.ndarray, frequency: float, 
                     pixel_size: float) -> float:
        """
        MTF 계산 (1D FFT 방법)
        
        Args:
            image: 엣지 영상 (2D array)
            frequency: 공간 주파수 (lp/mm)
            pixel_size: 픽셀 크기 (mm)
            
        Returns:
            MTF 값 (0~1)
        """
        # LSF (Line Spread Function) 계산
        lsf = np.mean(np.diff(image, axis=1), axis=0)
        
        # FFT로 MTF 계산
        mtf = np.abs(np.fft.fft(lsf))
        mtf = mtf / mtf[0]  # 정규화
        
        # 주파수 축
        n = len(lsf)
        freq_axis = np.fft.fftfreq(n, pixel_size)
        
        # 원하는 주파수의 MTF 값 보간
        mtf_value = np.interp(frequency, freq_axis[:n//2], mtf[:n//2])
        
        return mtf_value


class AnsysDataProcessor:
    """ANSYS 출력 데이터 처리 클래스"""
    
    @staticmethod
    def read_thermal_results(filepath: Union[str, Path]) -> Dict:
        """
        ANSYS 열해석 결과 읽기
        
        Args:
            filepath: 결과 파일 경로
            
        Returns:
            결과 딕셔너리
        """
        # 예제 구현 - 실제로는 ANSYS 출력 형식에 맞게 조정
        results = {
            'max_temp': 0,
            'min_temp': 0,
            'avg_temp': 0,
            'nodes': [],
            'temperatures': []
        }
        return results
    
    @staticmethod
    def extract_temperature_profile(data: Dict, path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        특정 경로를 따라 온도 프로파일 추출
        
        Args:
            data: 결과 데이터
            path: 경로 정의
            
        Returns:
            (위치, 온도) 배열
        """
        # 예제 구현
        position = np.linspace(0, 100, 100)
        temperature = 25 + 10 * np.sin(position / 10)
        return position, temperature


class MeasurementDataProcessor:
    """측정 데이터 처리 클래스"""
    
    @staticmethod
    def load_csv_data(filepath: Union[str, Path], 
                     skiprows: int = 0) -> pd.DataFrame:
        """
        CSV 측정 데이터 로드
        
        Args:
            filepath: CSV 파일 경로
            skiprows: 건너뛸 행 수
            
        Returns:
            DataFrame
        """
        return pd.read_csv(filepath, skiprows=skiprows)
    
    @staticmethod
    def moving_average(data: np.ndarray, window_size: int) -> np.ndarray:
        """
        이동 평균 필터
        
        Args:
            data: 입력 데이터
            window_size: 윈도우 크기
            
        Returns:
            필터링된 데이터
        """
        return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    
    @staticmethod
    def remove_outliers(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
        """
        이상치 제거 (표준편차 기반)
        
        Args:
            data: 입력 데이터
            threshold: 표준편차 배수
            
        Returns:
            이상치가 제거된 데이터
        """
        mean = np.mean(data)
        std = np.std(data)
        
        mask = np.abs(data - mean) < threshold * std
        return data[mask]
    
    @staticmethod
    def calculate_uncertainty(data: np.ndarray, confidence: float = 0.95) -> Tuple[float, float]:
        """
        측정 불확도 계산
        
        Args:
            data: 측정 데이터
            confidence: 신뢰 수준
            
        Returns:
            (평균, 불확도)
        """
        from scipy import stats
        
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        n = len(data)
        
        # t-분포 사용
        t_value = stats.t.ppf((1 + confidence) / 2, n - 1)
        uncertainty = t_value * std / np.sqrt(n)
        
        return mean, uncertainty


class ReportGenerator:
    """보고서 생성 클래스"""
    
    @staticmethod
    def generate_summary_plot(data: Dict, save_path: Union[str, Path]):
        """
        요약 플롯 생성
        
        Args:
            data: 플롯할 데이터 딕셔너리
            save_path: 저장 경로
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 예제 플롯들
        # 1. 온도 분포
        if 'temperature' in data:
            axes[0, 0].plot(data['temperature'])
            axes[0, 0].set_title('Temperature Distribution')
            axes[0, 0].set_xlabel('Position')
            axes[0, 0].set_ylabel('Temperature (°C)')
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 스팟 다이어그램
        if 'spot_x' in data and 'spot_y' in data:
            axes[0, 1].scatter(data['spot_x'], data['spot_y'], s=1)
            axes[0, 1].set_title('Spot Diagram')
            axes[0, 1].set_xlabel('X (μm)')
            axes[0, 1].set_ylabel('Y (μm)')
            axes[0, 1].set_aspect('equal')
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. MTF 곡선
        if 'mtf_freq' in data and 'mtf_value' in data:
            axes[1, 0].plot(data['mtf_freq'], data['mtf_value'])
            axes[1, 0].set_title('MTF Curve')
            axes[1, 0].set_xlabel('Spatial Frequency (lp/mm)')
            axes[1, 0].set_ylabel('MTF')
            axes[1, 0].grid(True, alpha=0.3)
            axes[1, 0].set_ylim([0, 1])
        
        # 4. 성능 요약
        if 'performance' in data:
            perf = data['performance']
            axes[1, 1].axis('off')
            
            text = "Performance Summary\n" + "="*30 + "\n\n"
            for key, value in perf.items():
                text += f"{key}: {value}\n"
            
            axes[1, 1].text(0.1, 0.9, text, transform=axes[1, 1].transAxes,
                           verticalalignment='top', fontfamily='monospace',
                           fontsize=10)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    @staticmethod
    def export_to_excel(data: Dict, filepath: Union[str, Path]):
        """
        데이터를 Excel 파일로 내보내기
        
        Args:
            data: 데이터 딕셔너리 (각 키는 시트가 됨)
            filepath: Excel 파일 경로
        """
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, df in data.items():
                if isinstance(df, pd.DataFrame):
                    df.to_excel(writer, sheet_name=sheet_name, index=False)


if __name__ == "__main__":
    # 예제: 스팟 크기 계산
    print("=" * 60)
    print("Spot Size Analysis Example")
    print("=" * 60)
    
    # 시뮬레이션 데이터 생성
    np.random.seed(42)
    n_rays = 10000
    
    # 가우시안 분포를 따르는 스팟
    x = np.random.normal(0, 10, n_rays)  # μm
    y = np.random.normal(0, 10, n_rays)
    
    processor = ZemaxDataProcessor()
    rms_spot = processor.calculate_rms_spot_size(x, y)
    geo_spot = processor.calculate_geometric_spot_size(x, y)
    
    print(f"총 광선 수: {n_rays}")
    print(f"RMS 스팟 반경: {rms_spot:.2f} μm")
    print(f"기하학적 스팟 반경: {geo_spot:.2f} μm")
    
    # 플롯
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=0.5, alpha=0.5)
    plt.xlabel('X (μm)')
    plt.ylabel('Y (μm)')
    plt.title('Spot Diagram')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    
    # RMS 원 그리기
    circle = plt.Circle((0, 0), rms_spot, fill=False, 
                       color='r', linewidth=2, label=f'RMS: {rms_spot:.1f} μm')
    plt.gca().add_patch(circle)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('/home/claude/spot_diagram.png', dpi=150)
    print(f"\n그래프 저장 완료: spot_diagram.png")
    
    # 예제: 측정 불확도 계산
    print("\n" + "=" * 60)
    print("Measurement Uncertainty Example")
    print("=" * 60)
    
    # 시뮬레이션 측정 데이터
    true_value = 100.0
    measurements = np.random.normal(true_value, 0.5, 20)
    
    meas_processor = MeasurementDataProcessor()
    mean, uncertainty = meas_processor.calculate_uncertainty(measurements, confidence=0.95)
    
    print(f"측정 횟수: {len(measurements)}")
    print(f"평균: {mean:.3f}")
    print(f"불확도 (95% 신뢰수준): ±{uncertainty:.3f}")
    print(f"결과: {mean:.3f} ± {uncertainty:.3f}")
