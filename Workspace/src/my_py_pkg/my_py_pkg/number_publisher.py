#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class NumberPulsiherNode(Node):
    
    def __init__(self):
        super().__init__("number_publisher")
        self.declare_parameter("number", 2)
        self.declare_parameter("time_period",1.0)
        self.counter_=self.get_parameter("number").value
        self.timer_period_=self.get_parameter("time_period").value
        self.publisher_=self.create_publisher(Int64, "number",10)
        self.timer_=self.create_timer(self.timer_period_,self.publish_number)
        self.get_logger().info("Number Publisher has been statarted. ")


    def publish_number(self):
        msg=Int64()
        msg.data=self.counter_
        self.publisher_.publish(msg)
        self.counter_+=1

def main(args=None):
    rclpy.init(args=args)
    node=NumberPulsiherNode()
    rclpy.spin(node)
    rclpy.shutdown

if __name__=="__main__":
    main()


