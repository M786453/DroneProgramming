from pysimverse import Drone

drone = Drone()
drone.connect()
drone.set_speed(50)
drone.take_off()

drone.move_forward(225)

drone.rotate(90)

drone.move_forward(255)

drone.land()