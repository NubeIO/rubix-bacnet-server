from flask_restful import abort, marshal_with

from src import db
from src.bacnet_server.interfaces.point.points import PointType
from src.bacnet_server.models.point import BACnetPointModel
from src.bacnet_server.models.point_store import BACnetPointStoreModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import BACnetPointBase
from src.bacnet_server.utils.model_utils import ModelUtils


class BACnetPointSingular(BACnetPointBase):
    """
    It returns point with point_store object value, which has the current values of point_store for that particular
    point with last not null value and value_array
    """

    def get(self, uuid):
        point = db.session \
            .query(BACnetPointModel, BACnetPointStoreModel) \
            .select_from(BACnetPointModel) \
            .filter_by(uuid=uuid) \
            .join(BACnetPointStoreModel, isouter=True) \
            .order_by(BACnetPointStoreModel.id.desc()) \
            .first()
        db.session.commit()
        if not point:
            abort(404, message=f'BACnet Point not found')

        return {**ModelUtils.row2dict(point[0]), "point_store": self.create_point_store(point[1])}, 200

    @marshal_with(point_fields)
    def put(self, uuid):
        data = BACnetPointSingular.parser.parse_args()
        point = BACnetPointModel.find_by_uuid(uuid)
        if point is None:
            return self.add_point(data, uuid)
        try:
            if data.object_type:
                data.object_type = PointType.__members__.get(data.object_type)
            BACnetPointModel.filter_by_uuid(uuid).update(data)
            BACnetPointModel.commit()
            return BACnetPointModel.find_by_uuid(uuid)
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, uuid):
        point = BACnetPointModel.find_by_uuid(uuid)
        if point:
            point.delete_from_db()
        return '', 204
