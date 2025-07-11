import rclpy
from rclpy.node import Node
import serial
from pynput import keyboard

class TeleopBTCar(Node):
    def __init__(self):
        super().__init__('teleop_bt_car_node')

        self.serial_port = '/dev/rfcomm0'
        self.baud_rate = 9600

        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.get_logger().info(f'Connected to {self.serial_port}')
        except Exception as e:
            self.get_logger().error(f'Failed to connect to serial port: {e}')
            return

        print("Use arrow keys to drive. 's' to stop. ESC to exit.")
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def send_command(self, cmd):
        try:
            self.ser.write(cmd.encode())
            self.get_logger().info(f'Sent: {cmd}')
        except Exception as e:
            self.get_logger().error(f'Failed to send command: {e}')

    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.send_command('f')
            elif key == keyboard.Key.down:
                self.send_command('b')
            elif key == keyboard.Key.left:
                self.send_command('l')
            elif key == keyboard.Key.right:
                self.send_command('r')
            elif key.char == 's':
                self.send_command('s')
        except AttributeError:
            pass

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.get_logger().info('ESC pressed. Exiting...')
            rclpy.shutdown()
        elif key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left,keyboard.Key.right]:
            self.send_command('s')  # Send stop when arrow key is released

def main(args=None):
    rclpy.init(args=args)
    node = TeleopBTCar()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
