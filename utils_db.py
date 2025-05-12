# lab5_project/utils_db.py
import json
import os
import requests
from bs4 import BeautifulSoup
from models import db, News, Category # Use absolute import instead of relative import

JSON_FILE_DIR = "json_file"
NEWS_JSON_PATH = os.path.join(JSON_FILE_DIR, "news.json")
CATEGORY_JSON_PATH = os.path.join(JSON_FILE_DIR, "category.json")


if not os.path.exists(JSON_FILE_DIR):
    os.makedirs(JSON_FILE_DIR)

def get_news_to_json():
    """Loads all news from the database and writes to news.json."""
    all_news_objects = News.query.all()
    data = [news.to_dict() for news in all_news_objects]
    with open(NEWS_JSON_PATH, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Successfully wrote {len(data)} news articles to {NEWS_JSON_PATH}")
    return data 

def read_news_from_json(keywords=None):
    """
    Reads news from news.json.
    If keywords are provided, filters news where the title (tieude) contains the keywords (case-insensitive).
    """
 
    if not os.path.exists(NEWS_JSON_PATH):
        print(f"{NEWS_JSON_PATH} not found. Attempting to generate it.")
        get_news_to_json() 

    try:
        with open(NEWS_JSON_PATH, "r", encoding="utf8") as f:
            news_list = json.load(f)
    except FileNotFoundError:
        print(f"Error: {NEWS_JSON_PATH} not found even after attempting to generate.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {NEWS_JSON_PATH}.")
        return []

    if keywords:
        keywords_lower = keywords.lower()
        filtered_news = [
            n for n in news_list
            if n.get("tieude") and keywords_lower in n["tieude"].lower()
        ]
        return filtered_news
    return news_list

def get_categories_to_json():
    """Loads all categories from the database and writes to category.json."""
    all_category_objects = Category.query.all()
    data = [cat.to_dict() for cat in all_category_objects]
    with open(CATEGORY_JSON_PATH, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Successfully wrote {len(data)} categories to {CATEGORY_JSON_PATH}")
    return data

def crawl_vnexpress_thoisu(max_articles=60):
    """Crawl tin tức Thời sự từ VnExpress và lưu vào DB."""
    url = "https://vnexpress.net/thoi-su"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select(".item-news")
    # Lấy category 'Thời sự' từ DB
    cat = Category.query.filter_by(subject="Thời sự").first()
    if not cat:
        cat = Category(subject="Thời sự", url=url)
        db.session.add(cat)
        db.session.commit()
    count = 0
    for item in articles:
        if count >= max_articles:
            break
        tieude_tag = item.select_one("h3.title-news a")
        if not tieude_tag:
            continue
        tieude = tieude_tag.get_text(strip=True)
        linkgoc = tieude_tag["href"]
        noidung = item.select_one("p.description")
        noidung = noidung.get_text(strip=True) if noidung else ""
        hinhanh_tag = item.select_one("img")
        hinhanh = hinhanh_tag["src"] if hinhanh_tag and hinhanh_tag.has_attr("src") else ""
        # Check trùng linkgoc
        if News.query.filter_by(linkgoc=linkgoc).first():
            continue
        news = News(tieude=tieude, noidung=noidung, hinhanh=hinhanh, linkgoc=linkgoc, cat_id=cat.id)
        db.session.add(news)
        count += 1
    db.session.commit()
    print(f"Đã crawl và lưu {count} bài báo Thời sự từ VnExpress.")

def crawl_vnexpress_tintuc(url, category_name, max_articles=10):
    """Crawl tin tức từ VnExpress theo URL và lưu vào DB."""
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select(".item-news")
   
    cat = Category.query.filter_by(subject=category_name).first()
    if not cat:
        cat = Category(subject=category_name, url=url)
        db.session.add(cat)
        db.session.commit()
    count = 0
    for item in articles:
        if count >= max_articles:
            break
        tieude_tag = item.select_one("h3.title-news a")
        if not tieude_tag:
            continue
        tieude = tieude_tag.get_text(strip=True)
        linkgoc = tieude_tag["href"]
        noidung = item.select_one("p.description")
        noidung = noidung.get_text(strip=True) if noidung else ""
        hinhanh_tag = item.select_one("img")
        hinhanh = hinhanh_tag["src"] if hinhanh_tag and hinhanh_tag.has_attr("src") else ""
        # Check trùng linkgoc
        if News.query.filter_by(linkgoc=linkgoc).first():
            continue
        news = News(tieude=tieude, noidung=noidung, hinhanh=hinhanh, linkgoc=linkgoc, cat_id=cat.id)
        db.session.add(news)
        count += 1
    db.session.commit()
    print(f"Đã crawl và lưu {count} bài báo từ {category_name} ({url}).")

# Hàm tổng hợp crawl nhiều nguồn
def crawl_multiple_sources():
    sources = [
        {"url": "https://vnexpress.net/thoi-su", "category_name": "Thời sự"},
        {"url": "https://vnexpress.net/the-thao", "category_name": "Thể thao"}
    ]
    for source in sources:
        crawl_vnexpress_tintuc(source["url"], source["category_name"])

