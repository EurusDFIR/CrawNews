# lab5_project/app.py
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from config import Config
from models import db, News, Category 
import utils_db 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db) 


@app.cli.command("seed-db")
def seed_db_command():
    """Adds sample data to the database."""
    with app.app_context():
    
        cat1 = Category.query.filter_by(subject="Thời sự").first()
        if not cat1:
            cat1 = Category(subject="Thời sự", url="https://vnexpress.net/thoi-su")
            db.session.add(cat1)

        cat2 = Category.query.filter_by(subject="Thể thao").first()
        if not cat2:
            cat2 = Category(subject="Thể thao", url="https://vnexpress.net/the-thao")
            db.session.add(cat2)
        
        cat3 = Category.query.filter_by(subject="Công nghệ").first()
        if not cat3:
            cat3 = Category(subject="Công nghệ", url="https://dantri.com.vn/suc-manh-so") 
            db.session.add(cat3)

        db.session.commit()

        # Add News
        news_items = [
            News(tieude="Tin tức thời sự nóng hổi", noidung="Chi tiết...", hinhanh="img1.jpg", linkgoc="link1.html", category=cat1),
            News(tieude="Kết quả bóng đá Ngoại Hạng Anh", noidung="Chi tiết...", hinhanh="img2.jpg", linkgoc="link2.html", category=cat2),
            News(tieude="Công nghệ AI thay đổi thế giới", noidung="Chi tiết...", hinhanh="img3.jpg", linkgoc="link3.html", category=cat3),
            News(tieude="Một tin tức khác về thời sự", noidung="Nội dung khác...", hinhanh="img4.jpg", linkgoc="link4.html", category=cat1),
        ]

        for item_data in news_items:
           
            existing_news = News.query.filter_by(linkgoc=item_data.linkgoc).first()
            if not existing_news:
                db.session.add(item_data)
        
        db.session.commit()
        print("Database seeded with sample data!")
        
        # After seeding, update the JSON files
        utils_db.get_news_to_json()
        utils_db.get_categories_to_json()
        print("JSON files updated.")


@app.cli.command("crawl-news")
def crawl_news_command():
    """Crawl tin tức từ nhiều nguồn và lưu vào DB."""
    with app.app_context():
        import utils_db
        utils_db.crawl_multiple_sources()
        # Sau khi crawl, cập nhật lại file JSON
        utils_db.get_news_to_json()
        print("Đã cập nhật news.json sau khi crawl từ nhiều nguồn.")


# --- Routes ---
@app.route("/")
def index():
    """Endpoint for the home page (index.html)."""
    return render_template("index.html")

@app.route("/category", methods=["GET"])
def get_categories_route():
    """
    Endpoint for category page.
    Loads categories from DB, saves to JSON (as per lab structure), then renders.
    """
  
    categories_data = utils_db.get_categories_to_json()
    return render_template("category.html", data=categories_data)

@app.route("/news", methods=["GET"])
def render_news_route():
    """
    Endpoint for news page.
    Uses read_news_from_json (which might internally call get_news_to_json if file is missing).
    """
    keywords = request.args.get("keywords", None)
    
  

    news_data = utils_db.read_news_from_json(keywords=keywords)
    return render_template("news.html", data=news_data, current_keywords=keywords or "")


if __name__ == "__main__":
   
    with app.app_context():
      
        if not News.query.first(): 
            print("No news found in DB. Consider running 'flask seed-db'")
        else:
           
            print("Refreshing JSON files from DB...")
            utils_db.get_news_to_json()
            utils_db.get_categories_to_json()

    app.run(debug=True)