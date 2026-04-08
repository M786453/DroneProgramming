from pysimverse import Drone
import time

class Level3:

    def __init__(self):
        self.drone = Drone()
        self.drone.connect()
        self.drone.set_speed(200)
        self.drone.take_off(50,200)

    def __reach_first_checkpoint(self):

        print("Reaching First Checkpoint...")

        self.drone.rotate(-35)

        self.drone.move_forward(380)

        print("First Checkpoint reached.")

    def __reach_second_checkpoint(self):

        print("Reaching Second Checkpoint...")

        self.drone.rotate(150)

        self.drone.move_forward(470)

        self.drone.land()

        print("Second Checkpoint reached.")
        

    def complete(self):

        self.__reach_first_checkpoint()
        self.__reach_second_checkpoint()


if __name__ == "__main__":

    level2 = Level3()
    level2.complete()

    time.sleep(10)
