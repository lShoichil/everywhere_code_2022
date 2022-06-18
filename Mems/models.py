from Mems import db


class Mems(db.Model):
    __tablename__ = "mems"
    id = db.Column(db.Integer, primary_key=True)
    vk_links = db.Column(db.String(300))
    vk_id = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    url_image = db.Column(db.String(300))
