# PaperResearch

학회 논문 수집, 주제 분류, 요약, 연구 동향 분석을 수행하는 Claude Code 기반 연구 도구

## 설치

```bash
uv sync
```

## 사용법

```bash
# 1. 논문 수집
/collect-papers vldb https://www.vldb.org/pvldb/volumes/18/ 2025

# 2. PDF 다운로드
/download-pdfs vldb 2025

# 3. 논문 요약
/summarize-paper --conference vldb 2025

# 4. 보고서 생성
/generate-report vldb 2025 overview
```

자세한 내용은 [CLAUDE.md](CLAUDE.md) 참조
