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
                    "schedule": [
                        {
                            "startDatetime": "2025-05-02T14:00:00+08:00",
                            "endDatetime": "2025-05-02T15:00:00+08:00",
                            "workshops": [
                                {
                                    "id": "57cf801e-3675-473b-b524-b125503c9f76",
                                    "title": "1-1-1",
                                    "description": "第1天\r\n第1時段\r\n第1場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                },
                                {
                                    "id": "fd6ab0a9-bfc7-4c98-b092-1552a1e1d4d3",
                                    "title": "1-1-2",
                                    "description": "第1天\r\n第1時段\r\n第2場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                }
                            ]
                        },
                        {
                            "startDatetime": "2025-05-02T15:20:00+08:00",
                            "endDatetime": "2025-05-02T16:40:00+08:00",
                            "workshops": [
                                {
                                    "id": "89a95941-c91a-4222-9981-d871c7acaee3",
                                    "title": "1-2-1",
                                    "description": "第1天\r\n第2時段\r\n第1場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                },
                                {
                                    "id": "d1b0e58f-7a34-42b6-a24f-63b299b1942f",
                                    "title": "1-2-2",
                                    "description": "第1天\r\n第2時段\r\n第2場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                },
                                {
                                    "id": "20dcc21c-f13b-4919-a021-7bdef7213beb",
                                    "title": "1-2-3",
                                    "description": "第1天\r\n第2時段\r\n第3場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                }
                            ]
                        },
                        {
                            "startDatetime": "2025-05-03T14:00:00+08:00",
                            "endDatetime": "2025-05-03T15:00:00+08:00",
                            "workshops": [
                                {
                                    "id": "a93c08f5-3ced-4f70-a81c-3c3cb2db2bfe",
                                    "title": "2-1-1",
                                    "description": "第2天\r\n第1時段\r\n第1場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                },
                                {
                                    "id": "14c12bf3-fe95-45c1-9578-e3212bdd5f9d",
                                    "title": "2-1-2",
                                    "description": "第2天\r\n第1時段\r\n第2場",
                                    "location": {
                                        "id": "191d42e9-c8e4-425b-86f1-3b64d12c7a9c",
                                        "name": "台大體育館 401 教室",
                                        "address": "",
                                        "floor": "4",
                                        "room_number": "401",
                                        "image_url": None
                                    }
                                }
                            ]
                        },
                        {
                            "startDatetime": "2025-05-03T15:20:00+08:00",
                            "endDatetime": "2025-05-03T16:40:00+08:00",
                            "workshops": [
                                {
                                    "id": "8c3cff19-76ec-4270-9a0c-ca21f07f470e",
                                    "title": "2-2-1",
                                    "description": "第2天\r\n第2時段\r\n第1場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                },
                                {
                                    "id": "cae846d9-687f-4386-b084-d760c1687c33",
                                    "title": "2-2-2",
                                    "description": "第2天\r\n第2時段\r\n第2場",
                                    "location": {
                                        "id": "2fabbd88-f24c-48a6-901d-b9d6a4340558",
                                        "name": "Test",
                                        "address": "",
                                        "floor": None,
                                        "room_number": None,
                                        "image_url": None
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
}
