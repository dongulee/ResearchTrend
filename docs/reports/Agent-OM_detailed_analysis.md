# Agent-OM: LLM 에이전트를 활용한 온톨로지 매칭

## 1. 논문 기본 정보

| 항목 | 내용 |
|------|------|
| **제목** | Agent-OM: Leveraging LLM Agents for Ontology Matching |
| **저자** | Zhangcheng Qiang, Weiqing Wang, Kerry Taylor |
| **소속** | Australian National University, Monash University |
| **학회/연도** | VLDB 2025 (Volume 18, Issue 3) |
| **페이지** | 516-529 |
| **GitHub** | https://github.com/qzc438/ontology-llm |

---

## 2. 연구 배경 및 동기

### 온톨로지 매칭(OM)이란?
서로 다른 온톨로지 간의 의미적 상호운용성을 가능하게 하고, 관련 엔티티를 정렬하는 작업입니다. 데이터 통합, 지식 발견의 핵심 기술입니다.

### 기존 접근법의 한계

**전통적 지식 기반 시스템** (LogMap, AML):
- 도메인 전문가 필요, 노동 집약적

**기계학습 기반 시스템** (BERTMap):
- 훈련 데이터 부족 문제 (도메인 온톨로지는 보통 100-200개 엔티티)
- LLM 재훈련/파인튜닝 비용 문제

**순수 LLM 기반** (OLaLa):
- 환각(Hallucination) 문제
- O(Ns × Nt) 복잡도로 비효율적

---

## 3. 핵심 아이디어

### 새로운 패러다임: LLM을 중앙 컨트롤러로 활용

```
Agent-OM = Retrieval Agent + Matching Agent (공유 메모리)
```

**세 가지 핵심 구성요소**:
1. **계획(Planning)**: Chain-of-Thought로 복잡한 작업 분해
2. **도구(Tools)**: 외부 리소스 호출
3. **메모리(Memory)**: ICL(단기) + RAG(장기)

---

## 4. 시스템 아키텍처

### Retrieval Agent (검색 에이전트)
```
R_int → R_syn → R_lex/R_ext → R_sem → R_sto
```

| 도구 | 기능 |
|------|------|
| Metadata Retriever | 카테고리/타입 수집 |
| Syntactic Retriever | 토큰화, 정규화 |
| Lexical Retriever | LLM으로 의미 해석 |
| Semantic Retriever | 트리플 관계 추출 |
| Hybrid Database | PostgreSQL + pgvector 저장 |

### Matching Agent (매칭 에이전트)
```
M_sea → M_met → M_sel → M_alg → M_ref
```

| 도구 | 기능 |
|------|------|
| Hybrid Database Search | 관계형/벡터 DB 검색 |
| Metadata Matcher | 카테고리/타입 필터링 |
| Syntactic/Lexical/Semantic Matcher | 코사인 유사도 기반 검색 |
| Matching Summariser | **RRF(Reciprocal Rank Fusion)**로 순위 통합 |
| Matching Validator | 이진 질문으로 환각 검증 |
| Matching Merger | 양방향 결과 교집합 |

---

## 5. 실험 결과

### OAEI Conference Track (Few-shot)
- 21개 온톨로지 쌍 정렬
- **F1 Score**: 2022년 3/13위, 2023년 5/12위

### OAEI Anatomy Track
| Test Case | 설명 | 결과 |
|-----------|------|------|
| TC1 (간단한 OM) | Trivial 포함 | F1 **2위** |
| TC2 (복잡한 OM) | Non-trivial만 | 11개 시스템 압도 |

### OAEI MSE Track (재료 과학)
| Test Case | 결과 |
|-----------|------|
| TC1 (복잡한 참조) | **최고 F1** |
| TC2 (도메인 지식) | **정밀도, 재현율, F1 모두 최고** |
| TC3 (간단한 OM) | 경쟁력 있음 |

**핵심 발견**: 복잡하고 Few-shot 작업에서 **기존 시스템 대비 큰 성능 향상**

---

## 6. 기술적 기여점

### 효율성 향상
```
Naive LLM-OM: O(Ns × Nt)  →  Agent-OM: O((k+1)(Ns + Nt))
```
k ≪ Ns, Nt 이므로 대규모 온톨로지에서 훨씬 효율적

### LLM 환각 완화
- RAG 기반 도구로 사실 정보 제공
- Matching Validator로 자기 검증
- 양방향 매칭 교집합으로 신뢰도 향상

### 파인튜닝 불필요
- CoT, ICL/RAG, 프롬프트 엔지니어링만으로 우수한 성능

---

## 7. 한계점

| 한계 | 설명 |
|------|------|
| **확장성** | 매우 큰 온톨로지에서의 성능 |
| **비용** | LLM API 호출 비용 |
| **TBox만 평가** | 인스턴스(ABox) 매칭 미포함 |
| **모라벡의 역설** | 복잡한 문제는 잘 풀지만, 간단한 문제에서 탁월하지 않음 |
| **프롬프트 수작업** | LLM마다 다른 템플릿 필요 |

---

## 8. 관련 연구 비교

| 접근법 | 대표 시스템 | Agent-OM 차이점 |
|--------|------------|-----------------|
| 지식 기반 | LogMap, AML | 전문가 불필요, 자동화 |
| ML 기반 | BERTMap | 파인튜닝 불필요 |
| 순수 LLM | OLaLa | 검색 기반으로 효율적, RAG로 환각 감소 |

---

## 9. 결론

Agent-OM은 **온톨로지 매칭을 위한 최초의 에이전트 기반 LLM 프레임워크**로:

1. **복잡한 OM 작업**에서 기존 시스템 대비 **큰 성능 향상**
2. **간단한 OM 작업**에서 최고 성능에 **근접**
3. LLM 재훈련 없이 **CoT + RAG + 도구 호출**만으로 달성

> *"Agent-OM is all you need"* - 100% 정확하고 완전 자동화된 도메인 독립적 OM을 향한 중요한 진전

---

## 참고 자료

- **논문 PDF**: https://www.vldb.org/pvldb/vol18/p516-qiang.pdf
- **GitHub**: https://github.com/qzc438/ontology-llm
- **로컬 요약 파일**: `data/summaries/40.json`
- **로컬 PDF**: `data/pdfs/40_Agent-OM_Leveraging_LLM_Agents_for_Ontology_Match.pdf`
- **태그**: Natural Language Processing, Data Integration, Machine Learning
