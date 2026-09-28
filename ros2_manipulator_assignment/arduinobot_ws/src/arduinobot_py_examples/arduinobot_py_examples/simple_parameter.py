from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.parameter import Parameter


class SimpleParameter(Node):

    # Parameters handled by this node and the type each one must keep
    EXPECTED_TYPES = {
        "simple_int_param": Parameter.Type.INTEGER,
        "simple_string_param": Parameter.Type.STRING,
    }

    def __init__(self):
        super().__init__("simple_parameter")
        self.declare_parameter("simple_int_param", 28)
        self.declare_parameter("simple_string_param", "Antonio")

        self.add_on_set_parameters_callback(self.paramChangeCallback)

    def paramChangeCallback(self, params):
        # Check the whole request first, so that one valid parameter cannot
        # make an update containing an invalid one succeed.
        for param in params:
            expected_type = self.EXPECTED_TYPES.get(param.name)
            if expected_type is not None and param.type_ != expected_type:
                return SetParametersResult(
                    successful=False,
                    reason="%s must be of type %s" % (param.name, expected_type.name))

        # Parameters not handled here (e.g. use_sim_time) are accepted unchanged
        for param in params:
            if param.name == "simple_int_param":
                self.get_logger().info(
                    "Param simple_int_param changed! New value is %d" % param.value)
            elif param.name == "simple_string_param":
                self.get_logger().info(
                    "Param simple_string_param changed! New value is %s" % param.value)

        return SetParametersResult(successful=True)


def main():
    rclpy.init()

    simple_parameter = SimpleParameter()
    try:
        rclpy.spin(simple_parameter)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        simple_parameter.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
