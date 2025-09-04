from datetime import timedelta
from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
    PushSource,
    RequestSource,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Int64, String

# Mendefinisikan Entitas
user = Entity(name="user", join_keys=["user_id"])
item = Entity(name="item", join_keys=["item_id"])

# Sumber data offline dari data lake (Parquet)
user_events_source = FileSource(
    name="user_events_source",
    path="s3://silver/user_events.parquet", # Ganti dengan path MinIO Anda
    s3_endpoint_override="http://localhost:9000", # Endpoint MinIO
    timestamp_field="event_timestamp",
)

# Feature View untuk Agregat Pengguna
user_aggregate_features_view = FeatureView(
    name="user_aggregate_features",
    entities=[user],
    ttl=timedelta(days=7),
    schema=[
        Field(name="total_purchases_7d", dtype=Int64),
        Field(name="distinct_items_viewed_7d", dtype=Int64),
    ],
    online=True,
    source=user_events_source,
    tags={"team": "recommendation"},
)

# Sumber data untuk metadata item
item_metadata_source = FileSource(
    name="item_metadata_source",
    path="s3://silver/item_metadata.parquet",
    s3_endpoint_override="http://localhost:9000",
)

# Feature View untuk Metadata Item
item_features_view = FeatureView(
    name="item_features",
    entities=[item],
    ttl=timedelta(days=30),
    schema=,
    online=True,
    source=item_metadata_source,
    tags={"team": "catalog"},
)