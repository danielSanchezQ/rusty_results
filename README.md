# Rusty results

Rusty results is a Python library for dealing with result types and option inspired on rust standard library.

Error handling with the Result and Err types.

Type Option represents an optional value: every Option is either Some and contains a value, or Empty and does not.
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
import rusty_results
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)