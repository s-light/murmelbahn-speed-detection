import time
import board
import pulseio
import neopixel

import digitalio
import analogio

print("")
print("io-test.py")

# Define the analog input pins for the sensors
sensor0 = analogio.AnalogIn(board.A0)
sensor1 = analogio.AnalogIn(board.A2)


def main():
    # print((sensor0.value // 1000),";" ,(sensor1.value // 1000))
    # print((sensor0.value),";" ,(sensor1.value))
    print(f"{(sensor0.value):>5}; {(sensor1.value):>5}")
    # print(
    #     # f"0: {sensor0.value:>5} 1: {sensor1.value:>5} 2: {sensor2.value:>5} 3: {sensor3.value:>5} "
    # )
    # time.sleep(0.001)


while True:
    main()
