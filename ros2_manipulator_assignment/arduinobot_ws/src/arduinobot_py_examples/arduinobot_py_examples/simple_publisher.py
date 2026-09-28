import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class SimplePublisher(Node):

    def __init__(self):
        super().__init__("simple_publisher")
        self.pub_ = self.create_publisher(String, "chatter", 10)
        self.counter_ = 0
        self.frequency_ = 1.0  # publishing rate in Hz
        self.get_logger().info("Publishing at %.1f Hz" % self.frequency_)

        # create_timer() expects the timer period in seconds, not a frequency
        self.timer_ = self.create_timer(1.0 / self.frequency_, self.timerCallback)

    def timerCallback(self):
        msg = String()
        msg.data = "Hello ROS 2 - counter: %d" % self.counter_
        self.pub_.publish(msg)
        self.counter_ += 1


def main():
    rclpy.init()

    simple_publisher = SimplePublisher()
    try:
        rclpy.spin(simple_publisher)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        simple_publisher.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
