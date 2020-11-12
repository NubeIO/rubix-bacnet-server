def update_point_store(point_uuid, present_value):
    from src.bacnet_server.models.model_point_store import BACnetPointStoreModel
    point_store = BACnetPointStoreModel(point_uuid=point_uuid, present_value=present_value)
    point_store.update()