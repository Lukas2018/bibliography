from datetime import datetime
from app import db


class Bibliography(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    author = db.Column(db.String(64), index=True)
    date = db.Column(db.DateTime, index=True)
    owner = db.Column(db.String(64), index=True)
    publication_date = db.Column(db.DateTime, index=True)
    files = db.relationship('File', backref='bibliography', lazy='dynamic')

    def to_dict(self):
        dict = {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "date": str(self.date),
            "owner": self.owner,
            "publication_date": str(self.publication_date)
        }
        return dict


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(140))
    data = db.Column(db.LargeBinary)
    bibliography_id = db.Column(db.Integer, db.ForeignKey('bibliography.id'))

    def to_dict(self):
        dict = {
            "id": self.id,
            "filename": self.filename,
            "bibliography_id": self.bibliography_id
        }
        return dict
