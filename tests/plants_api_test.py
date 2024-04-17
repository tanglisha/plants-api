import json
from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient
from plants_api.main import app
from plants_api.plants.models import PlantListItem
from plants_api.plants.models import PlantRead
from pytest import fixture
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from .factories import PlantCreateFactory
from .factories import PlantFactory

client = TestClient(app)


@fixture(autouse=True)
def db():
    """Fake database

    Override methods from this to change the responses from the database

    == Example ==

    Let's say we're calling the database using db.exec(some query).all()
    We need a `return_value` each time a method is called, so we need both
        ret = exec.return_value
        and then from that response
        ret.all.return_value = blah

    Like so:

    def test(db):
        db.exec.return_value.all.return_value = []
    """
    with patch(
        "plants_api.database.Session",
        name="Mock Session",
        spec_set=Session,
    ) as fake_session:
        fake_session.return_value.__enter__.return_value = fake_session
        yield fake_session


class TestPlant:
    class TestCreate:
        """Create a plant

        pk values are created in the server, not passed in
        """

        def test_basic_creation(self):
            request_body = PlantCreateFactory.build()

            subject = client.post(
                url="/plants",
                json=json.loads(request_body.model_dump_json()),
            )

            assert subject.status_code == 200

            assert subject.json().get("pk") is not None
            assert json_equal_minus_keys(
                subject.json(),
                request_body.model_dump_json(),
                "pk",
            )

    class TestUpdate:
        """Create a plant

        pk values are created in the server, not passed in
        """

        def test_plant_not_found(self, db):
            db.get_one.side_effect = NoResultFound()

            subject = client.patch(
                url=f"/plants/{uuid4()}",
                json={"latin_name": "should fail"},
            )

            assert subject.status_code == HTTPStatus.NOT_FOUND
            assert subject.json() == {"detail": "plant not found"}

        def test_name_update(self, db):
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

            assert subject.status_code == HTTPStatus.OK
            actual_response = PlantRead.model_validate(subject.json())
            assert actual_response == expected_response

    class TestList:
        def test_returns_list(self, db):
            db_response = PlantFactory.build_batch(2)
            expected_result = []
            for item in db_response:
                json_str = PlantListItem.model_validate(item).model_dump_json()
                expected_result.append(json.loads(json_str))

            db.exec.return_value.all.return_value = db_response

            subject = client.get(
                url="/plants",
            )

            assert subject.status_code == HTTPStatus.OK
            assert subject.json() == expected_result

    class TestRead:
        def test_returns_item(self, db):
            response = PlantFactory.build()
            db.get_one.return_value = response
            url = f"/plants/{response.pk}"

            subject = client.get(
                url=url,
            )

            assert subject.status_code == HTTPStatus.OK
            assert subject.json() == json.loads(
                PlantRead.model_validate(response).model_dump_json(),
            )


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
        if key in json1_dict.keys():
            json1_dict.pop(key)
        if key in json2_dict.keys():
            json2_dict.pop(key)

    return json1_dict == json2_dict
