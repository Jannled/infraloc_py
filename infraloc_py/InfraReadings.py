from tkinter import TclError
from matplotlib import pyplot as plt
import rclpy
from rclpy.node import Node
from rclpy.task import Future

from infraloc_interfaces.msg import InfraData
from infraloc_py.utils import qos_uros_best_effort, INFRALOC_NUM_CHANNELS

future_mutex = Future()
graph = None

NUM_SAMPLES = 120

class InfraReadings(Node):
    def __init__(self, topicName: str):
        super().__init__('infra_readings')
        self.subscription = self.create_subscription(
            InfraData,
            topicName,
            self.listener_callback,
            qos_uros_best_effort)
        self.subscription  # prevent unused variable warning

        self.get_logger().info('Started InfraReadings Plotter')

    def listener_callback(self, msg):
        graph.set_ydata(msg.data)
        future_mutex.done()


def main(args=None):
    global graph
    rclpy.init(args=args)

    topicName: str = input("Please enter the topic name to listen to: ")
    infra_readings = InfraReadings(topicName)

    # Create Figure
    plt.ion()
    fig = plt.figure(topicName)
    #fig, ax = plt.subplots()

    # Subplot 1
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title(topicName)
    ax1.set_ylim(0, 20000)
    graph = ax1.plot(range(0, NUM_SAMPLES), range(0, NUM_SAMPLES))
    plt.show()

    while True:
        try:
            plt.pause(0.01)
            rclpy.spin_once(infra_readings, timeout_sec=0.01)
        except (KeyboardInterrupt, TclError):
            print('Request to quit')
            break

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    infra_readings.destroy_node()

    try:
        if rclpy.ok():
            rclpy.shutdown()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
