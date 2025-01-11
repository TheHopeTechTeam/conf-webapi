"""
Workshop response examples
"""
import uuid

from starlette import status

WORKSHOP_LIST = {
    status.HTTP_200_OK: {
        "description": "Get workshop list",
        "content": {
            "application/json": {
                "example": {
                    "20250502": {
                        "1400": [
                            {
                                "id": uuid.uuid4(),
                                "title": "Workshop 1",
                                "description": "Workshop 1 description",
                                "location": {
                                    "id": uuid.uuid4(),
                                    "name": "2F 201 Room",
                                    "address": None,
                                    "floor": 2,
                                    "room_number": "201",
                                    "image_url": None
                                },
                                "start_datetime": "2025-05-02T14:00:00+08:00",
                                "end_datetime": "2025-05-02T15:20:00+08:00",
                            }
                        ],
                        "1520": [
                            {
                                "id": uuid.uuid4(),
                                "title": "Workshop 2",
                                "description": "Workshop 2 description",
                                "location": {
                                    "id": uuid.uuid4(),
                                    "name": "2F 202 Room",
                                    "address": None,
                                    "floor": 2,
                                    "room_number": "202",
                                    "image_url": None
                                },
                                "start_datetime": "2025-05-02T15:20:00+08:00",
                                "end_datetime": "2025-05-02T16:40:00+08:00",
                            }
                        ]
                    },
                    "20250503": {
                        "1400": [
                            {
                                "id": uuid.uuid4(),
                                "title": "Workshop 3",
                                "description": "Workshop 3 description",
                                "location": {
                                    "id": uuid.uuid4(),
                                    "name": "2F 203 Room",
                                    "address": None,
                                    "floor": 2,
                                    "room_number": "203",
                                    "image_url": None
                                },
                                "start_datetime": "2025-05-03T14:00:00+08:00",
                                "end_datetime": "2025-05-03T15:20:00+08:00",
                            }
                        ],
                        "1520": [
                            {
                                "id": uuid.uuid4(),
                                "title": "Workshop 4",
                                "description": "Workshop 4 description",
                                "location": {
                                    "id": uuid.uuid4(),
                                    "name": "2F 204 Room",
                                    "address": None,
                                    "floor": 2,
                                    "room_number": "204",
                                    "image_url": None
                                },
                                "start_datetime": "2025-05-03T15:20:00+08:00",
                                "end_datetime": "2025-05-03T16:40:00+08:00",
                            }
                        ]
                    }
                }
            }
        }
    }
}
