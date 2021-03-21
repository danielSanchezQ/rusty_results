import pydantic
import pytest
from rusty_results import Result, Ok
import json


class Model(pydantic.BaseModel):
    result_value: Result[int, str]


TEST_MODEL_SERIALIZED = '{"result_value": {"Value": 10}}'


def test_serialize():
    model = Model(result_value=Ok(10))
    assert model.json() == TEST_MODEL_SERIALIZED


def test_deserialize():
    model = Model(**json.loads(TEST_MODEL_SERIALIZED))
    assert model == Model(result_value=Ok(10))


def test_deserialize_fails():
    wrong_values = [
        10,
        {"foo": 10},
    ]
    with pytest.raises(pydantic.ValidationError):
        for value in wrong_values:
            Model(foo=value)