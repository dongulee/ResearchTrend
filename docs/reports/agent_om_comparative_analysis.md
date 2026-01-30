# Agent-OM 관련 VLDB 2025 논문 비교 분석 보고서

생성일: 2026-01-30

## 1. 개요

### 1.1 분석 범위
- 대상 학회: VLDB 2025
- 전체 논문 수: 480편
- 관련 논문 수: 141편 (29.4%)
- 핵심 관련 논문: 상위 30편 집중 분석

### 1.2 Agent-OM 논문 정보
- **논문 ID**: 40
- **제목**: Agent-OM: Leveraging LLM Agents for Ontology Matching
- **저자**: Zhangcheng Qiang, Weiqing Wang, Kerry Taylor
- **PDF URL**: https://www.vldb.org/pvldb/vol18/p516-qiang.pdf

#### 핵심 특징
- **연구 목적**: LLM 에이전트를 활용한 온톨로지 매칭 시스템 설계
- **방법론**: 검색과 매칭을 위한 두 개의 Siamese 에이전트와 OM 도구 세트로 구성된 Agent-OM 프레임워크
- **주요 기여**:
  1. 에이전트 기반 LLM OM 설계 패러다임 제안
  2. Agent-OM 일반 프레임워크
  3. 복잡하고 few-shot OM 태스크 성능 향상
- **실험 결과**: OAEI 3개 트랙에서 간단한 OM은 최고 성능에 근접, 복잡한/few-shot OM은 크게 향상
- **한계점**: 매우 큰 온톨로지에서의 확장성, LLM 비용

---

## 2. 카테고리별 논문 분포

| 카테고리 | 논문 수 | 비율 |
|---------|---------|------|
| LLM Agents | 39 | 27.7% |
| Ontology Matching | 10 | 7.1% |
| Knowledge Graph | 9 | 6.4% |
| Data Integration | 9 | 6.4% |
| NLP Database | 8 | 5.7% |
| Entity Matching | 1 | 0.7% |

### 주요 관찰
- LLM/Agent 기반 접근이 압도적으로 많음 (39편)
- 온톨로지 매칭 직접 관련 논문도 10편으로 상당수
- 지식 그래프와 데이터 통합 관련 논문이 각각 9편

---

## 3. 직접 관련 논문 (온톨로지/스키마 매칭)

### 3.1 Magneto (논문 ID: 200) - 최고 관련성
**제목**: Combining Small and Large Language Models for Schema Matching

**저자**: Yurong Liu, Eduardo Pena, Aecio Santos, Eden Wu, Juliana Freire

**관련성 점수**: 14 (Agent-OM과 동일)

**연구 내용**:
- **목적**: 데이터 발견을 위한 소형 및 대형 언어 모델 결합
- **방법론**: 소형 모델로 초기 필터링 후 대형 모델로 정제하여 비용과 품질 균형
- **기여**: 소형/대형 LM 결합 Magneto, 비용 효율적 데이터 발견
- **실험**: 대형 모델만 사용 대비 비용 절감
- **한계**: 소형 모델의 필터링 품질에 의존

**Agent-OM과의 비교**:
- **공통점**:
  - LLM 활용한 매칭 문제 해결
  - 비용 효율성 고려
  - Data Integration 태그 공통
- **차이점**:
  - Magneto는 소형/대형 모델 조합에 초점
  - Agent-OM은 에이전트 기반 아키텍처
  - Magneto는 스키마 매칭, Agent-OM은 온톨로지 매칭

---

### 3.2 CatDB (논문 ID: 197)
**제목**: Data-catalog-guided, LLM-based Generation of Data-centric ML Pipelines

**저자**: Saeed Fathollahzadeh, Essam Mansour, Matthias Boehm

**관련성 점수**: 14

**연구 내용**:
- **목적**: 데이터 카탈로그 기반 LLM Text-to-SQL 생성
- **방법론**: 데이터 카탈로그의 메타데이터를 활용하여 LLM의 Text-to-SQL 정확도 향상
- **주요 기여**: 데이터 카탈로그 기반 Text-to-SQL CatDB, 메타데이터 활용
- **핵심 발견**: 데이터 카탈로그가 NL2SQL에 유용, 메타데이터가 정확도 향상의 핵심

**Agent-OM과의 연관성**:
- 메타데이터 활용 접근이 유사 (온톨로지도 메타데이터의 일종)
- LLM을 구조화된 데이터 이해에 활용한다는 공통점
- 둘 다 Data Integration 문제 해결

