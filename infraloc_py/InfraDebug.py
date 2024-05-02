import math
from tkinter import TclError
from matplotlib import pyplot as plt
import rclpy
from rclpy.node import Node
from rclpy.task import Future

from infraloc_interfaces.msg import BucketStrength
from infraloc_py.utils import qos_uros_best_effort, INFRALOC_NUM_CHANNELS


class BeaconStrength(Node):
    def __init__(self, topicName: str, barPlot, polarPlot):
        super().__init__('beacon_strength')
        self.barPlot = barPlot
        self.polarPlot = polarPlot
        self.subscription = self.create_subscription(
            BucketStrength,
            topicName,
            self.listener_callback,
            qos_uros_best_effort)
        self.subscription  # prevent unused variable warning

        self.get_logger().info('Started BeaconStrength Plotter')

    def listener_callback(self, msg):
        # Iterate over wedges
        angle = msg.angle
        self.polarPlot.set_xdata([0, angle])

        # Iterate over bar plot
        for i, b in enumerate(self.barPlot):
            b.set_height(msg.bucket_strength[i])


def main(args=None):
    global bars, polar
    rclpy.init(args=args)

    beacon_strength1 = BeaconStrength('/bucket_strength')
    beacon_strength2 = BeaconStrength('/bucket_strength2')
    beacon_strength3 = BeaconStrength('/bucket_strength3')

    # Create Figure
    plt.ion()
    fig = plt.figure(topicName)
    #fig, ax = plt.subplots()

    # Subplot 1
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_title(topicName)
    ax1.set_ylim(0, 20000)
    bars = ax1.bar(range(0, INFRALOC_NUM_CHANNELS), range(0, INFRALOC_NUM_CHANNELS))

    # Subplot 2
    ax2 = fig.add_subplot(1, 2, 2, projection='polar')
    polar, = ax2.plot([0, math.radians(360)], [0, 1])
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)

    plt.show()

    while True:
        try:
            plt.pause(0.01)
            rclpy.spin_once(beacon_strength, timeout_sec=0.01)
            #rclpy.spin_until_future_complete(beacon_strength, future_mutex)
        except (KeyboardInterrupt, TclError):
            print('Request to quit')
            break

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    beacon_strength.destroy_node()

    try:
        if rclpy.ok():
            rclpy.shutdown()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
