"""Bidirectional number and English-words converter.

Supports non-negative whole numbers containing up to 37 decimal digits,
using the short-scale naming system through Undecillion.
"""

MAX_DIGITS = 37

number_list = [
    (1, "One"), (2, "Two"), (3, "Three"), (4, "Four"),
    (5, "Five"), (6, "Six"), (7, "Seven"), (8, "Eight"),
    (9, "Nine"), (10, "Ten"), (11, "Eleven"), (12, "Twelve"),
    (13, "Thirteen"), (14, "Fourteen"), (15, "Fifteen"),
    (16, "Sixteen"), (17, "Seventeen"), (18, "Eighteen"),
    (19, "Nineteen"), (20, "Twenty"), (30, "Thirty"),
    (40, "Forty"), (50, "Fifty"), (60, "Sixty"),
    (70, "Seventy"), (80, "Eighty"), (90, "Ninety"),
]

scale_list = [
    (1_000, "Thousand"),
    (1_000_000, "Million"),
    (1_000_000_000, "Billion"),
    (1_000_000_000_000, "Trillion"),
    (1_000_000_000_000_000, "Quadrillion"),
    (1_000_000_000_000_000_000, "Quintillion"),
    (1_000_000_000_000_000_000_000, "Sextillion"),
    (1_000_000_000_000_000_000_000_000, "Septillion"),
    (1_000_000_000_000_000_000_000_000_000, "Octillion"),
    (1_000_000_000_000_000_000_000_000_000_000, "Nonillion"),
    (1_000_000_000_000_000_000_000_000_000_000_000, "Decillion"),
    (1_000_000_000_000_000_000_000_000_000_000_000_000, "Undecillion"),
]


def bidirectional_search(search_value):
    """Find a number from its word, or a word from its number."""
    search_value = str(search_value).casefold()

    return next(
        (
            word if search_value == str(number).casefold() else number
            for number, word in number_list
            if search_value == str(number).casefold()
            or search_value == word.casefold()
        ),
        None,
    )


def one_way_search(search_value):
    """Return the numeric value associated with a scale word."""
    search_value = search_value.casefold()

    return next(
        (
            number
            for number, word in scale_list
            if search_value == word.casefold()
        ),
        None,
    )


def group_digits(number):
    """Yield groups of up to three digits, starting from the right."""
    for end in range(len(number), 0, -3):
        yield number[max(0, end - 3):end]


def apply_groups(number):
    """Yield non-zero three-digit groups with their scale names."""
    groups = list(group_digits(number))

    for index, group in enumerate(groups):
        if int(group) == 0:
            continue

        if index == 0:
            yield group
        else:
            yield f"{group} {scale_list[index - 1][1]}"


def split_digits(number):
    """Split a decimal string into the components used to build its words."""
    if not number.isdecimal():
        raise ValueError("Input must contain decimal digits only.")

    if len(number) > MAX_DIGITS:
        raise ValueError(f"Number cannot exceed {MAX_DIGITS} digits.")

    groups = list(apply_groups(number))
    groups.reverse()
    values = []

    for group in groups:
        parts = group.split()
        value = int(parts[0])
        scale = parts[1] if len(parts) > 1 else None

        match len(str(value)):
            case 1:
                values.append([0, value, scale])

            case 2:
                if value > 19:
                    tens, units = divmod(value, 10)
                    values.append([tens * 10, units, scale])
                else:
                    values.append([0, value, scale])

            case 3:
                hundreds, remainder = divmod(value, 100)

                if 10 < remainder < 20:
                    values.append(
                        [hundreds, "Hundred", remainder, 0, scale]
                    )
                else:
                    tens, units = divmod(remainder, 10)
                    values.append(
                        [hundreds, "Hundred", tens * 10, units, scale]
                    )

    return values


def validate_group(words):
    """Check whether words form a valid number from 1 through 999."""
    if not words:
        return False

    words = [word.casefold() for word in words]
    numbers = {word.casefold(): value for value, word in number_list}

    index = 0

    if len(words) >= 2 and words[1] == "hundred":
        if words[0] not in numbers or not 1 <= numbers[words[0]] <= 9:
            return False

        index = 2

    remaining = words[index:]

    if not remaining:
        return True

    if len(remaining) == 1:
        return remaining[0] in numbers

    if len(remaining) == 2:
        first = numbers.get(remaining[0])
        second = numbers.get(remaining[1])

        if first is None or second is None:
            return False

        return first >= 20 and first % 10 == 0 and 1 <= second <= 9

    return False


def _convert_to_number(text):
    """Convert already-validated number words into an integer."""
    total = 0
    group_value = 0

    for word in text.split():
        value = bidirectional_search(word)

        if value is not None:
            group_value += int(value)

        elif word.casefold() == "hundred":
            group_value *= 100

        else:
            scale = one_way_search(word)

            if scale is not None:
                total += group_value * scale
                group_value = 0

    return total + group_value


def validate_number_words(text):
    """Validate number words and enforce the 37-digit maximum.

    Returns (True, original_text) when valid, otherwise (False, error_message).
    """
    words = text.casefold().split()

    if not words:
        return False, "Input cannot be empty."

    scales = {word.casefold(): value for value, word in scale_list}
    numbers = {word.casefold(): value for value, word in number_list}

    if words == ["zero"]:
        return True, text

    if "zero" in words:
        return False, "Zero cannot be combined with other number words."

    current_group = []
    previous_scale = float("inf")

    for word in words:
        if word in scales:
            scale = scales[word]

            if scale >= previous_scale:
                return False, f"Invalid scale order: {word}"

            if not current_group:
                return False, f"Missing number before {word}."

            if not validate_group(current_group):
                return False, "Invalid number group."

            previous_scale = scale
            current_group = []

        elif word in numbers or word == "hundred":
            current_group.append(word)

        else:
            return False, f"Unrecognised word: {word}"

    # Validate the final group, which is not followed by a scale word.
    if current_group and not validate_group(current_group):
        return False, "Invalid number group."

    # Enforce the same maximum for words-to-number conversion.
    if len(str(_convert_to_number(text))) > MAX_DIGITS:
        return False, f"Number cannot exceed {MAX_DIGITS} digits."

    return True, text


def convert_to_number(text):
    """Convert valid English number words into an integer.

    Raises ValueError if the supplied words are invalid or exceed 37 digits.
    """
    valid, result = validate_number_words(text)

    if not valid:
        raise ValueError(result)

    return _convert_to_number(text)


def convert_to_words(search_input):
    """Convert a non-negative integer or decimal string into English words.

    Raises ValueError if the input is not decimal or exceeds 37 digits.
    """
    search_input = str(search_input)

    if not search_input.isdecimal():
        raise ValueError("Input must contain decimal digits only.")

    if len(search_input) > MAX_DIGITS:
        raise ValueError(f"Number cannot exceed {MAX_DIGITS} digits.")

    if int(search_input) == 0:
        return "Zero"

    words = []

    for group in split_digits(search_input):
        for item in group:
            if item is None or item == 0:
                continue

            if isinstance(item, str):
                words.append(item)
            else:
                word = bidirectional_search(item)

                if word is not None:
                    words.append(word)

    return " ".join(words)
