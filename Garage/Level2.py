from pysimverse import Drone
import time

class Level2:

    def __init__(self):
        self.drone = Drone()
        self.drone.connect()
        self.drone.set_speed(200)
        self.drone.take_off(100,200)

    def __reach_first_checkpoint(self):

        print("Reaching First Checkpoint...")

        self.drone.rotate(-80)

        self.drone.move_forward(230)

        print("First Checkpoint reached.")

    def __reach_second_checkpoint(self):

        print("Reaching Second Checkpoint...")

        self.drone.rotate(140)

        self.drone.move_forward(250)

        print("Second Checkpoint reached.")

    def __reach_third_checkpoint(self):

        print("Reaching Third Checkpoint...")

        self.drone.rotate(10)

        self.drone.move_forward(290)

        self.drone.land(200)

        print("Third Checkpoint reached.")

    def complete(self):

        self.__reach_first_checkpoint()
        self.__reach_second_checkpoint()
        self.__reach_third_checkpoint()


if __name__ == "__main__":

    level2 = Level2()
    level2.complete()

    time.sleep(10)
