import time
import board
import pulseio
import neopixel

import digitalio
import analogio

print("")
print("io-test.py")

# Define the analog input pins for the sensors
# possible pins:
# board.A0 board.GP26 board.GP26_A0 (GPIO26)
# board.A1 board.GP27 board.GP27_A1 (GPIO27)
# board.A2 board.GP28 board.GP28_A2 (GPIO28)

sensor0 = analogio.AnalogIn(board.GP26_A0)
sensor1 = analogio.AnalogIn(board.GP27_A1)
sensor2 = analogio.AnalogIn(board.GP28_A2)


def main():
    # print((sensor0.value // 1000),";" ,(sensor1.value // 1000))
    # print((sensor0.value),";" ,(sensor1.value))
    print(f"{sensor0.value:>5}; {sensor1.value:>5}; {sensor2.value:>5}")
    # print(
    #     # f"0: {sensor0.value:>5} 1: {sensor1.value:>5} 2: {sensor2.value:>5} 3: {sensor3.value:>5} "
    # )
    # time.sleep(0.001)


while True:
    main()
