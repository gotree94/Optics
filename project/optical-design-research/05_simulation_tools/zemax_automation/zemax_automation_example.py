"""
Zemax Automation Script
Zemax 자동화 스크립트

This script demonstrates basic Zemax OpticStudio automation using ZOS-API.
ZOS-API를 사용한 기본적인 Zemax OpticStudio 자동화를 시연합니다.

Note: This is an example script. Actual implementation requires ZOS-API installation.
참고: 이것은 예제 스크립트입니다. 실제 구현을 위해서는 ZOS-API 설치가 필요합니다.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


class ZemaxAutomation:
    """Zemax 자동화 클래스 (예제)"""
    
    def __init__(self):
        """초기화"""
        self.system = None
        self.lens_data_editor = None
    
    def connect_to_zemax(self):
        """
        Zemax OpticStudio 연결
        
        실제 구현 예제:
        import clr
        clr.AddReference("path/to/ZOSAPI.dll")
        import ZOSAPI
        self.zos = ZOSAPI.ZOSAPI()
        """
        print("Connecting to Zemax OpticStudio...")
        # 실제 연결 코드는 ZOS-API 설치 후 사용
        pass
    
    def create_new_lens(self, system_type="NSC"):
        """
        새 렌즈 시스템 생성
        
        Args:
            system_type: "NSC" or "SEQ"
        """
        print(f"Creating new {system_type} lens system...")
        pass
    
    def add_surface(self, surface_type, radius, thickness, material):
        """
        표면 추가
        
        Args:
            surface_type: 표면 타입 (Standard, Even Asphere, etc.)
            radius: 곡률 반경 (mm)
            thickness: 두께 (mm)
            material: 재질
        """
        print(f"Adding surface: R={radius}, T={thickness}, Material={material}")
        pass
    
    def set_wavelength(self, wavelength_um):
        """
        파장 설정
        
        Args:
            wavelength_um: 파장 (μm)
        """
        print(f"Setting wavelength: {wavelength_um} μm")
        pass
    
    def set_field(self, field_angles):
        """
        시야각 설정
        
        Args:
            field_angles: 시야각 리스트 (degrees)
        """
        print(f"Setting field angles: {field_angles}")
        pass
    
    def optimize_system(self, merit_function):
        """
        시스템 최적화
        
        Args:
            merit_function: 메리트 함수 정의
        """
        print("Running optimization...")
        pass
    
    def get_spot_diagram_data(self):
        """
        스팟 다이어그램 데이터 추출
        
        Returns:
            dict: {wavelength: {field: {x: [], y: []}}}
        """
        # 예제 데이터 생성
        data = {
            0.55: {  # wavelength in μm
                0: {  # field number
                    'x': np.random.normal(0, 5, 1000),
                    'y': np.random.normal(0, 5, 1000)
                }
            }
        }
        return data
    
    def get_mtf_data(self):
        """
        MTF 데이터 추출
        
        Returns:
            dict: {field: {freq: [], mtf_tangential: [], mtf_sagittal: []}}
        """
        # 예제 데이터 생성
        freq = np.linspace(0, 100, 50)
        mtf = np.exp(-freq / 50)
        
        data = {
            0: {
                'freq': freq,
                'mtf_tangential': mtf,
                'mtf_sagittal': mtf * 0.95
            }
        }
        return data
    
    def save_system(self, filepath):
        """
        시스템 저장
        
        Args:
            filepath: 저장 경로
        """
        print(f"Saving system to: {filepath}")
        pass


def example_create_simple_lens():
    """간단한 렌즈 생성 예제"""
    
    print("=" * 60)
    print("Example: Create Simple Doublet Lens")
    print("=" * 60)
    
    zemax = ZemaxAutomation()
    zemax.connect_to_zemax()
    zemax.create_new_lens(system_type="SEQ")
    
    # 파장 설정 (가시광)
    zemax.set_wavelength(0.55)
    
    # 시야각 설정
    zemax.set_field([0, 5, 10])
    
    # 표면 추가
    surfaces = [
        ("Standard", 50, 5, "BK7"),
        ("Standard", -30, 2, ""),
        ("Standard", -30, 5, "SF5"),
        ("Standard", -100, 95, "")
    ]
    
    for surf in surfaces:
        zemax.add_surface(*surf)
    
    # 최적화 (예제)
    merit_function = "RMS_SPOT_SIZE"
    zemax.optimize_system(merit_function)
    
    # 저장
    zemax.save_system("simple_doublet.zmx")
    
    print("\nLens creation completed!")


def example_analyze_spot_diagram():
    """스팟 다이어그램 분석 예제"""
    
    print("\n" + "=" * 60)
    print("Example: Analyze Spot Diagram")
    print("=" * 60)
    
    zemax = ZemaxAutomation()
    data = zemax.get_spot_diagram_data()
    
    # 플롯
    for wavelength, field_data in data.items():
        for field, spots in field_data.items():
            plt.figure(figsize=(8, 8))
            plt.scatter(spots['x'], spots['y'], s=0.5, alpha=0.5)
            plt.xlabel('X (μm)')
            plt.ylabel('Y (μm)')
            plt.title(f'Spot Diagram - λ={wavelength}μm, Field={field}°')
            plt.axis('equal')
            plt.grid(True, alpha=0.3)
            
            # RMS 계산
            rms = np.sqrt(np.mean(spots['x']**2 + spots['y']**2))
            plt.text(0.05, 0.95, f'RMS: {rms:.2f} μm',
                    transform=plt.gca().transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            plt.tight_layout()
            plt.savefig(f'spot_diagram_w{wavelength}_f{field}.png', dpi=150)
            print(f"Saved: spot_diagram_w{wavelength}_f{field}.png")
            plt.close()


def example_analyze_mtf():
    """MTF 분석 예제"""
    
    print("\n" + "=" * 60)
    print("Example: Analyze MTF")
    print("=" * 60)
    
    zemax = ZemaxAutomation()
    data = zemax.get_mtf_data()
    
    # 플롯
    for field, mtf_data in data.items():
        plt.figure(figsize=(10, 6))
        plt.plot(mtf_data['freq'], mtf_data['mtf_tangential'], 
                'b-', linewidth=2, label='Tangential')
        plt.plot(mtf_data['freq'], mtf_data['mtf_sagittal'], 
                'r--', linewidth=2, label='Sagittal')
        
        plt.xlabel('Spatial Frequency (lp/mm)')
        plt.ylabel('MTF')
        plt.title(f'MTF Curve - Field {field}°')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.ylim([0, 1])
        
        # 주요 주파수에서 MTF 표시
        freq_50 = 50
        mtf_50 = np.interp(freq_50, mtf_data['freq'], mtf_data['mtf_tangential'])
        plt.axvline(x=freq_50, color='g', linestyle=':', alpha=0.5)
        plt.text(freq_50 + 2, 0.5, f'MTF@50lp/mm: {mtf_50:.3f}',
                rotation=90, verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig(f'mtf_curve_f{field}.png', dpi=150)
        print(f"Saved: mtf_curve_f{field}.png")
        plt.close()


def batch_analysis(zemax_files):
    """
    배치 분석
    
    Args:
        zemax_files: Zemax 파일 경로 리스트
    """
    print("\n" + "=" * 60)
    print("Batch Analysis")
    print("=" * 60)
    
    results = []
    
    for zmx_file in zemax_files:
        print(f"\nAnalyzing: {zmx_file}")
        
        # 파일 열기 (예제)
        # zemax.open_file(zmx_file)
        
        # 분석 수행
        spot_data = {}  # zemax.get_spot_diagram_data()
        mtf_data = {}   # zemax.get_mtf_data()
        
        results.append({
            'file': zmx_file,
            'spot_data': spot_data,
            'mtf_data': mtf_data
        })
    
    print(f"\nBatch analysis completed for {len(zemax_files)} files")
    return results


if __name__ == "__main__":
    print("Zemax Automation Examples")
    print("=" * 60)
    
    # 예제 실행
    example_create_simple_lens()
    example_analyze_spot_diagram()
    example_analyze_mtf()
    
    # 배치 분석 예제
    files = ["lens1.zmx", "lens2.zmx", "lens3.zmx"]
    # results = batch_analysis(files)
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    
    print("\nNote: This is a demonstration script.")
    print("For actual Zemax automation, install ZOS-API and")
    print("uncomment the actual implementation code.")
