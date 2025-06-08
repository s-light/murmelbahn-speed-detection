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


def updateSensor(sensorID):
    global sensors
    value = sensors[sensorID]["sensor"].value
    sensors[sensorID]["last"] = value
    if value < threshold:
        sensors[sensorID]["peaked"] = True
        sensors[sensorID]["timestamp"] = time.monotonic_ns()
        # store as ms
        # sensors[sensorID]["timestamp"] = time.monotonic_ns() / (1000.0 * 1000.0) 
        # sensors[sensorID]["timestamp"] = time.monotonic()


def resetSensor(sensorID):
    global sensors
    sensors[sensorID]["last"] = 0
    sensors[sensorID]["timestamp"] = 0
    sensors[sensorID]["peaked"] = False


def printLog():
    print(
        f"{(sensors[0]["last"]/100):>5.2f}; {(sensors[1]["last"]/100):>5.2f};",
        f"{(sensors[0]["peaked"]*600):>10}; {(sensors[1]["peaked"]*600):>10};",
        f"{(measured_duration_s):>10.4f}s;",
        f"{(speed):>10.4f}m/s;",
    )


def main():
    global measured_duration_us
    global measured_duration_ms
    global measured_duration_s
    global speed

    updateSensor(0)
    updateSensor(1)

    if sensors[0]["peaked"] and sensors[1]["peaked"]:
        measured_duration_ns = sensors[1]["timestamp"] - sensors[0]["timestamp"]
        print("measured_duration_ns", measured_duration_ns)
        measured_duration_us = measured_duration_ns / 1000.0
        print("measured_duration_us", measured_duration_us)
        measured_duration_ms = measured_duration_us / 1000.0
        # measured_duration_ms = sensors[1]["timestamp"] - sensors[0]["timestamp"]
        print("measured_duration_ms", measured_duration_ms)
        measured_duration_s = measured_duration_ms / 1000.0
        # measured_duration_s = sensors[1]["timestamp"] - sensors[0]["timestamp"]
        print("measured_duration_s", measured_duration_s)
        speed = distance_m / measured_duration_s
        printLog()
        time.sleep(0.1)
        # wait until button is pressed.
        while btnReset.value:
            time.sleep(0)
        resetSensor(0)
        resetSensor(1)

    printLog()

    # time.sleep(0.001)

    if not btnReset.value:
        # btn Pressed..
        resetSensor(0)
        resetSensor(1)
        measured_duration_us = 0
        measured_duration_ms = 0
        measured_duration_s = 0
        measured_delay = 0
        speed = 0


while True:
    main()