---

### 3.3 BIRDIE (논문 ID: 154)
**제목**: Natural Language-Driven Table Discovery Using Differentiable Search Index

**저자**: Yuxiang Guo, Zhonghao Hu, Yuren Mao, Baihua Zheng, Yunjun Gao, Mingwei Zhou

**관련성 점수**: 12

**연구 내용**:
- **목적**: 미분 가능한 검색 인덱스를 사용한 자연어 기반 테이블 발견
- **방법론**: 자연어 쿼리를 기반으로 관련 테이블을 발견하는 미분 가능한 검색 인덱스
- **주요 발견**: 미분 가능 인덱스가 테이블 발견에 효과적, 자연어가 테이블 검색 접근성 향상

**Agent-OM과의 연관성**:
- 자연어 기반 검색이라는 공통 접근
- 데이터 발견 문제 해결
- 스키마/구조 이해 필요

---

## 4. LLM/Agent 기반 데이터 관리 (39편)

### 4.1 주요 시스템 및 프레임워크

#### QueryArtisan (논문 ID: 9)
- **저자**: Xiu Tang, Wenhao Liu, Sai Wu, Chang Yao, Gongsheng Yuan, Shanshan Ying, Gang Chen
- **핵심**: 데이터 레이크에서 자연어를 사용하여 직접 쿼리할 수 있는 LLM 기반 분석 도구
- **특징**: 중간 스키마 없이 자연어로 데이터 레이크 직접 쿼리
- **Agent-OM과의 관계**: 스키마 없이 데이터 접근 - 온톨로지 매칭의 필요성 감소

#### LEAP (논문 ID: 20)
- **저자**: Chuxuan Hu, Austin Peters, Daniel Kang
- **핵심**: 비정형 데이터에 대한 사회과학 쿼리를 자연어로 처리
- **성과**: QUIET-ML 데이터셋에서 pass@3 100%, pass@1 92% 달성
- **특징**: 모호한 쿼리 필터링으로 결정적 답변 보장

#### TabulaX (논문 ID: 283)
- **저자**: Arash Dargahi Nobari, Davood Rafiei
- **핵심**: 다중 클래스 테이블 변환을 위한 LLM 활용
- **특징**: 다양한 형식의 테이블 변환 자동화

#### GalaxyWeaver (논문 ID: 378)
- **저자**: Bing Tong, Yan Zhou, Chen Zhang, Jianheng Tang, Jia Li, Lei Chen
- **핵심**: LLM을 활용한 자율 테이블-그래프 변환과 스키마 최적화
- **특징**: 테이블 데이터를 그래프로 자동 변환
- **Agent-OM과의 관계**: 스키마 변환이라는 공통 주제

---

### 4.2 멀티 에이전트 시스템

#### AutoPrep (논문 ID: 259)
- **저자**: Meihao Fan, Ju Fan, Nan Tang, Lei Cao, Guoliang Li, Xiaoyong Du
- **핵심**: 자연어 질문 인식 데이터 준비를 위한 멀티 에이전트 프레임워크
- **특징**: LLM 기반 멀티 에이전트로 질문에 맞는 데이터 준비 자동화
- **Agent-OM과의 유사성**: 멀티 에이전트 아키텍처 활용

---

### 4.3 테이블 이해 및 변환

#### CENTS (논문 ID: 340)
- **저자**: Guorui Xiao, Dong He, Jin Wang, Magdalena Balazinska
- **핵심**: LLM 기반 테이블 이해를 위한 유연하고 비용 효율적 프레임워크
- **특징**: 비용 절감과 정확도 유지

#### OpenMEL (논문 ID: 183)
- **저자**: Xinyi Zhu, Yongqi Zhang, Lei Chen
- **핵심**: LLM을 사용한 비지도 멀티모달 엔티티 링킹
- **특징**: 레이블 없이 학습, 지도 방법과 유사한 성능

---

## 5. 지식 그래프 관련 (9편)

### 5.1 From Genesis to Maturity (논문 ID: 105)
**저자**: Sandra Geisler, Cinzia Cappiello, Irene Celino, David Chaves-Fraga, Anastasia Dimou, Ana Iglesias-Molina, Maurizio Lenzerini, Anisa Rula, Dylan Van Assche, Sascha Welten, Maria-Esther Vidal

