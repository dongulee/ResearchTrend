# PaperResearch

학회 논문 수집, 주제 분류, 요약, 연구 동향 분석을 수행하는 Claude Code 기반 연구 도구

## 패키지 관리

```bash
# 의존성 설치
uv sync

# 개발 의존성 포함 설치
uv sync --all-extras
```

## 프로젝트 구조

```
PaperResearch/
├── .claude/skills/
│   ├── collect-papers/SKILL.md    # 논문 목록 수집
│   ├── download-pdfs/SKILL.md     # PDF 다운로드
│   ├── summarize-paper/SKILL.md   # 논문 요약
│   └── generate-report/SKILL.md   # 보고서 생성
├── src/
│   ├── collectors/          # 학회별 논문 수집기
│   ├── storage/             # 데이터베이스 및 모델
│   └── utils/               # 유틸리티 (설정, PDF 처리)
└── data/                    # 데이터 저장소
    ├── papers.db            # SQLite 메타정보
    ├── pdfs/                # 다운로드된 PDF
    ├── summaries/           # 요약 JSON
    └── reports/             # 생성된 보고서
```

## 스킬 사용법

### /collect-papers - 논문 목록 수집
```
/collect-papers vldb https://www.vldb.org/pvldb/volumes/18/ 2025
```
VLDB proceedings 페이지에서 논문 메타정보를 파싱하여 SQLite DB에 저장

### /download-pdfs - PDF 다운로드
```
/download-pdfs vldb 2025
/download-pdfs vldb 2025 --limit 10
```
수집된 논문의 PDF를 `data/pdfs/`에 다운로드

### /summarize-paper - 논문 요약
```
/summarize-paper 42                           # 단일 논문
/summarize-paper --conference vldb 2025       # 학회 전체
```
PDF 텍스트를 분석하여 요약 생성 및 주제 태그 할당

### /generate-report - 보고서 생성
```
/generate-report vldb 2025 overview   # 개요 보고서
/generate-report vldb 2025 trends     # 트렌드 분석
/generate-report vldb 2025 detailed   # 상세 목록
```
요약 데이터 기반 Markdown 보고서 생성

## 데이터베이스 스키마

- `conferences`: 학회 정보 (name, year, volume, url)
- `papers`: 논문 메타정보 (title, authors, pdf_url, status)
- `paper_tags`: 논문 주제 태그 (tag, confidence)

## 주요 모듈

| 모듈 | 설명 |
|------|------|
| `src/collectors/vldb_collector.py` | VLDB proceedings JSON 파싱 |
| `src/storage/database.py` | SQLite CRUD 작업 |
| `src/utils/pdf_handler.py` | PDF 다운로드 및 텍스트 추출 |
| `src/utils/config.py` | 경로 및 설정 관리 |

## 워크플로우

1. `/collect-papers` → DB에 논문 메타정보 저장
2. `/download-pdfs` → PDF 파일 다운로드
3. `/summarize-paper` → Claude로 요약 생성 + 태그 분류
4. `/generate-report` → 종합 보고서 생성

## 지원 학회

- VLDB (https://www.vldb.org/pvldb/volumes/{volume}/)
