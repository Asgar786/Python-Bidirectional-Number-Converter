# Python Bidirectional Number Converter

A Python program that converts whole numbers into English words and converts
valid English number words back into integers.

The converter supports non-negative whole numbers containing up to **37
decimal digits**, using the short-scale naming system through **Undecillion**.

## Features

- Number-to-words conversion.
- Words-to-number conversion.
- Supports numbers from zero through 37 digits.
- Supports scale names from Thousand through Undecillion.
- Validates number-word groups and scale order.
- Rejects inputs that exceed the supported range.
- Can be used as an importable Python module or as an interactive program.
- Uses only the Python standard library; no third-party packages are required.

## Requirements

- Python 3.10 or later.

Python 3.10+ is required because the converter uses structural pattern matching
(`match` / `case`).

## Project files

```text
Python-Bidirectional-Number-Converter/
│
├── number_converter.py
├── main.py
├── README.md
├── LICENSE
├── .gitignore
└── tests/
    └── test_converter.py
```

## Run the interactive program

Open a terminal in the project directory and run:

```bash
python main.py
```

The interactive program accepts up to ten inputs per run. Enter either a
decimal number or its English word representation.

## Use the converter as a module

Place `number_converter.py` in your project, then import the functions:

```python
from number_converter import (
    convert_to_words,
    convert_to_number,
    validate_number_words,
)

print(convert_to_words("1234567"))

print(
    convert_to_number(
        "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
    )
)
```

Output:

```text
One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven
1234567
```

### Validate words before converting

`validate_number_words()` returns a tuple containing a Boolean and either the
original input or an error message:

```python
valid, result = validate_number_words("One Thousand Two")

if valid:
    print(convert_to_number(result))
else:
    print(result)
```

`convert_to_number()` and `convert_to_words()` raise `ValueError` when their
input is invalid or outside the supported range.

## Run the tests

From the project directory, run:

```bash
python -m unittest discover -s tests -v
```

The tests cover ordinary values, hundreds, scale names, Undecillion,
round-trip conversion, invalid word groups, and the 37-digit limit.

## Supported range

The maximum input length is 37 decimal digits. The largest supported value is:

```text
9,999,999,999,999,999,999,999,999,999,999,999,999
```

The converter uses the short-scale naming system (Million, Billion, Trillion,
and so on).

## License

This project is released under the MIT License. See `LICENSE` for details.
