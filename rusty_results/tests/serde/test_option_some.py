import pydantic
import pytest

from rusty_results import Option, Some
import json


class TestModel(pydantic.BaseModel):
    optional_value: Option[str]


TEST_MODEL_SERIALIZED = '{"optional_value": {"Value": "foo bar"}}'


def test_serialize():
    model = TestModel(optional_value=Some("foo bar"))
    assert model.json() == TEST_MODEL_SERIALIZED


def test_deserialize():
    model = TestModel(**json.loads(TEST_MODEL_SERIALIZED))
    assert model == TestModel(optional_value=Some("foo bar"))


def test_deserialize_fails():
    wrong_values = [
        10,
        {"foo": 10},
    ]
    with pytest.raises(pydantic.ValidationError):
        for value in wrong_values:
            TestModel(foo=value)