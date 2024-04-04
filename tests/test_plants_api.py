import json
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient
from plants_api.database import db as real_db
from plants_api.database import SessionLocal
from plants_api.main import app
from plants_api.plants.models import PlantRead
from pytest import fixture

from .factories import PlantCreateFactory
from .factories import PlantFactory
from .factories import PlantReadFactory

client = TestClient(app)

db = MagicMock(name="fake database")


@fixture(autouse=True)
def fake_db():
    """Override the database connection

    returns a MagicMock in place of the session
    """
    with patch.object(
        SessionLocal,
        "_create_session",
        name="fake session",
    ) as fake_engine:
        yield fake_engine


def override_database():
    """Override the Depends(db) functionality

    returns a MagicMock
    """
    yield db


app.dependency_overrides[real_db] = override_database


class TestPlant:
    class TestCreate:
        """Create a plant

        pk values are created in the server, not passed in
        """

        def test_basic_creation(self, fake_db):
            request_body = PlantCreateFactory.build()
            response = PlantRead.model_validate(
                request_body.model_dump(),
                update={"pk": uuid4()},
            )

            fake_db.refresh.side_effect = response

            subject = client.post(
                url="/plants",
                json=json.loads(request_body.model_dump_json()),
            )

            assert subject.status_code == 200
            assert json_equal_minus_keys(
                subject.json(),
                response.model_dump_json(),
                "pk",
            )

    class TestUpdate:
        """Create a plant

        pk values are created in the server, not passed in
        """

        def test_name_update(self):
            plant_id = str(uuid4())
            new_name = "updated name"

            request_body = PlantFactory.build()
            db_refresh = PlantRead.model_validate(request_body)
            expected_response = db_refresh.model_copy()
            expected_response.latin_name = new_name

            db.get_one.return_value = request_body
            db.refresh.side_effect = db_refresh

            subject = client.patch(
                url=f"/plants/{plant_id}",
                json={"latin_name": new_name},
            )

            assert subject.status_code == 200
            actual_response = PlantRead.model_validate(subject.json())
            assert actual_response == expected_response

    class TestList:
        def test_returns_list(self):
            response = [PlantReadFactory.build(), PlantReadFactory.build()]
            expected_result = []
            for item in [json.loads(x.model_dump_json()) for x in response]:
                expected_result.append(
                    {"pk": item.get("pk"), "latin_name": item.get("latin_name")},
                )
            db.execute.return_value.all.return_value = response

            subject = client.get(
                url="/plants",
            )

            assert subject.status_code == 200
            assert subject.json() == expected_result

    class TestRead:
        def test_returns_item(self):
            response = PlantReadFactory.build()
            db.execute.return_value.first.return_value = response
            url = f"/plants/{response.pk}"

            subject = client.get(
                url=url,
            )

            assert subject.status_code == 200
            assert subject.json() == json.loads(response.model_dump_json())


def json_equal_minus_keys(json1: str | dict, json2: str | dict, *keys: str) -> bool:
    if isinstance(json1, str):
        json1_dict = json.loads(json1)
    else:
        json1_dict = json1

    if isinstance(json2, str):
        json2_dict = json.loads(json2)
    else:
        json2_dict = json2

    for key in keys:
        json1_dict.pop(key)
        json2_dict.pop(key)

    return json1_dict == json2_dict
