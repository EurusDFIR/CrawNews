from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable = False,unique=True)
    url = db.Column(db.String(255), nullable = False)

    news = db.relationship('News', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.subject}'

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'url': self.url
        }    
    

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tieude = db.Column(db.String(255), nullable=False)
    noidung = db.Column(db.Text, nullable=True) # Content
    hinhanh = db.Column(db.String(255), nullable=True) 
    linkgoc = db.Column(db.String(255), nullable=False, unique=True) 
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'<News {self.tieude[:30]}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tieude': self.tieude,
            'noidung': self.noidung,
            'hinhanh': self.hinhanh,
            'linkgoc': self.linkgoc,
            'cat_id': self.cat_id
        }