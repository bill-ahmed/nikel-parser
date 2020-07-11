from schema import Schema, Or

from validations.schemas.base_schema import BaseSchema


class ParkingSchema(BaseSchema):
    SCHEMA = Schema([{
        'id': str,
        'name': str,
        'alias': Or(str, None),
        'building_id': Or(str, None),
        'description': Or(str, None),
        'campus': Or(*BaseSchema.VALID_CAMPUSES),
        'address': Or(str, None),
        'coordinates': {
            'latitude': float,
            'longitude': float
        },
        'last_updated': str
    }])
