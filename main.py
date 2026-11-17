"""Interactive command-line interface for the number converter."""

from number_converter import (
    MAX_DIGITS,
    convert_to_number,
    convert_to_words,
    validate_number_words,
)


def main():
    """Run the converter for up to ten inputs."""
    for _ in range(10):
        search_input = input(
            "Enter a number or a word to convert: "
        ).strip()

        if search_input.isdecimal():
            if len(search_input) > MAX_DIGITS:
                print(f"Number cannot exceed {MAX_DIGITS} digits.")
                continue

            print(
                f"The word representation of {search_input} is: "
                f"{convert_to_words(search_input)}"
            )

        else:
            valid, result = validate_number_words(search_input)

            if not valid:
                print(result)
                continue

            print(
                f"The value representation of {result} is: "
                f"{convert_to_number(result)}"
            )


if __name__ == "__main__":
    main()
