from unittest import TestCase
from unittest.mock import patch

from cli.utils_custom_command import EpicEventsCommand


class CliInputTestCase(TestCase):
    @patch("cli.utils_custom_command.EpicEventsCommand.custom_input")
    def test_text_input_successful(self, mock_custom_input):
        expected_values = ["some value", "value"]
        mock_custom_input.side_effect = expected_values

        value = EpicEventsCommand.text_input("label")
        self.assertEqual(value, "some value")

        value = EpicEventsCommand.text_input("label")
        self.assertEqual(value, "value")

    @patch("cli.utils_custom_command.EpicEventsCommand.custom_input")
    def test_int_input_successful(self, mock_custom_input):
        expected_value = [12, 2]
        mock_custom_input.side_effect = expected_value

        value = EpicEventsCommand.int_input("label")
        self.assertEqual(value, 12)

        value = EpicEventsCommand.int_input("label")
        self.assertEqual(value, 2)
