from . import db_manager as db

class BaseMixin():

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def remove(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            return False

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()
        
    @classmethod
    def get_filtered_by(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).one_or_none()
