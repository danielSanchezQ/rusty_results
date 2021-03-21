import pydantic
import pytest
from rusty_results import Option, Empty
import json


class TestModel(pydantic.BaseModel):
    optional_value: Option[str]


TEST_MODEL_SERIALIZED = '{"optional_value": {}}'


def test_serialize():
    model = TestModel(optional_value=Empty())
    assert model.json() == TEST_MODEL_SERIALIZED


def test_deserialize():
    model = TestModel(**json.loads(TEST_MODEL_SERIALIZED))
    assert model == TestModel(optional_value=Empty())


def test_deserialize_fails():
    wrong_values = [
        10,
        {"foo": 10},
    ]
    with pytest.raises(pydantic.ValidationError):
        for value in wrong_values:
            TestModel(foo=value)