# Rusty results

[![Docs](https://img.shields.io/badge/docs-read-green)](https://danielsanchezq.github.io/rusty_results/)
[![Run Python Tests](https://github.com/danielSanchezQ/rusty_results/actions/workflows/ci.yml/badge.svg)](https://github.com/danielSanchezQ/rusty_results/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/danielSanchezQ/rusty_results/branch/main/graph/badge.svg?token=6A8TEB63V0)](https://codecov.io/gh/danielSanchezQ/rusty_results)
[![Downloads](https://pepy.tech/badge/rusty-results)](https://pepy.tech/project/rusty-results)
[![GitHub release](https://img.shields.io/badge/github-repository-blue)](https://github.com/danielsanchezq/rusty_results)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/danielsanchezq/rusty_results)


Rusty results is a Python library for dealing with result and optional types inspired by rust standard library.

### Pattern matching ready!

It exposes two main types with two constructors each one. 


### Result
`Result[T, E]` is the type used for returning and propagating errors. It is based in the variants, `Ok(T)`, representing 
success and containing a value, and `Err(E)`, representing error and containing an error value.


### Option

`Option[T]` represents an optional value: every `Option` is either `Some(T)` that contains a value, or `Empty()` that does not.
Option types have a number of uses:
* Initial values
* Return values for functions that are not defined over the entire input range (partial function)
* Return value for otherwise reporting simple errors, where Empty is returned on error.
* Optional struct fields
* Optional function arguments


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rusty results.

```bash
pip install rusty_results
```

## Usage

```python
from rusty_results import Option, Some, Empty, Result, Ok, Err, UnwrapException
```

## Examples

```python
"""
Example on pattern matching handling of Result
"""

from rusty_results import Result, Ok, Err


def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("Cannot divide by zero")
    return Ok(a // b)


if __name__ == "__main__":
    values = [(10, 0), (10, 5)]
    for a, b in values:
        divide_result = divide(a, b)
        match divide_result:
            case Ok(value):
                print(f"{a} // {b} == {value}")
            case Err(e):
                print(e)
```

You can find more examples in the `/examples` folder.

## Pydantic
Option and Result are fully compatible with [pydantic](https://pydantic-docs.helpmanual.io/) models

```python
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

```

prints out:

```shell
{"name": {"Some": "Link"}, "phone": {}}
name=Some(Some='Link') phone=Empty()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)