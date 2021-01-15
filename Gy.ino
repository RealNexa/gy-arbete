#include <Servo.h>
Servo myServo;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myServo.attach(9);
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT); // INSIDE LED
  pinMode(3, INPUT);  // INSIDE MOVEMENT
  pinMode(4, INPUT); // OUTSIDE MOVEMENT
  pinMode(A1, INPUT); // LIGHT SENSOR
  pinMode(5, OUTPUT); // ALARM SOUND
  pinMode(6, OUTPUT); // ALARM LED
  pinMode(9, OUTPUT); // SERVO
  pinMode(10, OUTPUT);// MOTOR
  pinMode(7, OUTPUT); // OUTSIDE LED
  pinMode(A0, INPUT); // TEMP SENSOR
  
}
String get_sensor_data(){
  int temp = (((analogRead(A0)/1024.0) * 5) - 0.5) * 100;
  delay(5);
  int light = analogRead(A1) / 4;
  delay(5);
  int inside_movement = digitalRead(3);
  delay(5);
  int outside_movement = digitalRead(4);

  String data_to_send = String(String(inside_movement) + "," + String(outside_movement) + "," + String(light) + "," + String(temp));
  return data_to_send;
}

// return "{},{},{},{},{},{}".format(self.inside_led_on, self.outside_led_on, self.alarm_on, self.alarm_led_on, self.motor_on, self.servo_angle)


void get_and_set_data_from_pi(){
    if (Serial.available() > 0){
      String data = Serial.readStringUntil('\n');
      
      int inside_led = data.substring(0, data.indexOf(",")).toInt();
      data.remove(0, data.indexOf(",") + 1);
      int outside_led = data.substring(0, data.indexOf(",")).toInt();
      data.remove(0, data.indexOf(",") + 1);
      int alarm = data.substring(0, data.indexOf(",")).toInt();
      data.remove(0, data.indexOf(",") + 1);
      int alarm_led = data.substring(0, data.indexOf(",")).toInt();
      data.remove(0, data.indexOf(",") + 1);
      int motor = data.substring(0, data.indexOf(",")).toInt();
      data.remove(0, data.indexOf(",") + 1);
      int servo = data.toInt();

      
      digitalWrite(2, inside_led);
      delay(5);
      digitalWrite(7, outside_led);
      delay(5);
      if (alarm){
        tone(5, 3000, 1000);
      }
      delay(5);
      digitalWrite(6, alarm_led);
      delay(5);
      digitalWrite(10,motor);
      delay(5);
      if (servo > 0){
        myServo.write(70);
      } else {
        myServo.write(120);
      }

  }
}


void loop() {
  // put your main code here, to run repeatedly:
  delay(200);
  String data_to_send = get_sensor_data();
  Serial.println(data_to_send); // Order to send data: INSIDE_MOVEMENT, OUTSIDE_MOVEMENT, LIGHT_SENSOR, TEMP
  get_and_set_data_from_pi(); 
}
