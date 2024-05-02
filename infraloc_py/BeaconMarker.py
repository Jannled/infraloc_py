import math
from tkinter import TclError
from matplotlib import pyplot as plt
import rclpy
from rclpy.node import Node

import colorsys

from visualization_msgs.msg import MarkerArray, Marker

# ros2 run infraloc_py beacon_marker --params-file src/infraloc_py/beacon_pos.yml
# ros2 param load infraloc src/infraloc_py/beacon_pos.yml

PCB_DIAMETER = 0.07 # m
NUM_MARKERS = 3

class BeaconMarker(Node):
	def __init__(self, topicName: str):
		super().__init__('infraloc')
		self.pub = self.create_publisher(
			MarkerArray,
			topicName,
			5
		)

		self.declare_parameter('chan_1_x', 0.0)
		self.declare_parameter('chan_1_y', 0.0)
		self.declare_parameter('chan_2_x', 0.0)
		self.declare_parameter('chan_2_y', 0.0)
		self.declare_parameter('chan_3_x', 0.0)
		self.declare_parameter('chan_3_y', 0.0)

		#self.declare_parameters(namespace='', parameters=[
		#	('chan_1_x', rclpy.Parameter.Type.DOUBLE),
		#	('chan_1_y', rclpy.Parameter.Type.DOUBLE),
		#	('chan_2_x', rclpy.Parameter.Type.DOUBLE),
		#	('chan_2_y', rclpy.Parameter.Type.DOUBLE),
		#	('chan_3_x', rclpy.Parameter.Type.DOUBLE),
		#	('chan_3_y', rclpy.Parameter.Type.DOUBLE)
		#])

		self.timer_pos = self.create_timer(2.0, self.publish_positions)


	def publish_positions(self):
		msg = MarkerArray()
		msg.markers = []

		for i in range(0, NUM_MARKERS):
			marker = Marker()
			marker.id = i
			marker.header.frame_id = 'map'
			marker.type = Marker.CYLINDER
			marker.action = Marker.ADD

			marker.scale.x = PCB_DIAMETER # !important
			marker.scale.y = PCB_DIAMETER # !important
			marker.scale.z = PCB_DIAMETER / 5 # !important

			color = colorsys.hsv_to_rgb(i/NUM_MARKERS, 0.5, 1.0)
			marker.color.r = color[0]
			marker.color.g = color[1]
			marker.color.b = color[2]
			marker.color.a = 1.0 # !important
			
			marker.pose.position.x = self.get_parameter('chan_' + str(i+1) + '_x').get_parameter_value().double_value
			marker.pose.position.y = self.get_parameter('chan_' + str(i+1) + '_y').get_parameter_value().double_value
			marker.pose.position.z = 0.0
			marker.pose.orientation.w = 1.0 # !important

			msg.markers.append(marker)
			
		self.pub.publish(msg)


def main(args=None):
	global bars, polar
	rclpy.init(args=args)

	markerArray = BeaconMarker('beacon_pos_array')

	try:
		rclpy.spin(markerArray)
	except KeyboardInterrupt as e:
		print("KeyboardInterrupt")
		pass

	try:
		if rclpy.ok():
			rclpy.shutdown()
	except Exception as e:
		print(e)


if __name__ == '__main__':
	main()
