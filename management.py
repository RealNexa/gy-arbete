import threading
import time
import serial
import statistics


class AlarmManager():

    def __init__(self):
        self.alarm_on = False

    def on(self):
        self.alarm_on = True

    def off(self):
        self.alarm_on = False

    def alarm_status(self):
        return self.alarm_on




class DataManager():
    def __init__(self):
        # INPUT FROM ARDUINO
        self.inside_movement = False
        self.outside_movement = False

        self.light_sensor_value_list = []
        self.light_sensor_value = 0

        self.temp_value_list = []
        self.temp_value = 0

        # OUTPUT TO ARDUINO
        self.inside_led_on = False
        self.servo_angle = 0
        self.motor_on = False
        self.alarm_on = False
        self.alarm_led_on = False
        self.outside_led_on = False

        self.security_on = False
        self.manual_motor_on = False
        self.motor_override = False

    def input_data_from_arduino(self, data):
        try:
            data = data.decode("utf-8")
            data = data.split(",")
            if int(data[0]) == 0:
                self.inside_movement = False
            else:
                self.inside_movement = True

            if int(data[1]) == 0:
                self.outside_movement = False
            else:
                self.outside_movement = True

            self.light_sensor_value_list.append(int(data[2]))
            self.temp_value_list.append(int(data[3]))
        except:
            pass


    def process_data(self):
        # CHANGE WHAT HAPPENS FOR DIFFERENT EVENTS

        # self.motor_on = self.temp_value > 24

        # self.alarm_on = self.inside_movement and self.security_on
        # self.alarm_led_on = self.inside_movement and self.security_on

        self.inside_led_on = self.inside_movement and not self.security_on
        self.outside_led_on = self.outside_movement

        self.servo_angle = 180 if self.light_sensor_value > 50 else 0

        if len(self.temp_value_list) > 50:
            self.temp_value_list.pop(0)
        self.temp_value = int(statistics.mean(self.temp_value_list))

        if len(self.light_sensor_value_list) > 50:
            self.light_sensor_value_list.pop(0)
        self.light_sensor_value = int(statistics.mean(self.light_sensor_value_list))


        # Security
        if self.security_on and self.inside_movement:
            self.alarm_on = True
            self.alarm_led_on = True

        if not(self.security_on):
            self.alarm_on = False
            self.alarm_led_on = False

        # Fan/AC
        if not self.motor_override:
            self.motor_on = self.temp_value > 24
        elif self.motor_override:
            self.motor_on = self.manual_motor_on


    def get_data(self):
        return "{},{},{},{},{},{}\n".format(1 if self.inside_led_on else 0,
                                          1 if self.outside_led_on else 0,
                                          1 if self.alarm_on else 0,
                                          1 if self.alarm_led_on else 0,
                                          1 if self.motor_on else 0,
                                          self.servo_angle)

    def _print_value(self):
        print("\n"*10)
        print("Inside Movement:", self.inside_movement)
        print("Outside Movement:", self.outside_movement)
        print("Light Sensor Value", self.light_sensor_value)
        print("Temperature:", self.temp_value)
        print("Inside Led:", self.inside_led_on)
        print("Servo Angle:", self.servo_angle)
        print("Motor:", self.motor_on)
        print("Alarm Sound:", self.alarm_on)
        print("Alarm_LED:", self.alarm_led_on)
        print("Outside Led", self.outside_led_on)






class SerialManager():

    def __init__(self, serial_port, baud_rate):
        # Initialize serial port
        self.serial_comm = serial.Serial(serial_port, baud_rate)
        self.servo = 0

    def get_data(self):
        if self.serial_comm.in_waiting > 0:
            line = self.serial_comm.readline()
            return line

    def send_data(self, data):
        self.serial_comm.write(data.encode())


if __name__ == '__main__':

    serial_manager = SerialManager("COM5", 9600)
    data_manager = DataManager()

    while True:
        data = serial_manager.get_data()
        if data is not None:
            print("GOT DATA")
            data_manager._print_value()
            data_manager.input_data_from_arduino(data)
            data_manager.process_data()
            processed_data = data_manager.get_data()
            serial_manager.send_data(processed_data)
        time.sleep(0.5)



"""
d = SerialManager()


def thread_function():
    while True:
        time.sleep(1)
        print(d.get_data())


t = threading.Thread(target=thread_function)

t.start()

while True:
    d.set_data(int(input("Set servo value to: ")))
"""