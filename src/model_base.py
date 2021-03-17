from src import db


class ModelBase(db.Model):
    __abstract__ = True

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_db_no_commit(self):
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
