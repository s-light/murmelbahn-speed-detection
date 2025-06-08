import time
import board
import pulseio
import neopixel

import digitalio
import analogio

print("")
print("threshold.py")


btnReset = digitalio.DigitalInOut(board.GP21)
btnReset.direction = digitalio.Direction.INPUT
btnReset.pull = digitalio.Pull.UP

# possible pins:
# board.A0 board.GP26 board.GP26_A0 (GPIO26)
# board.A1 board.GP27 board.GP27_A1 (GPIO27)
# board.A2 board.GP28 board.GP28_A2 (GPIO28)

sensor0 =  analogio.AnalogIn(board.GP26_A0)
sensor1 =  analogio.AnalogIn(board.GP28_A2)
sensor0_ts = None
sensor1_ts = None

threshold = 9000

measured_duration_us = 0
measured_duration_ms = 0
measured_duration_s = 0
measured_delay = 0
speed = 0

distance_mm = 200
distance_cm = distance_mm / 10.0
distance_m = distance_cm / 100.0


print(f"distance_mm: {distance_mm}mm")
print(f"distance_cm: {distance_cm}cm")
print(f"distance_m: {distance_m}m")
time.sleep(2)
print("running..")


def printLog():
    print(
        f"{sensor0.value:>5}; {sensor1.value:>5};",
        f"{(sensor0_ts if sensor0_ts else 0):>14}; {(sensor1_ts if sensor1_ts else 0):>14};",
        f"{(measured_duration_s):>10.4f}s;",
        f"{(speed):>10.4f}m/s;",
    )


def main():
    global measured_duration_us
    global measured_duration_ms
    global measured_duration_s
    global speed
    global sensor0
    global sensor0_ts
    global sensor1
    global sensor1_ts

    if sensor0.value < threshold:
        sensor0_ts = time.monotonic_ns()
    if sensor1.value < threshold:
        sensor1_ts = time.monotonic_ns()

    # printLog()

    if sensor0_ts and sensor1_ts:
        # printLog()

        measured_duration_ns = sensor1_ts - sensor0_ts
        measured_duration_us = measured_duration_ns / 1000.0
        measured_duration_ms = measured_duration_us / 1000.0
        measured_duration_s = measured_duration_ms / 1000.0

        speed = distance_m / measured_duration_s

        print(
            "\n",
            f"{measured_duration_ms:>10.4f}ms → ",
            f"{measured_duration_s:>7.4f}s → ",
            f"{speed:>9.4f}m/s ",
            "\n",
        )
        # printLog()
        time.sleep(0.1)
        # wait until button is pressed.
        while btnReset.value:
            time.sleep(0)

        sensor0_ts = None
        sensor1_ts = None
        measured_duration_us = 0
        measured_duration_ms = 0
        measured_duration_s = 0
        measured_delay = 0
        speed = 0
        print("running..")


while True:
    main()
