import time
import board
import pulseio
import neopixel

import digitalio
import analogio

print("")
print("timetest.py")


btnReset = digitalio.DigitalInOut(board.GP21)
btnReset.direction = digitalio.Direction.INPUT
btnReset.pull = digitalio.Pull.UP


distance_cm = 20.0
distance_m = distance_cm / 100.0

def time_test(sleep_time):
    ts_1 = time.monotonic_ns()
    time.sleep(sleep_time)
    ts_2 = time.monotonic_ns()

    measured_duration_ns = ts_2 - ts_1
    measured_duration_us = measured_duration_ns / 1000.0
    measured_duration_ms = measured_duration_us / 1000.0
    measured_duration_s = measured_duration_ms / 1000.0

    speed = distance_m / measured_duration_s

    print(
        f"{sleep_time:>7.4f}: ",
        f"{measured_duration_ns:>16.4f}ns → ",
        f"{measured_duration_us:>13.4f}us  → ",
        f"{measured_duration_ms:>10.4f}ms → ",
        f"{measured_duration_s:>7.4f}s → ",
        f"{speed:>9.4f}m/s ",
    )


def main():
    if not btnReset.value:
        # btn Pressed..
        print("timetest start...")
        time_test(0)
        # time_test(0.0)
        # time_test(0.001)
        # time_test(0.01)
        time_test(0.068)
        time_test(0.069)
        time_test(0.07)
        time_test(0.1)
        # time_test(0.2)
        # time_test(0.5)
        # time_test(0.75)
        # time_test(1.0)
        # time_test(2.0)

        print("done.")

print("push button GP21 to run test.")
while True:
    main()
