from djitellopy import Tello
import time

# Initialize the Tello drone
tello = Tello()


# Connect to the drone
tello.connect()
print(f"Battery: {tello.get_battery()}%")


# Take off
tello.takeoff()
print("Tello has taken off.")

# Hover for 5 seconds
time.sleep(5)

tello.land()
print("Tello has landed.")