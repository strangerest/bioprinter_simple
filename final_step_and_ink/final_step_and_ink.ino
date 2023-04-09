#include <InkShield.h>
#include <AccelStepper.h>

InkShieldA0A3 MyInkShield(2);
// -------- motor begin ----------//
AccelStepper stepper_x(AccelStepper::FULL2WIRE, 3, 6);
AccelStepper stepper_y(AccelStepper::FULL2WIRE, 4, 7);

float string_weight =8.3;

float mm_in_steps = 20000 / 99;
float x_step = mm_in_steps /4;       // 1 mm in steps = 10000/58
float y_step = (mm_in_steps / 4) * string_weight;  // 1 mm in steps = 10000/58
float x_coor=0;
float y_coor=0;
float move_speed = 5000000;

float x_pix_size;

void config_motors(float speed = 5000, float acceleration = 50000000) {
  stepper_x.setMaxSpeed(speed);
  stepper_x.setSpeed(speed);
  stepper_x.setAcceleration(acceleration);

  stepper_y.setMaxSpeed(speed);
  stepper_y.setSpeed(speed);
  stepper_y.setAcceleration(acceleration);
}
// -------- motor end ----------//

//---------- buffer ------------//
uint8_t buffer[1000];

void setup() {
  Serial.begin(115200);
  config_motors(move_speed);

  // MyInkShield.spray_ink(uint16_t(0b1111111111)); // uncoment to check ink
}


void loop() {

  // be here til serial comunication
  while (Serial.available() == 0) {
    delayMicroseconds(1);
  }

  if (Serial.available()) {
    x_pix_size = Serial.parseInt();
    Serial.read(); // read spase betwing number of bytest and bytearray

    Serial.readBytes(buffer, int(x_pix_size));  // put pixels in buffer

    // print line of 12 pixels
    for (int i = 0; i < int(x_pix_size); i++) {
      // uint16_t poop_ink_patern = (uint16_t(uint16_t(buffer[i])) << 8) | (uint16_t(buffer[i+1]));
       uint16_t poop_ink_patern = uint16_t(buffer[i]);
      MyInkShield.spray_ink(poop_ink_patern);

      x_coor += x_step;
      stepper_x.moveTo(x_coor);
      stepper_x.runToPosition();

    }

    // move to next line
    y_coor += y_step;
    stepper_y.moveTo(y_coor);
    stepper_y.runToPosition();

    x_coor = 0;
    stepper_x.moveTo(x_coor);
    stepper_x.runToPosition();
  }
  Serial.write('n');  // send n symbol to say that we are ready to get next pack
}


