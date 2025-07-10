#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedStateArray
from my_robot_interfaces.srv import SetLed

class LedPanelNode(Node):
    def __init__(self):
        super().__init__("led_panel")
        self.led_states_ = [0, 0, 0]  # ✅ Only initialize here once

        self.led_state_pub_ = self.create_publisher(LedStateArray, "led_panel_state", 10)
        self.led_state_timer_ = self.create_timer(5.0, self.publish_led_state)

        self.set_led_service_ = self.create_service(SetLed, "Set_Led", self.callback_set_led)

        self.get_logger().info("Led panel node has been started")

    def publish_led_state(self):
        self.get_logger().info(f"Timer callback triggered: publishing {self.led_states_}")
        msg = LedStateArray()
        msg.led_status = self.led_states_
        self.led_state_pub_.publish(msg)

    def callback_set_led(self, request: SetLed.Request, response: SetLed.Response):
        led_number = request.led_number
        state = request.state

        if led_number >= len(self.led_states_) or led_number < 0:
            response.success = False
            return response
        if state not in (0, 1):
            response.success = False
            return response

        self.led_states_[led_number] = state
        self.publish_led_state()  # ✅ Optional: immediately publish change
        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
