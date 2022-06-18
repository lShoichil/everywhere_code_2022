from Mems import db


class Mems(db.Model):
    __tablename__ = "mems"
    id = db.Column(db.Integer, primary_key=True)
    vk_links = db.Column(db.String(300))
    vk_id = db.Column(db.Integer)
    likes_parse = db.Column(db.Integer)
    likes_count = db.Column(db.Integer)  # для 2,3 заданий
    url_image = db.Column(db.String(300))
    promote = db.Column(db.Boolean)  # для 3
