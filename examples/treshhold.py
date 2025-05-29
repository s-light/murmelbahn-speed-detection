import time
import board
import pulseio
import neopixel

import digitalio
import analogio

print("")
print("io-test.py")


btnReset = digitalio.DigitalInOut(board.GP21)
btnReset.direction = digitalio.Direction.INPUT
btnReset.pull = digitalio.Pull.UP

sensors = [
    {
        "sensor": analogio.AnalogIn(board.A2),
        "last": 0,
        "timestamp": 0,
        "peaked": False,
    },
    {
        "sensor": analogio.AnalogIn(board.A0),
        "last": 0,
        "timestamp": 0,
        "peaked": False,
    },
]


threshold = 18000


def updateSensor(sensorID):
    global sensors
    value = sensors[sensorID]["sensor"].value
    sensors[sensorID]["last"] = value
    if value < threshold:
        sensors[sensorID]["peaked"] = True
        sensors[sensorID]["timestamp"] = time.monotonic_ns()


def resetSensor(sensorID):
    global sensors
    sensors[sensorID]["last"] = 0
    sensors[sensorID]["timestamp"] = 0
    sensors[sensorID]["peaked"] = False


def main():
    global measured_delay

    updateSensor(0)
    updateSensor(1)

    if sensors[0]["peaked"] and sensors[1]["peaked"] :
        measured_delay_ns = sensors[0]["timestamp"] - sensors[1]["timestamp"]
        measured_delay = measured_delay_ns / 1000000

    print(
        f"{sensors[0]["last"]:>5}; {sensors[1]["last"]:>5};",
        f"{(sensors[0]["peaked"]*1000):>10}; {(sensors[1]["peaked"]*1000):>10};",
        f"{(measured_delay):>10}",
    )

    # time.sleep(0.001)

    if not btnReset.value:
        # btn Pressed..
        resetSensor(0)
        resetSensor(1)
        measured_delay = 0


while True:
    main()
