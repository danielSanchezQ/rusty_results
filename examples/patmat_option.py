"""
Example on pattern matching handling of Option
"""

from rusty_results import Option, Some, Empty


def find_index(l: [str], value: str) -> Option[int]:
    for i, e in enumerate(l):
        if e == value:
            return Some(i)
    return Empty()


if __name__ == "__main__":
    values = [str(i) for i in range(10)]
    for i in (5, 11):
        found_index = find_index(values, str(i))
        match found_index:
            case Some(index):
                print(f"Value {i} found at index {index}")
            case Empty():
                print(f"Value {i} not in list")


