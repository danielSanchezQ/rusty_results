import pydantic
from rusty_results import Option, Some, Empty


class MyData(pydantic.BaseModel):
    name: Option[str]
    phone: Option[int]


if __name__ == "__main__":
    import json
    # serialize to json
    json_data = MyData(name=Some("Link"), phone=Empty()).json()
    print(json_data)
    # deserialize json data
    data = MyData(**json.loads(json_data))
    print(data)
