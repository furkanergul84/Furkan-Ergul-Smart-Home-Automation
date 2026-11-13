"""Demonstration of the Smart Home Automation System (Stage 1).

Run with:  python main.py
"""

from smart_home import (
    AlarmSystem,
    Camera,
    Controller,
    DeviceOffError,
    House,
    InvalidValueError,
    Light,
    MotionSensor,
    SmokeSensor,
    TemperatureSensor,
    Thermostat,
)


def build_demo_house() -> House:
    """Create a sample house with rooms, devices and sensors."""
    house = House("My Smart Home")

    living_room = house.add_room("Living Room")
    living_room.add_device(Light("Ceiling Light", power_watts=60))
    living_room.add_device(Light("Reading Lamp", power_watts=15, brightness=40))
    living_room.add_device(Thermostat("Living Thermostat", target_temperature=22))
    living_room.add_sensor(TemperatureSensor("Living Temp Sensor"))
    living_room.add_sensor(SmokeSensor("Living Smoke Sensor"))

    bedroom = house.add_room("Bedroom")
    bedroom.add_device(Light("Bedside Lamp", power_watts=8, brightness=30))
    bedroom.add_device(Thermostat("Bedroom Thermostat", target_temperature=19))
    bedroom.add_sensor(TemperatureSensor("Bedroom Temp Sensor"))

    entrance = house.add_room("Entrance")
    entrance.add_device(Camera("Door Camera"))
    entrance.add_device(AlarmSystem("Main Alarm"))
    entrance.add_sensor(MotionSensor("Door Motion Sensor"))

    return house


def main() -> None:
    house = build_demo_house()
    controller = Controller(house)

    print("1) Initial state - everything is OFF")
    print(controller.status_report())

    print("\n2) Turning on Living Room and Entrance devices")
    controller.turn_on_room("Living Room")
    controller.turn_on_room("Entrance")

    print("\n3) Sensors report new readings, controller updates thermostats")
    living = house.get_room("Living Room")
    living.sensors_of_type(TemperatureSensor)[0].record(18.5)
    living.sensors_of_type(SmokeSensor)[0].record(2)
    house.get_room("Bedroom").sensors_of_type(TemperatureSensor)[0].record(20.0)
    controller.update_thermostats()

    print("\n4) Camera starts recording, alarm is armed")
    camera = controller.devices_of_type(Camera)[0]
    alarm = controller.devices_of_type(AlarmSystem)[0]
    camera.start_recording()
    alarm.arm()

    print(controller.status_report())

    print("\n5) Validation and errors (encapsulation protects the objects)")
    lamp = controller.find_devices_by_name("reading")[0]
    try:
        lamp.brightness = 150
    except InvalidValueError as error:
        print(f"   InvalidValueError -> {error}")

    spare_camera = Camera("Spare Camera")  # created but never turned on
    try:
        spare_camera.start_recording()
    except DeviceOffError as error:
        print(f"   DeviceOffError    -> {error}")

    print("\n6) Polymorphism: same call, different behaviour per device type")
    for device in house.all_devices:
        print(f"   {device.device_type:<11} {device.name:<20} -> {device.current_power:7.1f} W")
    print(f"   TOTAL HOUSE POWER: {house.current_power:.1f} W")

    print("\n7) Turning everything off")
    controller.turn_off_all()
    print(f"   {house}")


if __name__ == "__main__":
    main()
