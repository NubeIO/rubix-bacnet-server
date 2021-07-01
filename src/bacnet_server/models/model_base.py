from sqlalchemy import desc, asc

from src import db


class ModelBase(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def find_by_pagination(cls, page: int, per_page: int, sort: str, sort_by: str):
        query = cls.query
        if sort or sort_by:
            if not sort_by:
                sort_by = cls.__table__.primary_key.columns.keys()[0]
            else:
                if sort_by not in cls.__table__.columns.keys():
                    raise ValueError(f"Does not exist sort_by{sort_by}")
            sort = desc(sort_by) if sort == "desc" else asc(sort_by)
            query = query.order_by(sort)
        return query.paginate(page=page, per_page=per_page, error_out=False)

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
