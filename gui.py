import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import time
from management import DataManager, SerialManager

class RequestWorker(qtc.QThread):

    data_receved = qtc.pyqtSignal(dict)

    def __init__(self):
        self.thread_running = 0
        self.serial_manager = SerialManager("COM5", 9600)
        self.serial_manager.serial_comm.close()
        self.data_manager = DataManager()
        super().__init__()

    def run(self):
        self.serial_manager.serial_comm.close()
        self.serial_manager.serial_comm.open()
        self.thread_running = 1
        while self.thread_running == 1:
            data = self.serial_manager.get_data()
            if data is not None:
                self.data_manager.security_on = mw.security_toggle.isChecked()
                self.data_manager.manual_motor_on = mw.motor_toggle.isChecked()
                self.data_manager.motor_override = mw.motor_manual_override.isChecked()
                # self.data_manager._print_value()
                self.data_manager.input_data_from_arduino(data)
                self.data_manager.process_data()
                processed_data = self.data_manager.get_data()
                self.serial_manager.send_data(processed_data)

                self.data_receved.emit(
                    {
                        "i_movement": self.data_manager.inside_movement,
                        "o_movement": self.data_manager.outside_movement,
                        "light_level": self.data_manager.light_sensor_value,
                        "temp": self.data_manager.temp_value,
                        "inside_led": self.data_manager.inside_led_on,
                        "servo_angle": self.data_manager.servo_angle,
                        "motor": self.data_manager.motor_on,
                        "alarm_sound": self.data_manager.alarm_on,
                        "alarm_led": self.data_manager.alarm_led_on,
                        "outside_led": self.data_manager.outside_led_on,
                        "security": self.data_manager.security_on
                     }
                )
            time.sleep(0.1)





    def stop(self):
        self.thread_running = 0
        self.serial_manager.serial_comm.close()


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()

        # Adds a layout to parent widget
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)


        self._connection_status_label = qtw.QLabel(self, text="Connection Status: ")

        self.connection_status_label = qtw.QLabel(self, text="Not Connected")
        self.connection_status_label.setStyleSheet("color: red")
        connection_layout = qtw.QHBoxLayout()
        connection_layout.addWidget(self._connection_status_label)
        connection_layout.addWidget(self.connection_status_label)
        layout.addLayout(connection_layout)



        self._light_label = qtw.QLabel(self, text="Light Level: ")
        self.light_label = qtw.QLabel(self, text="Not Connected")
        self.light_layout = qtw.QHBoxLayout()
        self.light_layout.addWidget(self._light_label)
        self.light_layout.addWidget(self.light_label)
        layout.addLayout(self.light_layout)

        self._temp_label = qtw.QLabel(self, text="Temperature: ")
        self.temp_label = qtw.QLabel(self, text="Not Connected")
        self.temp_layoyt = qtw.QHBoxLayout()
        self.temp_layoyt.addWidget(self._temp_label)
        self.temp_layoyt.addWidget(self.temp_label)
        layout.addLayout(self.temp_layoyt)

        self._servo_label = qtw.QLabel(self, text="Servo Angle: ")
        self.servo_label = qtw.QLabel(self, text="Not Connected")
        self.servo_layout = qtw.QHBoxLayout()
        self.servo_layout.addWidget(self._servo_label)
        self.servo_layout.addWidget(self.servo_label)
        layout.addLayout(self.servo_layout)

        self._inside_movement_label = qtw.QLabel(self, text="Inside Movement: ")
        self.inside_movement_label = qtw.QLabel(self, text="Not Connected")
        self.inside_movement_layout = qtw.QHBoxLayout()
        self.inside_movement_layout.addWidget(self._inside_movement_label)
        self.inside_movement_layout.addWidget(self.inside_movement_label)
        layout.addLayout(self.inside_movement_layout)

        self._outside_movement_label = qtw.QLabel(self, text="Outside Movement: ")
        self.outside_movement_label = qtw.QLabel(self, text="Not Connected")
        self.outside_movement_layout = qtw.QHBoxLayout()
        self.outside_movement_layout.addWidget(self._outside_movement_label)
        self.outside_movement_layout.addWidget(self.outside_movement_label)
        layout.addLayout(self.outside_movement_layout)

        self._outside_led_label = qtw.QLabel(self, text="Outside LED: ")
        self.outside_led_label = qtw.QLabel(self, text="Not Connected")
        self.outside_led_layout = qtw.QHBoxLayout()
        self.outside_led_layout.addWidget(self._outside_led_label)
        self.outside_led_layout.addWidget(self.outside_led_label)
        layout.addLayout(self.outside_led_layout)

        self._inside_led_label = qtw.QLabel(self, text="Inside LED: ")
        self.inside_led_label = qtw.QLabel(self, text="Not Connected")
        self.inside_led_layout = qtw.QHBoxLayout()
        self.inside_led_layout.addWidget(self._inside_led_label)
        self.inside_led_layout.addWidget(self.inside_led_label)
        layout.addLayout(self.inside_led_layout)

        self._motor_label = qtw.QLabel(self, text="Fan: ")
        self.motor_label = qtw.QLabel(self, text="Not Connected")
        self.motor_toggle = qtw.QCheckBox(text="On")
        self.motor_manual_override = qtw.QCheckBox(text="Manual Control")
        self.motor_manual_override.stateChanged.connect(self.motor_toggle.setCheckable)
        self.motor_layout = qtw.QHBoxLayout()
        self.motor_layout.addWidget(self._motor_label)
        self.motor_layout.addWidget(self.motor_label)
        self.motor_layout.addWidget(self.motor_toggle)
        self.motor_layout.addWidget(self.motor_manual_override)
        layout.addLayout(self.motor_layout)

        self._security_label = qtw.QLabel(self, text="Secutiry: ")
        self.security_label = qtw.QLabel(self, text="Not Connected")
        self.security_toggle = qtw.QCheckBox(text="On")
        self.security_layoyt = qtw.QHBoxLayout()
        self.security_layoyt.addWidget(self._security_label)
        self.security_layoyt.addWidget(self.security_label)
        self.security_layoyt.addWidget(self.security_toggle)
        layout.addLayout(self.security_layoyt)

        self._alarm_sound_label = qtw.QLabel(self, text="Alarm Sound: ")
        self.alarm_sound_label = qtw.QLabel(self, text="Not Connected")
        self.alarm_sound_layoyt = qtw.QHBoxLayout()
        self.alarm_sound_layoyt.addWidget(self._alarm_sound_label)
        self.alarm_sound_layoyt.addWidget(self.alarm_sound_label)
        layout.addLayout(self.alarm_sound_layoyt)

        self._alarm_led_label = qtw.QLabel(self, text="Alarm Led: ")
        self.alarm_led_label = qtw.QLabel(self, text="Not Connected")
        self.alarm_led_layoyt = qtw.QHBoxLayout()
        self.alarm_led_layoyt.addWidget(self._alarm_led_label)
        self.alarm_led_layoyt.addWidget(self.alarm_led_label)
        layout.addLayout(self.alarm_led_layoyt)



        grid_layout = qtw.QGridLayout()
        layout.addLayout(grid_layout)

        start_button = qtw.QPushButton(self)
        start_button.setText("Connect")
        start_button.clicked.connect(self.start_connection)
        grid_layout.addWidget(start_button, 0, 0)

        stop_button = qtw.QPushButton(self)
        stop_button.setText("Disconnect")
        stop_button.clicked.connect(self.stop_connection)
        grid_layout.addWidget(stop_button, 0, 1)




        self.worker = RequestWorker()
        self.worker.data_receved.connect(self.set_labels)

        self.show()


    def set_labels(self, data):
        self.light_label.setText(str(data["light_level"]))
        self.temp_label.setText(str(data["temp"]) + " \u00B0C")
        self.inside_movement_label.setText(str(data["i_movement"]))
        self.outside_movement_label.setText(str(data["o_movement"]))
        self.servo_label.setText(str(data["servo_angle"]))
        self.outside_led_label.setText(str(data["outside_led"]))
        self.inside_led_label.setText(str(data["inside_led"]))
        self.motor_label.setText(str(data["motor"]))
        self.security_label.setText(str(data["security"]))
        self.alarm_sound_label.setText(str(data["alarm_sound"]))
        self.alarm_led_label.setText(str(data["alarm_led"]))

    def start_connection(self):
        self.worker.start()
        self.connection_status_label.setText("Connected")
        self.connection_status_label.setStyleSheet("color: green")

    def stop_connection(self):
        self.worker.stop()
        self.connection_status_label.setText("Not Connected")
        self.connection_status_label.setStyleSheet("color: red")


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