**연구 내용**:
- **목적**: 지식 그래프 관리의 핵심 과제를 해결하기 위한 생태계 및 생애주기 개념 제안
- **방법론**: 데이터 통합, 표준화, 지속적 업데이트, 효율적 쿼리, 출처 추적 등의 작업을 체계적으로 관리
- **핵심 발견**: KG 생태계 관점이 체계적 관리에 효과적, 이종 데이터 통합에서 KG의 핵심 역할

**Agent-OM과의 연관성**:
- 온톨로지는 지식 그래프의 스키마
- 데이터 통합이 핵심 주제
- 이종 데이터 처리

### 5.2 LEADRE (논문 ID: 353)
**저자**: Fengxin Li, Yi Li, Yue Liu, Chao Zhou, Yuan Wang, Xiaoxiang Deng, Wei Xue, Dapeng Liu, Lei Xiao, Haijie Gu, Jie Jiang, Hongyan Liu, Biao Qin, Jun He

**연구 내용**:
- **목적**: 다면적 지식 강화 LLM 기반 디스플레이 광고 추천 시스템
- **특징**: 지식 그래프와 LLM 결합

### 5.3 SDG-KG (논문 ID: 422)
**저자**: Wissal Benjira, Nicolas Travers, Bénédicte Bucher, Malika Grim-Yefsah, Faten Atigui

**연구 내용**:
- **목적**: 오픈 데이터를 사용하여 SDG 지표를 계산하는 프레임워크
- **특징**: 지식 그래프로 SDG 지표 계산 자동화

---

## 6. 비교 분석

### 6.1 기술적 접근 방식

#### Agent-OM의 독특한 점
1. **Siamese Agent 아키텍처**: 검색과 매칭을 위한 두 개의 에이전트
2. **OM 도구 세트**: 전문 온톨로지 매칭 도구 통합
3. **Few-shot 학습**: 적은 예제로 복잡한 매칭 학습
4. **OAEI 벤치마크**: 표준 온톨로지 매칭 평가

#### 유사 논문들의 접근
1. **모델 조합** (Magneto): 소형/대형 모델 조합으로 비용 효율
2. **메타데이터 활용** (CatDB): 데이터 카탈로그 활용
3. **미분 가능 인덱스** (BIRDIE): 엔드투엔드 학습
4. **멀티 에이전트** (AutoPrep): 작업별 에이전트 분산

---

### 6.2 연구 문제별 분류

| 연구 문제 | 논문 수 | 대표 논문 |
|----------|---------|-----------|
| 스키마/온톨로지 매칭 | 10 | Agent-OM, Magneto |
| Text-to-SQL/NL2Query | 8 | CatDB, TableCopilot |
| 테이블 발견/이해 | 7 | BIRDIE, CENTS |
| 지식 그래프 구축/관리 | 9 | From Genesis to Maturity, SDG-KG |
| 데이터 변환 | 6 | TabulaX, GalaxyWeaver |
| 엔티티 매칭/링킹 | 2 | OpenMEL |
| BI/분석 자동화 | 5 | SiriusBI, QueryArtisan |

---

### 6.3 공통점

1. **LLM 중심 접근**: 대부분 GPT 계열 모델 활용
2. **비용 효율성 고려**: LLM 비용 절감 전략 필수
3. **자연어 인터페이스**: 사용자 접근성 향상
4. **데이터 통합 문제**: 이종 데이터 소스 통합
5. **Few-shot/Zero-shot 학습**: 레이블 데이터 부족 문제 해결

---

### 6.4 차이점

| 특징 | Agent-OM | Magneto | CatDB | QueryArtisan |
|------|----------|---------|-------|--------------|
| 주요 작업 | 온톨로지 매칭 | 스키마 매칭 | Text-to-SQL | 데이터 레이크 쿼리 |
| 아키텍처 | Siamese Agents | Small+Large LM | Catalog-guided | Just-in-time Code Gen |
| 데이터 형식 | OWL/RDF | 테이블 | SQL DB | 다중 모달리티 |
| 평가 벤치마크 | OAEI | 데이터 발견 | Spider, BIRD | 실제 데이터 레이크 |
| 비용 전략 | 도구 세트 활용 | 모델 조합 | 메타데이터 필터링 | 비용 모델 최적화 |

---

## 7. 연구 트렌드 분석

### 7.1 주요 트렌드

1. **LLM 에이전트화**: 단순 모델 호출에서 에이전트 기반 시스템으로 진화
   - Agent-OM, AutoPrep 등 멀티 에이전트 프레임워크
   - 작업별 전문화된 에이전트

