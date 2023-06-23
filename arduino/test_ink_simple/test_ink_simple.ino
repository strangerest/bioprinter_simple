#include <InkShield.h>
InkShieldA0A3 MyInkShield(2);
int x;
void setup() {
  Serial.begin(115200);
}
void loop() {
  MyInkShield.spray_ink2(0b111111111111);
  if (Serial.available()) {
  uint8_t tt[1] =  {0b00000000};
  uint8_t tt2[1] = {0b00000000};
  uint8_t tt3[2] = {0b00000000,0b00000000};
  Serial.readBytes(tt3,2);
  MyInkShield.spray_ink2((uint16_t(tt3[0]) << 8) | (uint16_t(tt3[1])));
  }
}