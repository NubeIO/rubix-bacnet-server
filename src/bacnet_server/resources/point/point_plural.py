import uuid
from flask_restful import marshal_with
from sqlalchemy import func
from src.bacnet_server.models.point import BACnetPointModel
from src.bacnet_server.models.point_store import BACnetPointStoreModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase
from src.bacnet_server.utils.model_utils import ModelUtils


class BACnetPointPlural(BACnetPointBase):
    def get(self):
        from src import db
        partition_table = db.session.query(BACnetPointStoreModel, func.rank()
                                           .over(order_by=BACnetPointStoreModel.ts.desc(),
                                                 partition_by=BACnetPointStoreModel.point_uuid)
                                           .label('rank')).subquery()

        filtered_partition_table = db.session.query(partition_table).filter(partition_table.c.rank == 1).subquery()
        joined_table = db.session \
            .query(BACnetPointModel, filtered_partition_table) \
            .select_from(BACnetPointModel) \
            .join(filtered_partition_table, BACnetPointModel.uuid == filtered_partition_table.c.point_uuid,
                  isouter=True).all()
        db.session.commit()
        serialized_output = []
        for row in joined_table:
            serialized_output.append({**ModelUtils.row2dict(row[0]), "point_store": self.create_point_store(row)})
        return serialized_output, 200

    @marshal_with(point_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = BACnetPointPlural.parser.parse_args()
        return self.add_point(data, _uuid)
