#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounterNode(Node):
    
    def __init__(self):
        super().__init__("number_counter")
        self.last_counter=0

        self.subscriber_=self.create_subscription(Int64,"number",self.callback_counter_val,10)
        self.get_logger().info("Counter Recieving has been started")

        self.publisher_=self.create_publisher(Int64,"number_counter",10)
        self.get_logger().info("Number futher publishing has been started ")

        self.reset_counter_server_=self.create_service(SetBool,"reset_counter",self.callback_reset_counter)
        self.get_logger().info("Reset request server has also been started. ")

    def callback_reset_counter(self, request:SetBool.Request, response:SetBool.Response):
        if request.data==True:
            self.last_counter=0
            response.success=True
            response.message=("Reset complete")
        else:
            response.success=False
            response.message="Reset request not accepted"
        return response

    def callback_counter_val(self,msg:Int64):
        self.last_counter+=2
        self.get_logger().info(str(msg.data))
        new_msg=Int64()
        new_msg.data=self.last_counter
        self.publisher_.publish(new_msg)

def main(args=None):
    rclpy.init(args=args)
    node=NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown

if __name__=="__main__":
    main()


