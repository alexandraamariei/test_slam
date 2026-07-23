import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class TurtleBotController(Node):
    def __init__(self):
        super().__init__('turtlebot_controller')
        
        # Publisher pentru a trimite comenzi către motoare (sau Gazebo)
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscriber pentru a citi odometria (din Gazebo sau de la ESP32)
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        
        self.get_logger().info("Nodul TurtleBot Controller a pornit!")

    def odom_callback(self, msg):
        # Aici procesăm datele de poziție primite
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.get_logger().info(f"Poziție curentă: x={x:.2f}, y={y:.2f}")

    def move_robot(self, linear_x, angular_z):
        # Creăm mesajul Twist pentru mișcare
        msg = Twist()
        msg.linear.x = float(linear_x)     # Viteza de deplasare înainte/înapoi
        msg.angular.z = float(angular_z)   # Viteza de rotație
        
        self.cmd_vel_publisher.publish(msg)
        self.get_logger().info(f"Comandă trimisă: Viteză={linear_x}, Rotație={angular_z}")

def main(args=None):
    rclpy.init(args=args)
    controller = TurtleBotController()
    
    # Exemplu: Mutăm robotul în față la inițializare (pentru test)
    controller.move_robot(0.2, 0.0) 
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        # Oprim robotul la închiderea programului
        controller.move_robot(0.0, 0.0)
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
