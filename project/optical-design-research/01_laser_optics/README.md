# Laser Optics (레이저 광학)

이 디렉토리는 레이저 광학 시스템 설계 및 분석 프로젝트를 포함합니다.

## 📁 구조

### 1. Beam Shaping (빔 정형)
레이저 다이오드의 타원형 빔을 원형 빔으로 변환하는 광학계 설계

#### Collimation Lens (콜리메이션 렌즈)
- **목적**: 레이저 다이오드 출력 빔의 고속축 콜리메이션
- **주요 파일**:
  - `fac_design.zmx` - 고속축 콜리메이터 Zemax 파일
  - `collimation_analysis.xlsx` - 성능 분석 결과
  - `design_notes.md` - 설계 노트

#### Cylindrical Lens (원통형 렌즈)
- **목적**: 빔 정형 및 원형화
- **주요 파일**:
  - `cylindrical_pair.zmx` - 원통형 렌즈 쌍 설계
  - `beam_circularization.py` - 빔 원형도 분석 스크립트

#### Prism Pair (프리즘 쌍)
- **목적**: 비대칭 빔 보정
- **주요 파일**:
  - `anamorphic_prism.zmx` - 프리즘 설계
  - `beam_shaping_analysis.m` - MATLAB 분석 스크립트

### 2. F-theta Lens (F-theta 렌즈)
레이저 스캐닝 시스템용 텔레센트릭 F-theta 렌즈

#### Telecentric Design (텔레센트릭 설계)
- **사양**:
  - 초점거리: 100-600mm
  - 시야각: ±12°
  - F-theta 왜곡: < 0.5%

#### Scanning System (스캐닝 시스템)
- **구성**:
  - Galvanometer 스캐너
  - F-theta 렌즈
  - 보호 윈도우

### 3. Fiber Coupling (광섬유 커플링)
고출력 레이저 다이오드-광섬유 커플링 시스템

#### Coupling Efficiency (커플링 효율)
- **목표**: > 85% 효율
- **분석 도구**:
  - `coupling_simulation.zmx`
  - `efficiency_calculator.py`

## 🔧 사용 방법

### Zemax 파일 열기
```bash
# Zemax OpticStudio에서 .zmx 파일 열기
# File → Open → [파일 선택]
```

### Python 스크립트 실행
```python
# 빔 정형 분석 예제
python beam_circularization.py --input collimation_data.csv --output results/
```

## 📊 주요 성능 지표

| 항목 | 목표 | 달성 |
|------|------|------|
| 빔 품질 (M²) | < 1.3 | 1.21 |
| 빔 원형도 | > 95% | 97.2% |
| 커플링 효율 | > 85% | 87.5% |

## 📚 참고 문헌

1. W. Koechner, "Solid-State Laser Engineering"
2. K. Thyagarajan, "Fiber Optic Essentials"
3. G. Spühler et al., "Beam shaping with cylindrical lenses"

## 🔗 관련 링크

- [Zemax OpticStudio Documentation](https://support.zemax.com/)
- [Laser Diode Beam Shaping Tutorial](https://www.thorlabs.com/)
