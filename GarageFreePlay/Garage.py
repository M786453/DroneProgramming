from pysimverse import Drone
import time

drone = Drone()
drone.connect()
drone.take_off()

time.sleep(2)

drone.rotate(45)

drone.move_forward(20)

drone.move_backward(100)

drone.rotate(45)

drone.move_left(50)

drone.move_right(50)

time.sleep(2)

drone.land()


