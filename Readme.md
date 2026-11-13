# Smart Home Automation System – Stage 1

[![Tests](https://github.com/furkanergul84/Furkan-Ergul-Smart-Home-Automation/actions/workflows/tests.yml/badge.svg)](https://github.com/furkanergul84/Furkan-Ergul-Smart-Home-Automation/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

**Course:** Object Based Programming (2019G0005), İstanbul Esenyurt University
**Lecturer:** Dr. Coşkun Şahin
**Student:** Furkan Ergül
**Assignment:** #8 Smart Home Automation System (Midterm – Stage 1: Architecture)

A smart home simulation written in Python using Object-Oriented Programming.
Stage 1 models the main components of a smart home:

- **Device** (abstract) → **Light**, **Thermostat**, **Camera**, **AlarmSystem**
- **Sensor** (abstract) → **TemperatureSensor**, **MotionSensor**, **SmokeSensor**
- **Room** – holds devices and sensors
- **House** – made of rooms
- **Controller** – controls the whole house (switching, searching, reporting)

The design of each class and the OOP principles used are explained in
[Report_01.md](Report_01.md), together with the UML class diagram.

---

## Requirements

- **Python 3.10 or newer** ([python.org/downloads](https://www.python.org/downloads/))
- No external libraries are needed (only the Python standard library is used).

Check your Python version:

```bash
python --version
```

## Setup

```bash
git clone https://github.com/furkanergul84/Furkan-Ergul-Smart-Home-Automation.git
cd Furkan-Ergul-Smart-Home-Automation
```

## Running the demo

```bash
python main.py
```

The demo builds a sample house (Living Room, Bedroom, Entrance), turns devices
on, feeds sensor readings to the thermostats, records with the camera, arms
the alarm, shows validation errors and prints the power consumption of every
device. A shortened sample output:

```text
=== House 'My Smart Home' (3 rooms, 2074.0 W) ===

Room 'Living Room' (3 devices, 2 sensors, 2066.0 W)
   [Light      ] Ceiling Light        ON  | brightness 100%
   [Light      ] Reading Lamp         ON  | brightness 40%
   [Thermostat ] Living Thermostat    ON  | target 22.0°C, now 18.5°C, heating
   <TemperatureSensor> Living Temp Sensor: 18.5°C
   <SmokeSensor> Living Smoke Sensor: 2%
...
5) Validation and errors (encapsulation protects the objects)
   InvalidValueError -> Brightness must be between 0 and 100.
   DeviceOffError    -> Cannot start recording: 'Spare Camera' is OFF.
```

## Running the tests

```bash
python -m unittest -v
```

33 unit tests cover the devices, sensors, rooms, house and controller.
The tests also run automatically on GitHub Actions on every push (see the badge above).

## Using the classes in your own code

```python
from smart_home import House, Controller, Light, Thermostat, TemperatureSensor

house = House("My Home")
kitchen = house.add_room("Kitchen")
kitchen.add_device(Light("Kitchen Light", power_watts=40))
kitchen.add_device(Thermostat("Kitchen Thermostat", target_temperature=21))
kitchen.add_sensor(TemperatureSensor("Kitchen Temp"))

controller = Controller(house)
controller.turn_on_room("Kitchen")
print(controller.status_report())
```

## Project structure

```text
.
├── main.py                  # demonstration script
├── smart_home/              # the package
│   ├── __init__.py          # public API of the package
│   ├── devices.py           # Device (abstract), Light, Thermostat, Camera, AlarmSystem
│   ├── sensors.py           # Sensor (abstract), TemperatureSensor, MotionSensor, SmokeSensor
│   ├── room.py              # Room
│   ├── house.py             # House
│   ├── controller.py        # Controller
│   └── exceptions.py        # custom exceptions
├── tests/                   # unit tests (unittest)
├── .github/workflows/       # GitHub Actions: runs the tests on every push
├── Readme.md                # this file
└── Report_01.md             # OOP report + UML diagram
```

## Roadmap

| Stage | Content | Status |
|---|---|---|
| 1 | Architecture: Device, Sensor, Controller, Room, House, device inheritance | ✅ Done |
| 2 | Automation rules (temperature threshold → heater), energy log per room, sorting devices | Planned |
| 3 | Event-driven design (SensorTriggeredEvent), web pages, scheduling, emergency alerts | Planned |