2. **비용 효율성 최적화**:
   - 소형/대형 모델 조합 (Magneto)
   - 메타데이터 기반 필터링 (CatDB)
   - 예산 인식 처리 (Doctopus)

3. **자연어 인터페이스 보편화**:
   - Text-to-SQL (8편)
   - 자연어 기반 테이블 발견 (5편)
   - 질문 응답 기반 분석 (7편)

4. **스키마/온톨로지 자동화**:
   - 매칭 자동화 (10편)
   - 변환 자동화 (6편)
   - 발견 자동화 (7편)

5. **멀티모달 통합**:
   - 텍스트 + 이미지 (OpenMEL)
   - 테이블 + 그래프 (GalaxyWeaver)
   - 비정형 데이터 통합 (Unify, DocDB)

---

### 7.2 시간적 진화

**1세대** (전통적 접근):
- 규칙 기반 매칭
- 수작업 스키마 통합
- 전문가 시스템

**2세대** (ML 기반):
- 지도 학습 매칭 모델
- 특성 공학
- 레이블 데이터 의존

**3세대** (LLM 시대 - VLDB 2025):
- Few-shot/Zero-shot 학습
- 자연어 이해 활용
- 에이전트 기반 아키텍처
- 비용 효율 최적화

---

## 8. 연구진 분석

### 8.1 주요 연구 그룹

#### Zhejiang University (Gang Chen 그룹)
- **논문**: QueryArtisan (9), TableCopilot (430), QueryArtisan Demo (397)
- **주제**: 데이터 레이크, 자연어 기반 쿼리
- **특징**: 실용적 시스템 구축

#### HKUST (Lei Chen 그룹)
- **논문**: OpenMEL (183), GalaxyWeaver (378)
- **주제**: 엔티티 링킹, 테이블-그래프 변환
- **특징**: 멀티모달 처리

#### University of Washington (Magdalena Balazinska)
- **논문**: CENTS (340)
- **주제**: LLM 기반 테이블 이해
- **특징**: 비용 효율성

#### NYU (Juliana Freire)
- **논문**: Magneto (200)
- **주제**: 스키마 매칭
- **특징**: 모델 조합 전략

#### Tsinghua University (Guoliang Li)
- **논문**: AutoPrep (259), Unify (402)
- **주제**: 데이터 준비, 비정형 데이터 분석
- **특징**: 멀티 에이전트 시스템

---

### 8.2 지역별 분포

| 지역 | 논문 수 | 주요 기관 |
|------|---------|-----------|
| 중국 | 18 | Zhejiang Univ, Tsinghua, HKUST |
| 유럽 | 6 | ETH Zurich, FU Berlin, Univ of Milan |
| 미국 | 4 | NYU, UW, Stanford |
| 기타 | 2 | Australia (ANU) |

---

## 9. Agent-OM과의 구체적 비교

### 9.1 직접 경쟁 논문: Magneto

**우위점 (Agent-OM)**:
- 온톨로지 매칭 전문화
- Siamese 아키텍처로 대칭성 보장
- OAEI 표준 벤치마크 활용
- Few-shot 학습에 강점

**우위점 (Magneto)**:
- 비용 효율성 (소형 모델 활용)
- 스케일러블한 필터링
- 데이터 발견 일반화

---

### 9.2 보완적 논문: From Genesis to Maturity

**연관성**:
- 온톨로지는 KG의 스키마
- Agent-OM으로 온톨로지 매칭 → KG 통합
- 생애주기 관리에서 매칭은 초기 단계

**통합 가능성**:
- Agent-OM을 KG 생태계에 통합
- 지속적 온톨로지 진화 지원

---

### 9.3 대안적 접근: QueryArtisan

**차이점**:
- Agent-OM: 스키마 매칭으로 통합
- QueryArtisan: 스키마 없이 직접 쿼리

**트레이드오프**:
- Agent-OM: 초기 매칭 비용, 이후 효율적 통합
- QueryArtisan: 즉시 쿼리, 매번 LLM 비용

---

## 10. 연구 방향 및 시사점

### 10.1 Agent-OM의 강점

1. **전문화된 접근**: 온톨로지 매칭 특화
2. **에이전트 아키텍처**: 확장 가능하고 모듈화
3. **Few-shot 학습**: 레이블 데이터 부족 환경
4. **도구 통합**: 기존 OM 도구 활용

