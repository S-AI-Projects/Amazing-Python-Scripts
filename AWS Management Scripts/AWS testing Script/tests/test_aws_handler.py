import importlib.util
from pathlib import Path
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "awsHandler.py"
SPEC = importlib.util.spec_from_file_location("aws_handler_under_test", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load AWS handler from {SOURCE}")
AWS_HANDLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AWS_HANDLER)


class FakeEc2Client:
    def __init__(self):
        self.calls = []

    def run_instances(self, **parameters):
        self.calls.append(parameters)
        return {"Instances": [{"InstanceId": "ignored-return-value"}]}


class CreateEc2RegressionTests(unittest.TestCase):
    def assert_launch_parameters(self, ami_id, count, expected_parameters):
        # README.md line 3 describes EC2 machine generation. awsHandler.py
        # lines 1-10 build and send the requested launch parameters.
        client = FakeEc2Client()
        expected_result = None
        actual_result = AWS_HANDLER.create_ec2(client, ami_id, count)
        actual_calls = client.calls
        expected_calls = [expected_parameters]
        print(
            f"input={(ami_id, count)!r}, expected="
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
            f"input={(ami_id, count)!r}; expected calls={expected_calls!r}; "
            f"actual calls={actual_calls!r}",
        )

    def test_smallest_valid_instance_count(self):
        # README.md line 3 describes EC2 creation. awsHandler.py lines 4-5
        # map count to both AWS bounds; one is the smallest positive count.
        ami_id = "ami-smallest"
        count = 1
        expected_parameters = {
            "ImageId": "ami-smallest",
            "MinCount": 1,
            "MaxCount": 1,
        }
        self.assert_launch_parameters(ami_id, count, expected_parameters)

    def test_ordinary_instance_count(self):
        # README.md line 3 establishes the multi-instance use case;
        # awsHandler.py lines 4-5 forward count unchanged to both bounds.
        ami_id = "ami-ordinary"
        count = 3
        expected_parameters = {
            "ImageId": "ami-ordinary",
            "MinCount": 3,
            "MaxCount": 3,
        }
        self.assert_launch_parameters(ami_id, count, expected_parameters)


if __name__ == "__main__":
    unittest.main()
