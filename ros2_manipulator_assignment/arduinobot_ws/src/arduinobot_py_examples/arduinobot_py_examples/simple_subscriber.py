import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class SimpleSubscriber(Node):

    def __init__(self):
        super().__init__("simple_subscriber")
        self.sub_ = self.create_subscription(String, "chatter", self.msgCallback, 10)

    def msgCallback(self, msg):
        self.get_logger().info("I heard: %s" % msg.data)


def main():
    rclpy.init()

    simple_subscriber = SimpleSubscriber()
    try:
        rclpy.spin(simple_subscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        simple_subscriber.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
