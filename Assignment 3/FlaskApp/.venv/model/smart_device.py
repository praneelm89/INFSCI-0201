import json
from abc import ABC, abstractmethod

class SmartDevice(ABC):
    def __init__(self, name, manufacturer):
        self.name = name
        self.manufacturer = manufacturer

    @abstractmethod
    def to_json(self):
        pass



class LightBulb(SmartDevice):
    def __init__(self, name, manufacturer, brightness):
        super().__init__(name, manufacturer)
        self.brightness = brightness
    
    def to_json(self):
        lightBulb_dict = {
            'name' : self.name,
            'manufacturer' : self.manufacturer,
            'brightness' : self.brightness
        }
        return json.dumps(lightBulb_dict)
    
    def adjust_brightness(self, value):
        self.brightness = value
        print("Brightness is set to", value)



class Home:
    def __init__(self, address):
        self.address = address
        self.smart_devices = []

    def add_device(self, dev):
        self.smart_devices.append(dev)
    #    dev.connect_to_network()       // would only work if lightBulb has connect_to_network() method defined, but this is not specified in the UML class diagram. Check with Kamil
        
    def print_devices(self):
        for device in self.smart_devices:
            print(device.to_json())