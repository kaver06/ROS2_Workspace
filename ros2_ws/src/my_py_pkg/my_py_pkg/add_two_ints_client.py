#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial

class AddTwiIntsClient(Node):
    
    def __init__(self):
        super().__init__("add_two_ints_clients")
        self.client_=self.create_client(AddTwoInts, "add_two_ints")


    def call_add_two_ints(self, a, b):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for two Ints server...")
        
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client_.call_async(request)
        future.add_done_callback (partial(self.callback_call_add_two_ints,request=request))

    def callback_call_add_two_ints(self, future, request):
        response = future.result()
        self.get_logger().info(str(request.a) + " + " + str(request.b) + " = " + str(response.sum))


def main(args=None):
    rclpy.init(args=args)
    node=AddTwiIntsClient()
    node.call_add_two_ints(2, 7)
    node.call_add_two_ints(6, 8)
    node.call_add_two_ints(5, 2)

    rclpy.spin(node)
    rclpy.shutdown

if __name__=="__main__":
    main()


