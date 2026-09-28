"""Checks for the parameter-update contract of the simple_parameter node."""

from arduinobot_py_examples.simple_parameter import SimpleParameter
import pytest
import rclpy
from rclpy.parameter import Parameter


@pytest.fixture
def node():
    rclpy.init()
    simple_parameter = SimpleParameter()
    yield simple_parameter
    simple_parameter.destroy_node()
    rclpy.shutdown()


def test_defaults(node):
    assert node.get_parameter("simple_int_param").value == 28
    assert node.get_parameter("simple_string_param").value == "Antonio"


def test_valid_updates_are_accepted(node):
    results = node.set_parameters([
        Parameter("simple_int_param", Parameter.Type.INTEGER, 30),
        Parameter("simple_string_param", Parameter.Type.STRING, "ROS 2"),
    ])
    assert all(result.successful for result in results)
    assert node.get_parameter("simple_int_param").value == 30
    assert node.get_parameter("simple_string_param").value == "ROS 2"


def test_parameters_not_handled_by_the_node_are_accepted(node):
    result = node.set_parameters([Parameter("use_sim_time", Parameter.Type.BOOL, True)])[0]
    assert result.successful
    assert node.get_parameter("use_sim_time").value is True


def test_wrong_type_is_rejected(node):
    result = node.set_parameters([
        Parameter("simple_int_param", Parameter.Type.STRING, "thirty")])[0]
    assert not result.successful
    assert node.get_parameter("simple_int_param").value == 28


def test_batch_with_one_invalid_parameter_is_rejected_as_a_whole(node):
    result = node.set_parameters_atomically([
        Parameter("simple_int_param", Parameter.Type.INTEGER, 5),
        Parameter("simple_string_param", Parameter.Type.INTEGER, 7),
    ])
    assert not result.successful
    assert node.get_parameter("simple_int_param").value == 28
    assert node.get_parameter("simple_string_param").value == "Antonio"


def test_callback_rejects_mixed_batch(node):
    # rclpy normally rejects a wrong type before the callback runs, because the
    # declared type is enforced; the callback applies the same rule itself.
    result = node.paramChangeCallback([
        Parameter("simple_int_param", Parameter.Type.INTEGER, 5),
        Parameter("simple_string_param", Parameter.Type.INTEGER, 7),
    ])
    assert not result.successful
    assert "simple_string_param" in result.reason