---

### 10.2 개선 가능 영역

1. **비용 효율성**: Magneto의 소형/대형 모델 조합 기법 도입
2. **스케일러빌리티**: 매우 큰 온톨로지 처리 최적화
3. **멀티모달**: OpenMEL처럼 이미지 등 다중 모달리티 지원
4. **생태계 통합**: KG 생애주기 관리와 통합

---

### 10.3 향후 연구 방향

1. **하이브리드 접근**:
   - Agent-OM + Magneto (비용 효율)
   - Agent-OM + CatDB (메타데이터 활용)

2. **벤치마크 확장**:
   - OAEI 외 실제 산업 데이터셋
   - 멀티모달 온톨로지 매칭

3. **스케일 최적화**:
   - 분산 에이전트 아키텍처
   - 점진적 매칭 (Chameleon의 disaggregated 접근)

4. **응용 확장**:
   - 지식 그래프 통합
   - RAG 시스템 스키마 통합
   - 데이터 레이크 메타데이터 관리

---

## 11. 결론

### 11.1 핵심 발견

1. **LLM 에이전트 패러다임의 부상**: VLDB 2025에서 39편의 LLM 에이전트 논문 - 데이터 관리의 새로운 트렌드

2. **온톨로지/스키마 매칭의 중요성 지속**: 10편의 직접 관련 논문 - 여전히 핵심 문제

3. **비용 효율성이 핵심 과제**: 대부분 논문이 LLM 비용 최적화 전략 제시

4. **자연어 인터페이스 보편화**: 전문 지식 없이 데이터 접근 - 민주화

5. **멀티모달 및 이종 데이터 통합**: 복잡한 현실 데이터 환경 반영

---

### 11.2 Agent-OM의 위치

- **선도적 연구**: LLM 에이전트를 온톨로지 매칭에 적용한 초기 연구
- **차별화된 접근**: Siamese 에이전트 아키텍처로 대칭성 보장
- **검증된 성능**: OAEI 벤치마크에서 효과 입증
- **개선 가능성**: 비용 효율, 스케일러빌리티에서 추가 최적화 여지

---

### 11.3 학계 기여

VLDB 2025에서 Agent-OM과 관련 연구들은 다음을 보여줌:

1. **LLM이 데이터 통합 문제의 게임 체인저**: 전통적 방법 대비 획기적 성능
2. **에이전트 기반 접근이 복잡한 작업에 효과적**: 모듈화와 전문화
3. **비용과 품질의 트레이드오프 해결 필요**: 실용적 배포를 위한 핵심
4. **자연어가 데이터 관리를 민주화**: 전문가 의존도 감소

---

## 12. 참고 자료

### 주요 관련 논문 (상위 10편)

1. **Agent-OM** (ID: 40) - 본 논문
   - https://www.vldb.org/pvldb/vol18/p516-qiang.pdf

2. **Magneto** (ID: 200) - 스키마 매칭
   - https://www.vldb.org/pvldb/vol18/p2681-freire.pdf

3. **CatDB** (ID: 197) - Text-to-SQL
   - https://www.vldb.org/pvldb/vol18/p2639-fathollahzadeh.pdf

4. **LEADRE** (ID: 353) - 지식 강화 LLM
   - https://www.vldb.org/pvldb/vol18/p4763-he.pdf

5. **QueryArtisan** (ID: 9) - 데이터 레이크 쿼리
   - https://www.vldb.org/pvldb/vol18/p108-yao.pdf

6. **LEAP** (ID: 20) - 비정형 데이터 쿼리
   - https://www.vldb.org/pvldb/vol18/p253-hu.pdf

7. **From Genesis to Maturity** (ID: 105) - KG 생애주기
   - https://www.vldb.org/pvldb/vol18/p1390-geisler.pdf

8. **BIRDIE** (ID: 154) - 테이블 발견
   - https://www.vldb.org/pvldb/vol18/p2070-gao.pdf

9. **OpenMEL** (ID: 183) - 엔티티 링킹
   - https://www.vldb.org/pvldb/vol18/p2454-zhu.pdf

10. **TabulaX** (ID: 283) - 테이블 변환
    - https://www.vldb.org/pvldb/vol18/p3826-nobari.pdf

---

**보고서 작성**: Claude Code (Agent-OM 관련 논문 분석 시스템)
**데이터 소스**: VLDB 2025 (480편 중 141편 관련 논문 분석)
