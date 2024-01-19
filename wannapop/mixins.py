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
    
    @classmethod
    def get_all_with(cls, join_cls):
        return cls.db_query_with(join_cls).order_by(cls.id.asc()).all()
    
    @classmethod
    def get_all_with_outerjoin(cls, outer_join_cls, **kwargs):
        return db.session.query(outer_join_cls).filter_by(**kwargs).one_or_none()
    
    
