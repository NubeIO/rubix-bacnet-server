from threading import Thread

from mrb.mapper import api_to_topic_mapper
from mrb.message import HttpMethod, Response
from mrb.validator import is_valid

from src import db


def update_point_store(point_uuid: str, present_value: float, sync_to_ps: bool = True):
    from src.bacnet_server.models.model_point_store import BACnetPointStoreModel
    point_store = BACnetPointStoreModel(point_uuid=point_uuid, present_value=present_value)
    point_store.update()
    db.session.commit()
    Thread(target=_sync_to_ps, daemon=True,
           kwargs={'point_uuid': point_uuid, 'present_value': present_value, 'sync_to_ps': sync_to_ps}).start()


def _sync_to_ps(point_uuid: str, present_value: float, sync_to_ps: bool):
    if sync_to_ps:
        mapping: Response = api_to_topic_mapper(api=f"/api/gbp/mapping/bacnet/{point_uuid}",
                                                destination_identifier='ps',
                                                http_method=HttpMethod.GET)
        if is_valid(mapping):
            # TODO: upgrade sync logic
            api_to_topic_mapper(
                api=f"/api/generic/points_value/uuid/{mapping.content.get('generic_point_uuid')}",
                destination_identifier='ps',
                body={"priority_array": {"_16": present_value}},
                http_method=HttpMethod.PATCH)
