from app import db
from models import File, Bibliography


def get_user_bibliographies(username):
    bibliographies = Bibliography.query.filter_by(owner=username).all()
    return bibliographies


def get_bibliography_files(bibliography_id):
    bibliography = Bibliography.query.filter_by(id=bibliography_id).first()
    return bibliography.files


def add_bibliography(bibliography):
    if bibliography is not None:
        db.session.add(bibliography)
        db.session.commit()


def edit_bibliography(bibliography_id, bibliography_new):
    bibliography = Bibliography.query.filter_by(id=bibliography_id).first()
    bibliography.name = bibliography_new.name
    bibliography.author = bibliography_new.author
    bibliography.date = bibliography_new.date
    bibliography.owner = bibliography_new.owner
    bibliography.publication_date = bibliography_new.publication_date
    db.session.commit()


def delete_bibliography(bibliography_id):
    bibliography = Bibliography.query.filter_by(id=bibliography_id).first()
    if bibliography is not None:
        db.session.delete(bibliography)
        db.session.commit()


def get_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file is not None:
        return file


def upload_file(file):
    if file is not None:
        db.session.add(file)
        db.session.commit()


def delete_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file is not None:
        db.session.delete(file)
        db.session.commit()
