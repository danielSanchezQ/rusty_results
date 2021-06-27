import pydantic
import pytest
from rusty_results import Option, Empty
import json


class Model(pydantic.BaseModel):
    optional_value: Option[str]


TEST_MODEL_SERIALIZED = '{"optional_value": {}}'


def test_serialize():
    model = Model(optional_value=Empty())
    assert model.json() == TEST_MODEL_SERIALIZED


def test_deserialize():
    model = Model(**json.loads(TEST_MODEL_SERIALIZED))
    assert model == Model(optional_value=Empty())


def test_deserialize_fails():
    wrong_values = [
        10,
        {"foo": 10},
    ]
    with pytest.raises(pydantic.ValidationError):
        for value in wrong_values:
            Model(foo=value)


def test_deserialize_wrong_number_of_values():
    with pytest.raises(pydantic.ValidationError):
        Model(optional_value={"Empty": "foo", "Bar": "Baz"})


def test_deserialize_inner_is_none():
    with pytest.raises(pydantic.ValidationError):
        Model(optional_value={"Empty": None})
