from rusty_results import Option, Some, Empty
from rusty_results import early_return


@early_return
def fail_on_operation() -> Option[int]:
    value1 = Some(10)
    value2 = Empty()
    return Some(~value1 + ~value2)


def success_on_operation() -> Option[int]:
    value1 = Some(10)
    value2 = Some(10)
    return Some(~value1 + ~value2)


if __name__ == "__main__":
    print("Success so it return value: ", success_on_operation())
    print("Fail so it return Empty: ", fail_on_operation())
