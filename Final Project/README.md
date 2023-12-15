# Project Report

[**Github Repository**](https://github.com/praneelm89/INFSCI-0201/tree/main/Final%20Project)

## Abstract:
This project implements a SmartHome API using Flask, providing users with the ability to manage various smart home devices such as thermostats, light bulbs, smart vacuums, and smart fridges. The API supports CRUD (Create, Read, Update, & Delte) operations, data persistence, and integrates with a public weather API for enhanced functionality with the Smart Refrigerators. Users can interact with the API to add/remove devices, retrieve device information, and inquire about the temperature difference between the home and outside.

## API Features:

**SmartDevice Class:**
The `SmartDevice` class is an abstract base class (ABC) with attributes such as `device_id`, `device_type`, `manufacturer`, and `location`. It contains an abstract method `to_json()` for serialization and a method `update(data)` to dynamically update object attributes based on the provided data dictionary.

**Thermostat Class:**
Inherits `SmartDevice` and introduces a `temperature` attribute. It has a method `getTemp()` to retrieve the temperature and `to_json()` for serialization.

**SmartVacuum Class:**
Inherits `SmartDevice`, and includes attributes like `binStatus` and `binStatusMessage`. Methods include `to_json()` for serialization, `setBinStatus(binFull)` to set bin status, and `setStatus()` to set a corresponding status message based on bin status.

**SmartFridge Class:**
Inherits `SmartDevice` and introduces attributes like `city` and `currentWeather`. It implements `to_json()` for serialization, `getCity()` to retrieve the city, and interacts with a weather API to fetch current weather conditions, storing them in `currentWeather`.

**LightBulb Class:**
Inherits `SmartDevice` and has a `brightness` attribute. It implements `to_json()` for serialization and `adjust_brightness(value)` to dynamically set the brightness level.

**GarageDoor Class:**
Inherits `SmartDevice`, the `GarageDoor` class includes attributes like `openStatus` and `garageDoorMessage`. Methods include `to_json()` for serialization, `openDoor()` and `closeDoor()` to change the door status, and `setStatus()` to set a corresponding status message.

**Home Class:**
The `Home` class represents a home with attributes such as `address`, `smart_devices`, and `num_smart_devices`. It includes methods like `add_device(dev)`, `get_New_DeviceID()`, `print_devices()`, `update_Device(id, data)`, and `delete_Device(id)` for managing smart devices within the home. The methods facilitate adding, retrieving, printing, updating, and deleting devices.

## Project Idea:
**This Project is an adaptation of project idea #1:**

Implement a SmartHome API that allows owners to run particular operations. The smart home can have various smart home devices such as thermostat, light bulbs, smart vacuum, etc. (all extend from the same parent class). The API should allow users to add/remove smart home devices, list these devices (as an HTML page), alter their information, communicate with them, etc. For example, the API should allow its users to ask: ‘the temperature difference between the home and outside’. To satisfy this functionality, the API should check home’s temperature from Thermostat and consume a public API that provides current temperature outside the home (i.e., providing the home address or allowing the user to provide a new address/zip code). The API saves the home devices to a file. Thus, if the server restarted, the home devices should be created by reading this file. Moreover, the API provides an endpoint for users to view their past activities such that this history should be able to share with the user whenever they want to.


## API Endpoints:
1. `/devices` (GET): Retrieve a list of all devices.
2. `/devices/{device_id}` (GET): Retrieve information about a specific device.
3. `/devices` (POST): Add a new device to the system.
4. `/devices/{device_id}` (PUT): Update information for a specific device.
5. `/devices/{device_id}` (DELETE): Delete a device.
6. `/devices/html` (GET): Retrieve a list of devices in HTML format.

## Data Persistence Decision:
The project uses JSON for data persistence. Device information is serialized to JSON format and stored in files, ensuring easy retrieval and persistence between sessions.

## UML Diagram:
```
+----------------+      +--------------------+       +-------------------+
|   SmartDevice  |<-----|    Thermostat      |       |   SmartVacuum     |
+----------------+      +--------------------+       +-------------------+
| device_id      |      | temperature        |       | binStatus         |
| device_type    |      +--------------------+       +-------------------+
| location       |      | getTemp()          |       | setBinStatus()    |
| manufacturer   |      | to_json()          |       | setStatus()       |
| update()       |      +--------------------+       |                   |
+----------------+                                   +-------------------+

+----------------+      +--------------------+       +-------------------+
|   SmartFridge  |      |    LightBulb       |       |    GarageDoor     |
+----------------+      +--------------------+       +-------------------+
| city           |      | brightness         |       | doorStatus        |
| currentWeather |      +--------------------+       | openDoor()        |
| getCity()      |      | adjust_brightness()|       | closeDoor()       |
| get_weather()  |      | to_json()          |       | setStatus()       |
| setLocalTemp() |      +--------------------+       |                   |
+----------------+                                   +-------------------+

+----------------+
|      Home      |
+----------------+
| address        |
| smart_devices  |
| num_smart_dev  |
| add_device()   |
| get_New_Device |
| print_devices()|
| update_Device()|
| delete_Device()|
+----------------+
```


## Public API
I used the [Weather API](https://www.weatherapi.com/), a free API to retrieve the current weather based on provided location to display on the Smart Refrigerator Screens.