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


