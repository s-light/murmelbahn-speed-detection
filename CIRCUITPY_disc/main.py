import time
import board
import pulseio
import neopixel

import digitalio
import analogio

print("")
print("murmelbahn-speed-detection main.py")


btnReset = digitalio.DigitalInOut(board.GP21)
btnReset.direction = digitalio.Direction.INPUT
btnReset.pull = digitalio.Pull.UP

# possible pins:
# board.A0 board.GP26 board.GP26_A0 (GPIO26)
# board.A1 board.GP27 board.GP27_A1 (GPIO27)
# board.A2 board.GP28 board.GP28_A2 (GPIO28)

sensor0 = analogio.AnalogIn(board.GP26_A0)
sensor1 = analogio.AnalogIn(board.GP28_A2)
sensor0_ts = None
sensor1_ts = None

threshold = 9000

distance_mm = 200
distance_cm = distance_mm / 10.0
distance_m = distance_cm / 100.0


print(f"distance_mm: {distance_mm}mm")
print(f"distance_cm: {distance_cm}cm")
print(f"distance_m: {distance_m}m")
time.sleep(2)
print("running..")


def update_speed_measurement():
    global sensor0
    global sensor0_ts
    global sensor1
    global sensor1_ts

    if sensor0.value < threshold:
        sensor0_ts = time.monotonic_ns()
    if sensor1.value < threshold:
        sensor1_ts = time.monotonic_ns()

    if sensor0_ts and sensor1_ts:
        measured_duration_ns = sensor1_ts - sensor0_ts
        measured_duration_s = measured_duration_ns / (1000.0 * 1000.0 * 1000.0)
        speed = distance_m / measured_duration_s
        print(
            f"{speed:>3.2f}m/s ",
            f"→ ",
            f"{(speed*3.6):>4.2f}km/h ",
        )
        time.sleep(0.1)
        # reset
        sensor0_ts = None
        sensor1_ts = None


def main():
    update_speed_measurement()


while True:
    main()
