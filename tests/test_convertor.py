import unittest

from number_converter import (
    convert_to_number,
    convert_to_words,
    validate_number_words,
)


class NumberConverterTests(unittest.TestCase):

    def test_number_to_words_basic_values(self):
        cases = {
            "0": "Zero",
            "1": "One",
            "19": "Nineteen",
            "20": "Twenty",
            "21": "Twenty One",
            "99": "Ninety Nine",
            "100": "One Hundred",
            "101": "One Hundred One",
            "110": "One Hundred Ten",
            "999": "Nine Hundred Ninety Nine",
            "1000": "One Thousand",
            "1001": "One Thousand One",
            "1234567": (
                "One Million Two Hundred Thirty Four Thousand "
                "Five Hundred Sixty Seven"
            ),
        }

        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(convert_to_words(number), expected)

    def test_words_to_number(self):
        cases = {
            "Zero": 0,
            "One": 1,
            "Twenty One": 21,
            "One Hundred": 100,
            "One Hundred Nineteen": 119,
            "One Thousand One": 1001,
            "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven": 1234567,
            "One Undecillion": 10**36,
        }

        for words, expected in cases.items():
            with self.subTest(words=words):
                self.assertEqual(convert_to_number(words), expected)

    def test_37_digit_round_trip(self):
        number = str(10**37 - 1)
        words = convert_to_words(number)

        self.assertEqual(convert_to_number(words), int(number))

    def test_undecillion(self):
        self.assertEqual(convert_to_words(str(10**36)), "One Undecillion")
        self.assertEqual(convert_to_number("One Undecillion"), 10**36)

    def test_rejects_more_than_37_digits(self):
        valid, message = validate_number_words("Ten Undecillion")

        self.assertFalse(valid)
        self.assertIn("37 digits", message)

        with self.assertRaises(ValueError):
            convert_to_words("1" + ("0" * 37))

    def test_rejects_invalid_word_order(self):
        valid, _ = validate_number_words("One Thousand One Million")
        self.assertFalse(valid)

    def test_rejects_invalid_number_group(self):
        valid, _ = validate_number_words("Twenty Twenty")
        self.assertFalse(valid)

    def test_rejects_zero_combined_with_other_words(self):
        valid, _ = validate_number_words("Zero One")
        self.assertFalse(valid)

    def test_rejects_unknown_words(self):
        valid, _ = validate_number_words("One Zillion")
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()
