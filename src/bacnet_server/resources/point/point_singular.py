from flask_restful import abort, marshal_with

from src import db
# from src.modbus.interfaces.point.points import ModbusDataType, ModbusPointType, ModbusDataEndian
# from src.modbus.models.point import ModbusPointModel
# from src.modbus.models.point_store import ModbusPointStoreModel
# from src.modbus.resources.mod_fields import point_fields
# from src.modbus.resources.point.point_base import ModbusPointBase
from src.bacnet_server.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian
from src.bacnet_server.models.point import ModbusPointModel
from src.bacnet_server.models.point_store import ModbusPointStoreModel
from src.bacnet_server.resources.mod_fields import point_fields
from src.bacnet_server.resources.point.point_base import ModbusPointBase
from src.bacnet_server.utils.model_utils import ModelUtils


class ModbusPointSingular(ModbusPointBase):
    """
    It returns point with point_store object value, which has the current values of point_store for that particular
    point with last not null value and value_array
    """

    def get(self, uuid):
        point = db.session \
            .query(ModbusPointModel, ModbusPointStoreModel) \
            .select_from(ModbusPointModel) \
            .filter_by(uuid=uuid) \
            .join(ModbusPointStoreModel, isouter=True) \
            .order_by(ModbusPointStoreModel.id.desc()) \
            .first()
        db.session.commit()
        if not point:
            abort(404, message=f'Modbus Point not found')

        return {**ModelUtils.row2dict(point[0]), "point_store": self.create_point_store(point[1])}, 200

    @marshal_with(point_fields)
    def put(self, uuid):
        data = ModbusPointSingular.parser.parse_args()
        point = ModbusPointModel.find_by_uuid(uuid)
        if point is None:
            return self.add_point(data, uuid)
        try:
            if data.type:
                data.type = ModbusPointType.__members__.get(data.type)
            if data.data_type:
                data.data_type = ModbusDataType.__members__.get(data.data_type)
            if data.data_endian:
                data.data_endian = ModbusDataEndian.__members__.get(data.data_endian)
            ModbusPointModel.filter_by_uuid(uuid).update(data)
            ModbusPointModel.commit()
            return ModbusPointModel.find_by_uuid(uuid)
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if point:
            point.delete_from_db()
        return '', 204
