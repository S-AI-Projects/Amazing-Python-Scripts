import contextlib
import datetime
import doctest
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import call, patch


SOURCE = Path(__file__).resolve().parents[1] / "amazonprice.py"


class StopPriceTrackerLoop(Exception):
    pass


class FakeProduct:
    def __init__(self, value):
        self.value = value
        self.text = value

    def get_text(self):
        return self.value

    def strip(self):
        return self.value.strip()


class FakeSoup:
    def find(self, _tag=None, id=None, **_kwargs):
        if id == "productTitle":
            return FakeProduct("Fixture Product")
        return FakeProduct("10.")


def load_amazonprice():
    requests = types.ModuleType("requests")
    requests.get = lambda *_args, **_kwargs: types.SimpleNamespace(content=b"")
    bs4 = types.ModuleType("bs4")
    bs4.BeautifulSoup = lambda *_args, **_kwargs: FakeSoup()
    pywhatkit = types.ModuleType("pywhatkit")
    pywhatkit.sendwhatmsg = lambda *_args, **_kwargs: None
    modules = {
        "requests": requests,
        "bs4": bs4,
        "pywhatkit": pywhatkit,
    }

    def stop_sleep(_seconds):
        raise StopPriceTrackerLoop

    spec = importlib.util.spec_from_file_location("amazonprice", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load price tracker from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    inputs = [
        "fixture-user-agent",
        "https://example.test/product",
        "0",
        "fixture@example.test",
        "fixture-password",
        "+15550000000",
    ]
    with patch.dict(sys.modules, modules):
        with patch("builtins.input", side_effect=inputs):
            with patch("time.sleep", side_effect=stop_sleep):
                with contextlib.redirect_stdout(io.StringIO()):
                    try:
                        spec.loader.exec_module(module)
                    except StopPriceTrackerLoop:
                        pass
    return module


AMAZONPRICE = load_amazonprice()


class MessageSendingTests(unittest.TestCase):
    def test_documented_example(self):
        result = doctest.testmod(AMAZONPRICE, verbose=False)
        expected = doctest.TestResults(failed=0, attempted=3)
        print(f"docstring example: expected={expected!r}, actual={result!r}")
        self.assertEqual(
            result,
            expected,
            f"expected doctest result={expected!r}; actual={result!r}",
        )

    def assert_message_sending(self, phone_number, title, fixed_now, expected_call):
        expected_result = None
        original_phone = phone_number
        original_title = title
        with patch.object(AMAZONPRICE.datetime, "datetime") as clock:
            with patch.object(
                AMAZONPRICE.pywhatkit, "sendwhatmsg"
            ) as send_message:
                clock.now.return_value = fixed_now
                actual_result = AMAZONPRICE.message_sending(phone_number, title)
        actual_calls = send_message.call_args_list
        expected_calls = [expected_call]
        print(
            f"input={(phone_number, title)!r}, now={fixed_now!r}, expected="
            f"{(expected_result, expected_calls)!r}, actual="
            f"{(actual_result, actual_calls)!r}"
        )
        self.assertIsNone(
            actual_result,
            f"expected return={expected_result!r}; actual return={actual_result!r}",
        )
        self.assertEqual(
            actual_calls,
            expected_calls,
            f"input={(phone_number, title)!r}; expected calls={expected_calls!r}; "
            f"actual calls={actual_calls!r}",
        )

    def test_smallest_valid_input(self):
        # amazonprice.py lines 49-51 interpolate the title and forward the
        # phone number. An empty title is the shortest accepted title.
        phone_number = "+15551234567"
        title = ""
        fixed_now = datetime.datetime(2024, 1, 2, 9, 41)
        expected_message = (
            "Price of  is fallen below the threshold amount. Click on the link "
            "below to buy the product!!!\n\n"
        )
        expected_call = call(phone_number, expected_message, 9, 42)
        self.assert_message_sending(
            phone_number, title, fixed_now, expected_call
        )

    def test_ordinary_input(self):
        # amazonprice.py lines 49-50 build the alert and schedule it one minute
        # after now. The separate User-Agent request setup is at source line 20.
        phone_number = "+15551234567"
        title = "Stainless Steel Bottle"
        fixed_now = datetime.datetime(2024, 1, 2, 14, 8)
        expected_message = (
            "Price of Stainless Steel Bottle is fallen below the threshold amount. "
            "Click on the link below to buy the product!!!\n\n"
        )
        expected_call = call(phone_number, expected_message, 14, 9)
        self.assert_message_sending(
            phone_number, title, fixed_now, expected_call
        )


if __name__ == "__main__":
    unittest.main()
