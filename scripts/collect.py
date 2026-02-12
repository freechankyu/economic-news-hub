#!/usr/bin/env python3
"""
경제 뉴스 수집 메인 스크립트
- RSS/API 소스에서 데이터 수집
- 중복 제거, 카테고리 분류, 요약 생성
- JSON 파일로 저장
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
import feedparser
import requests
from dateutil import parser as date_parser
from deep_translator import GoogleTranslator
import re
from bs4 import BeautifulSoup

def clean_html(raw_html):
    """HTML tags remover (using BeautifulSoup and regex fallback)"""
    if not raw_html:
        return ""
    try:
        # First try BeautifulSoup for real HTML
        soup = BeautifulSoup(raw_html, "html.parser")
        text = soup.get_text(separator=' ', strip=True)
        
        # If still contains HTML-like patterns (escaped or text), use regex
        if '<' in text or '&lt;' in text:
            # Remove escaped HTML entities
            text = re.sub(r'&lt;.*?&gt;', '', text)
            # Remove any remaining < > patterns
            text = re.sub(r'<[^>]+>', '', text)
        
        return text.strip()
    except:
        # Fallback to regex if BS4 fails
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', raw_html).strip()

BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "scripts" / "config"
DATA_DIR = BASE_DIR / "data"
ARCHIVE_DIR = DATA_DIR / "archive"

# 디렉토리 생성
DATA_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)


def load_json(filepath):
    """JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, filepath):
    """JSON 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_id(url):
    """URL로부터 고유 ID 생성 (SHA-256)"""
    return hashlib.sha256(url.encode('utf-8')).hexdigest()[:16]


def translate_text(text, target='ko'):
    """텍스트 번역 (영어 -> 한국어)"""
    if not text or len(text) < 2:
        return text
    
    try:
        # 한글이 포함되어 있으면 번역 스킵
        if any(ord(c) > 128 for c in text):
            return text
            
        translator = GoogleTranslator(source='auto', target=target)
        return translator.translate(text)
    except Exception as e:
        print(f"  Translation error: {e}")
        return text


def fetch_rss(source):
    """RSS 피드 수집 (User-Agent 헤더 추가)"""
    try:
        # User-Agent 헤더 추가하여 요청
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # requests로 먼저 가져오기 (봇 차단 방지)
        response = requests.get(source['rss_url'], headers=headers, timeout=10)
        response.raise_for_status()
        
        # feedparser로 파싱
        feed = feedparser.parse(response.content)
        items = []
        
        print(f"  - {source['name']}: {len(feed.entries)} items found")
        
        for entry in feed.entries[:10]:  # 최근 10개만
            # 발행일 파싱
            published = None
            if hasattr(entry, 'published'):
                try:
                    published = date_parser.parse(entry.published)
                except:
                    pass
            
            if not published and hasattr(entry, 'updated'):
                try:
                    published = date_parser.parse(entry.updated)
                except:
                    pass
            
            # 24시간 이내 항목만 (테스트를 위해 주석 처리하거나 시간 늘림)
            # if published and (datetime.now(published.tzinfo) - published).days > 1:
            #     continue
            
            title = entry.title if hasattr(entry, 'title') else ''
            link = entry.link if hasattr(entry, 'link') else ''
            summary = entry.summary if hasattr(entry, 'summary') else ''
            
            # 번역 (영문 소스인 경우)
            if source['language'] != 'ko':
                title = translate_text(title)
                if summary:
                    summary = translate_text(summary[:200])
            
            item = {
                'url': link,
                'title': title,
                'summary_source': summary[:200] if summary else '',
                'published': published.isoformat() if published else datetime.now().isoformat()
            }
            
            if item['url'] and item['title']:
                items.append(item)
        
        return items
    except Exception as e:
        print(f"Error fetching {source['name']}: {e}")
        return []


def classify_category(title, summary, categories):
    """키워드 기반 카테고리 자동 분류"""
    title_lower = title.lower()
    summary_lower = summary.lower() if summary else ''
    combined = title_lower + ' ' + summary_lower
    
    best_match = '기타'
    best_score = 0
    
    for cat_name, cat_info in categories['categories'].items():
        score = 0
        for keyword in cat_info['keywords']:
            if keyword.lower() in combined:
                score += cat_info['priority']
        
        if score > best_score:
            best_score = score
            best_match = cat_name
    
    return best_match


def generate_auto_summary(title, source_summary):
    """자체 요약 생성 (Safe Mode: 길이 제한 및 HTML 제거)"""
    # 1. HTML 태그 제거
    clean_summary = clean_html(source_summary)
    
    # 2. 길이 제한 (최대 150자)
    if len(clean_summary) > 150:
        clean_summary = clean_summary[:150]
        # 마지막 공백을 찾아서 자연스럽게 자름
        last_space = clean_summary.rfind(' ')
        if last_space > 100:
            clean_summary = clean_summary[:last_space]
        clean_summary += '...'
    
    # 3. 내용이 없으면 제목 사용
    if not clean_summary:
        clean_summary = title
    
    return clean_summary


def calculate_relevance(item, category):
    """관련도 점수 계산 (간단한 휴리스틱)"""
    score = 50  # 기본 점수
    
    # 소스 타입에 따라 가중치
    if item['source']['type'] == 'official':
        score += 20
    
    # 카테고리별 가중치
    priority_categories = ['금리', '거시경제', '정책']
    if category in priority_categories:
        score += 15
    
    # 최근성 (발행 시간이 최근일수록 높음)
    if item['published_at']:
        try:
            pub_time = datetime.fromisoformat(item['published_at'].replace('Z', '+00:00'))
            hours_ago = (datetime.now(pub_time.tzinfo) - pub_time).total_seconds() / 3600
            if hours_ago < 6:
                score += 20
            elif hours_ago < 12:
                score += 10
        except:
            pass
    
    return min(100, score)


def extract_tags(title, summary, category):
    """태그 추출 (간단한 키워드 추출)"""
    tags = [category]
    
    # 주요 키워드 리스트
    common_tags = {
        '한국은행': ['한국은행', 'BOK'],
        '금융위': ['금융위원회', '금융위'],
        '기재부': ['기획재정부', '기재부'],
        '연준': ['연준', 'FED', 'Federal Reserve'],
        '금리': ['금리', '기준금리'],
        '인플레이션': ['인플레이션', 'CPI', '물가'],
        '환율': ['환율', '달러', '원화'],
    }
    
    combined = (title + ' ' + (summary or '')).lower()
    
    for tag, keywords in common_tags.items():
        if any(kw.lower() in combined for kw in keywords):
            if tag not in tags:
                tags.append(tag)
    
    return tags[:5]  # 최대 5개


def main():
    """메인 수집 프로세스"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 수집 시작")
    
    # 설정 로드
    sources_config = load_json(CONFIG_DIR / "sources.json")
    categories_config = load_json(CONFIG_DIR / "categories.json")
    
    # 기존 데이터 로드 (있으면)
    latest_path = DATA_DIR / "feed-latest.json"
    existing_ids = set()
    
    if latest_path.exists():
        existing = load_json(latest_path)
        existing_ids = {item['id'] for item in existing.get('items', [])}
    
    all_items = []
    
    # 각 소스에서 수집
    for source in sources_config['sources']:
        if source['status'] != 'active':
            continue
        
        print(f"  수집 중: {source['name']}")
        items = fetch_rss(source)
        
        for item in items:
            item_id = generate_id(item['url'])
            
            # 중복 체크
            if item_id in existing_ids:
                continue
            
            category = classify_category(item['title'], item['summary_source'], categories_config)
            
            processed_item = {
                'id': item_id,
                'title': item['title'],
                'url': item['url'],
                'source': {
                    'domain': source['url'].split('/')[2],
                    'name': source['name'],
                    'type': source['copyright_status']
                },
                'published_at': item['published'],
                'collected_at': datetime.now().isoformat(),
                'category': category,
                'tags': extract_tags(item['title'], item['summary_source'], category),
                'country': source['country'],
                'summary': {
                    'auto': generate_auto_summary(item['title'], item['summary_source']),
                    'source': item['summary_source'][:100] if item['summary_source'] else ''
                },
                'relevance_score': 0,  # 나중에 계산
                'is_trending': False
            }
            
            # 관련도 점수 계산
            processed_item['relevance_score'] = calculate_relevance(processed_item, category)
            
            all_items.append(processed_item)
            existing_ids.add(item_id)
    
    print(f"  새 항목 {len(all_items)}개 수집")
    
    # 기존 데이터와 병합 (48시간 이내만 유지)
    if latest_path.exists():
        existing = load_json(latest_path)
        cutoff = datetime.now() - timedelta(hours=48)
        
        for item in existing.get('items', []):
            if item['id'] not in existing_ids:
                continue
            
            try:
                pub_time = datetime.fromisoformat(item['published_at'].replace('Z', '+00:00'))
                if pub_time > cutoff:
                    all_items.append(item)
            except:
                pass
    
    # 관련도 순으로 정렬
    all_items.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    # feed-latest.json 저장
    feed_latest = {
        'generated_at': datetime.now().isoformat(),
        'version': '1.0',
        'total_items': len(all_items),
        'items': all_items
    }
    
    save_json(feed_latest, latest_path)
    print(f"  저장 완료: feed-latest.json ({len(all_items)}개)")
    
    # trending.json 생성 (최근 6시간)
    cutoff_6h = datetime.now() - timedelta(hours=6)
    recent_items = []
    
    for item in all_items:
        try:
            pub_time = datetime.fromisoformat(item['published_at'].replace('Z', '+00:00'))
            if pub_time > cutoff_6h:
                item['is_trending'] = True
                recent_items.append(item)
        except:
            pass
    
    trending = {
        'generated_at': datetime.now().isoformat(),
        'period': {
            'from': cutoff_6h.isoformat(),
            'to': datetime.now().isoformat()
        },
        'top_items': [item['id'] for item in recent_items[:20]]
    }
    
    save_json(trending, DATA_DIR / "trending.json")
    print(f"  저장 완료: trending.json ({len(recent_items)}개)")
    
    # 아카이브 (선택적)
    archive_filename = f"feed-{datetime.now().strftime('%Y%m%d-%H')}.json"
    save_json(feed_latest, ARCHIVE_DIR / archive_filename)
    print(f"  아카이브: {archive_filename}")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 수집 완료\n")


if __name__ == '__main__':
    main()
