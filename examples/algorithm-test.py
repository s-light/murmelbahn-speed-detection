import time
import board
import pulseio
import neopixel

import digitalio
import analogio

print("")
print("io-test.py")

# sensor1 = digitalio.DigitalInOut(board.GP3)
# sig.direction = digitalio.Direction.INPUT


# Define the analog input pins for the sensors
# sensor0 =
# sensor1 = analogio.AnalogIn(board.A1)
# sensor2 = analogio.AnalogIn(board.A2)
# sensor3 = analogio.AnalogIn(board.A3)

sensors = [
    {
        "sensor": analogio.AnalogIn(board.A0),
        "last": -1,
        "max": -1,
        "timestamp": -1,
        "increasing": False,
        "peaked": False,
    },
    {
        "sensor": analogio.AnalogIn(board.A2),
        "last": 0,
        "max": 0,
        "timestamp": 0,
        "increasing": False,
        "peaked": False,
    },
]

measured_delay = 0


def updateSensor(sensorID):
    global sensors
    value = sensors[sensorID]["sensor"].value
    
    value = value_raw // (65536 / 20)
    # if not sensors[sensorID]["peaked"]:
        # Read the analog value
        sensors[sensorID]["last"] = value
        # Check if the value is increasing
        if value > sensors[sensorID]["max"]:
            sensors[sensorID]["increasing"] = True
            sensors[sensorID]["peaked"] = False
            sensors[sensorID]["max"] = value
            sensors[sensorID]["timestamp"] = time.monotonic_ns()

        # Check if the value has peaked
        elif value < sensors[sensorID]["max"] and sensors[sensorID]["increasing"]:
            sensors[sensorID]["increasing"] = False
            sensors[sensorID]["peaked"] = True
            # print(f"Max at: {sensors[sensorID]["timestamp"]} seconds")
            # sensors[sensorID]["max"] = 0
            # sensors[sensorID]["timestamp"] = None

def resetSensor(sensorID):
    global sensors
    sensors[sensorID]["increasing"] = False
    sensors[sensorID]["peaked"] = False
    sensors[sensorID]["max"] = 0
    sensors[sensorID]["timestamp"] = None


def updateSensorReadings():
    global sensors
    global measured_delay

    # reading0 = sensor0.value // 6553
    # if sensorValues[0]["last"] < reading0:
    #     sensorValues[0]["last"] = reading0
    #     sensorValues[0]["time"] = 0
    # elif sensorValues[0]["last"] > reading0:
    #     sensorValues[0]["time"] = time.monotonic()

    # reading1 = sensor1.value // 6553
    # if sensorValues[1]["last"] < reading1:
    #     sensorValues[1]["last"] = reading1
    #     sensorValues[1]["time"] = 0
    # elif sensorValues[1]["last"] > reading1:
    #     sensorValues[1]["time"] = time.monotonic()

    # if sensorValues[0]["time"] > 0 and sensorValues[1]["time"] > 0:
    #     measured_delay = sensorValues[0]["time"] - sensorValues[1]["time"]
    #     # reset
    #     sensorValues[0]["time"] = 0
    #     sensorValues[0]["last"] = 0
    #     sensorValues[1]["time"] = 0
    #     sensorValues[1]["last"] = 0

    # print(
    #     reading0,
    #     ";",
    #     reading1,
    #     ";",
    #     sensorValues[0]["last"],
    #     ";",
    #     sensorValues[1]["last"],
    #     ";",
    #     measured_delay,
    # )

    updateSensor(0)
    updateSensor(1)
    if sensors[0]["peaked"] and sensors[1]["peaked"] :
        measured_delay_ns = sensors[0]["timestamp"] - sensors[1]["timestamp"]
        measured_delay = measured_delay_ns / 1000000
        resetSensor(0)
        resetSensor(1)
        print(
            f"{sensors[0]["last"]:>5}; {sensors[1]["last"]:>5}; {sensors[0]["max"]:>10}; {sensors[1]["max"]:>10};  {(measured_delay):>10}"
        )
        time.sleep(0.1)
    else: 
        measured_delay = 0
    print(
        f"{sensors[0]["last"]:>5}; {sensors[1]["last"]:>5}; {sensors[0]["max"]:>10}; {sensors[1]["max"]:>10};  {(measured_delay):>10}"
    )


def main():
    updateSensorReadings()
    # print((sensor0.value // 1000),";" ,(sensor1.value // 1000))
    # print((sensor0.value),";" ,(sensor1.value))
    # print(
    #     f"{(sensor0.value//1000):>5}; {(sensor1.value//1000):>5}"
    #     # f"0: {sensor0.value:>5} 1: {sensor1.value:>5} 2: {sensor2.value:>5} 3: {sensor3.value:>5} "
    # )
    # time.sleep(0.001)


while True:
    main()
