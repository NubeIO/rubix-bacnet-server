from src import db


class ModelBase(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        ModelBase.save_to_db_no_commit(self)
        db.session.commit()

    def save_to_db_no_commit(self):
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
