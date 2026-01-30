"""
Agent-OM과 관련 논문들의 상세 비교 분석
"""
import json
from pathlib import Path
from collections import defaultdict, Counter
import re

# 핵심 관련 논문 ID 목록
CORE_PAPERS = [40, 200, 197, 353, 9, 20, 105, 154, 183, 283, 340, 360, 377, 378]

def load_summary(paper_id):
    """요약 파일 로드"""
    summary_path = Path(f'data/summaries/{paper_id}.json')
    if summary_path.exists():
        try:
            with open(summary_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None

def extract_authors(authors_str):
    """저자 문자열에서 개별 저자 추출"""
    # 쉼표로 분리
    authors = [a.strip() for a in authors_str.split(',')]
    return authors

def analyze_author_network():
    """저자 네트워크 분석"""
    author_papers = defaultdict(list)
    author_collaborators = defaultdict(set)

    for paper_id in CORE_PAPERS:
        summary = load_summary(paper_id)
        if summary:
            authors_str = summary.get('authors', '')
            title = summary.get('title', '')
            authors = extract_authors(authors_str)

            for author in authors:
                author_papers[author].append({
                    'id': paper_id,
                    'title': title
                })

                # 공저자 관계
                for other in authors:
                    if other != author:
                        author_collaborators[author].add(other)

    return author_papers, author_collaborators

def analyze_methodology():
    """방법론 비교 분석"""
    methodologies = {}

    for paper_id in CORE_PAPERS:
        summary = load_summary(paper_id)
        if summary:
            title = summary.get('title', '')
            summary_dict = summary.get('summary', {})

            methodologies[paper_id] = {
                'title': title,
                'methodology': summary_dict.get('methodology', ''),
                'contributions': summary_dict.get('contributions', []),
                'experiments': summary_dict.get('experiments', ''),
                'limitations': summary_dict.get('limitations', ''),
                'tags': summary.get('tags', [])
            }

    return methodologies

def analyze_tags():
    """태그 분석"""
    tag_papers = defaultdict(list)
    tag_confidence = defaultdict(list)

    for paper_id in CORE_PAPERS:
        summary = load_summary(paper_id)
        if summary:
            title = summary.get('title', '')
            tags = summary.get('tags', [])

            for tag_info in tags:
                tag = tag_info.get('tag', '')
                confidence = tag_info.get('confidence', 0)

                tag_papers[tag].append({
                    'id': paper_id,
                    'title': title,
                    'confidence': confidence
                })
                tag_confidence[tag].append(confidence)

    return tag_papers, tag_confidence

def main():
    print("="*100)
    print("Agent-OM 관련 핵심 논문 상세 비교 분석")
    print("="*100)

    # 1. 저자 네트워크 분석
    print("\n\n1. 저자 네트워크 분석")
    print("-"*100)

    author_papers, author_collaborators = analyze_author_network()

    # 다중 논문 저자
    multi_paper_authors = {author: papers for author, papers in author_papers.items()
                          if len(papers) > 1}

    if multi_paper_authors:
        print("\n다중 논문 저자 (2편 이상):")
        for author, papers in sorted(multi_paper_authors.items(),
                                     key=lambda x: len(x[1]), reverse=True):
            print(f"\n  {author} ({len(papers)}편):")
            for paper in papers:
                print(f"    - [ID {paper['id']}] {paper['title']}")
    else:
        print("\n핵심 논문들 간 저자 중복 없음")

    # 협력 네트워크
    print("\n\n주요 연구 그룹 (공저자 3명 이상):")
    for author, collaborators in sorted(author_collaborators.items(),
                                       key=lambda x: len(x[1]), reverse=True)[:10]:
        if len(collaborators) >= 3:
            print(f"  {author}: {len(collaborators)}명의 공저자")

    # 2. 방법론 비교
    print("\n\n2. 방법론 상세 비교")
    print("-"*100)

    methodologies = analyze_methodology()

    print("\nAgent-OM (ID: 40)과 다른 논문들의 방법론 비교:\n")

    agent_om = methodologies.get(40)
    if agent_om:
        print(f"[Agent-OM]")
        print(f"  방법론: {agent_om['methodology']}")
        print(f"  기여:")
        for contrib in agent_om['contributions']:
            print(f"    - {contrib}")
        print(f"  한계: {agent_om['limitations']}")

        print("\n\n[비교 대상 논문들]\n")

        for paper_id in [200, 197, 9]:  # Magneto, CatDB, QueryArtisan
            if paper_id in methodologies:
                paper = methodologies[paper_id]
                print(f"\n{'='*80}")
                print(f"[ID {paper_id}] {paper['title']}")
                print(f"{'='*80}")
                print(f"  방법론: {paper['methodology']}")
                print(f"  기여:")
                for contrib in paper['contributions']:
                    print(f"    - {contrib}")
                print(f"  한계: {paper['limitations']}")

    # 3. 태그 분석
    print("\n\n3. 태그 기반 클러스터링")
    print("-"*100)

    tag_papers, tag_confidence = analyze_tags()

    print("\n주요 태그별 논문 분포:\n")

    for tag in sorted(tag_papers.keys(), key=lambda t: len(tag_papers[t]), reverse=True)[:8]:
        papers = tag_papers[tag]
        avg_conf = sum(tag_confidence[tag]) / len(tag_confidence[tag])

        print(f"\n{tag} ({len(papers)}편, 평균 신뢰도: {avg_conf:.2f}):")
        for paper in papers:
            print(f"  - [ID {paper['id']}] {paper['title'][:70]}... (conf: {paper['confidence']})")

    # 4. 기술적 특징 비교
    print("\n\n4. 기술적 특징 비교표")
    print("-"*100)

    comparison_aspects = {
        'LLM 모델': ['GPT-4', 'GPT-3.5', 'BERT', 'T5'],
        'Architecture': ['Agent', 'Pipeline', 'Hybrid', 'Ensemble'],
        'Learning': ['Few-shot', 'Zero-shot', 'Supervised', 'Unsupervised'],
        'Optimization': ['Cost', 'Quality', 'Latency', 'Throughput']
    }

    print("\n핵심 논문별 기술적 특징:\n")
    print(f"{'Paper ID':<12} {'Title':<50} {'주요 태그':<40}")
    print("-"*102)

    for paper_id in CORE_PAPERS[:10]:
        summary = load_summary(paper_id)
        if summary:
            title = summary.get('title', '')[:48]
            tags = summary.get('tags', [])[:2]
            tag_str = ', '.join([t['tag'] for t in tags])

            print(f"{paper_id:<12} {title:<50} {tag_str:<40}")

    # JSON 저장
    output = {
        'author_network': {
            'multi_paper_authors': {author: [p['title'] for p in papers]
                                   for author, papers in multi_paper_authors.items()},
            'collaboration_count': {author: len(collab)
                                   for author, collab in author_collaborators.items()}
        },
        'methodologies': methodologies,
        'tag_analysis': {
            'tag_papers': {tag: [p['title'] for p in papers]
                          for tag, papers in tag_papers.items()},
            'tag_confidence': {tag: sum(confs) / len(confs)
                             for tag, confs in tag_confidence.items()}
        }
    }

    with open('data/agent_om_detailed_comparison.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n\n상세 비교 분석 결과가 'data/agent_om_detailed_comparison.json'에 저장되었습니다.")

if __name__ == '__main__':
    main()
