from app.entity.OffersEntity import OffersEntity
import pydantic

o = OffersEntity(
    business_id=1,
    title="test",
    original_price=10,
    discounted_price=5,
    pickup_start_time="2026-08-23T21:43:00.000Z",
    pickup_end_time="2026-08-23T06:43:00.000Z"
)
print(o.pickup_end_time.tzinfo)
