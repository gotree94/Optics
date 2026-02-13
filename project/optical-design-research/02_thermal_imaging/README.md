# Thermal Imaging (열상 광학)

LWIR(Long Wave Infrared) 열상 광학 모듈 설계 및 분석

## 📁 구조

### 1. LWIR Module
8-14μm 파장 대역 열상 광학 모듈

#### 12deg FOV (12도 시야각)
- **응용**: 망원 모드, 목표물 식별
- **사양**:
  - 시야각: 12° × 9°
  - 초점거리: 100mm
  - F/# = 1.0
  - 탐지 거리: > 600m

#### 40deg FOV (40도 시야각)
- **응용**: 광각 모드, 상황 인식
- **사양**:
  - 시야각: 40° × 30°
  - 초점거리: 25mm
  - F/# = 1.0
  - 시야 범위: > 200m

#### Dual FOV System (이중 시야각 시스템)
- **특징**: 
  - 빠른 시야각 전환 (< 0.5초)
  - 동일 검출기 사용
  - 소형 경량 설계

### 2. Lens Design
렌즈 광학 설계

#### Zemax Files
- `lwir_12deg.zmx` - 12도 망원 렌즈
- `lwir_40deg.zmx` - 40도 광각 렌즈
- `dual_fov.zmx` - 이중 시야각 통합 설계

#### Tolerance Analysis
- `tolerance_budget.xlsx` - 공차 예산
- `manufacturing_tolerances.pdf` - 제조 공차 분석
- `assembly_tolerances.pdf` - 조립 공차 분석

### 3. Detector Interface
검출기 인터페이스 설계

## 🎯 설계 목표

### 광학 성능
- **MTF**: > 0.3 @ 17 cy/mm
- **왜곡**: < 2%
- **상대 조도**: > 50% @ 최대 시야각

### 기계적 성능
- **무게**: < 2kg
- **크기**: 120mm × 80mm × 60mm
- **작동 온도**: -40°C ~ +71°C

### 환경 사양
- **진동**: MIL-STD-810G
- **충격**: MIL-STD-810G
- **방수**: IP67

## 🔬 분석 도구

### MTF 분석
```python
# MTF 계산 및 플롯
python scripts/mtf_analysis.py --lens lwir_12deg.zmx --detector VOx_640x480
```

### 열 변형 해석
```python
# 온도 변화에 따른 광학 성능 분석
python scripts/thermal_optical_analysis.py --temp_range -40:71 --step 10
```

## 📊 성능 데이터

### 12도 FOV 성능
| 파라미터 | 사양 | 측정값 |
|---------|------|--------|
| MTF @ 17cy/mm | > 0.3 | 0.42 |
| 왜곡 | < 2% | 1.2% |
| 무게 | < 2kg | 1.75kg |

### 40도 FOV 성능
| 파라미터 | 사양 | 측정값 |
|---------|------|--------|
| MTF @ 17cy/mm | > 0.3 | 0.38 |
| 왜곡 | < 2% | 1.8% |
| 무게 | < 2kg | 1.65kg |

## 🛠️ 설계 가이드라인

### 재료 선택
- **렌즈**: Germanium (Ge), Chalcogenide Glass
- **하우징**: Aluminum 6061-T6
- **윈도우**: ZnSe with AR coating

### 코팅
- **AR 코팅**: LWIR 대역 최적화
- **목표 반사율**: < 0.5% per surface

### 아써멀 설계
- **온도 보상**: Passive athermalization
- **초점 이동**: < ±50μm over -40~+71°C

## 📚 기술 문서

### 설계 사양서
- `Design_Specification_LWIR_12deg.pdf`
- `Design_Specification_LWIR_40deg.pdf`

### 분석 보고서
- `Optical_Performance_Report.pdf`
- `Thermal_Analysis_Report.pdf`
- `Tolerance_Analysis_Report.pdf`

## 🔗 참고 자료

- [FLIR Thermal Imaging Guidebook](https://www.flir.com/)
- [Edmund Optics - LWIR Imaging](https://www.edmundoptics.com/)
- [MIL-STD-810G Environmental Testing](https://www.atecorp.com/)
