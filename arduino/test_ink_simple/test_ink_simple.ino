// /*
// sketch to test ink shield on uno board by Serial comand
// */
// #include <InkShield.h>         // #include <InkShieldMega.h>
// InkShieldA0A3 MyInkShield(2);  // find out, why 2 pin is
// void setup() {
//   Serial.begin(115200);
// }

// void loop() {
//   if (Serial.available()) {

//     Serial.write(Serial.read());
//     // uint16_t pattern = 0b0011001100110011;
//     // // Serial.read() | (Serial.read() << 8);
//     // MyInkShield.spray_ink(pattern);
//     // Serial.print(pattern);
//     // delay(1000);
//     // if (Serial.read() == 'a') {
//     //   MyInkShield.spray_ink(0b0011111111111111);
//     //   delay(20);
//     // }
//     // else {
//     // Serial.readBytes()
//     // }
//   }
// }

#include <InkShield.h>
InkShieldA0A3 MyInkShield(2);
int x;
void setup() {
  Serial.begin(115200);
  // Serial.setTimeout(1);
  // delay(500);
  // uint8_t tt =  0b11000000;
  // uint8_t tt2 = 0b00000001;
  // MyInkShield.spray_ink2((uint16_t(tt2) << 8) | (uint16_t(tt)));
}
void loop() {
  if (Serial.available()) {
  uint8_t tt[1] =  {0b00000000};
  uint8_t tt2[1] = {0b00000000};
  uint8_t tt3[2] = {0b00000000,0b00000000};
  Serial.readBytes(tt3,2);
  MyInkShield.spray_ink2((uint16_t(tt3[0]) << 8) | (uint16_t(tt3[1])));


    // delay(100);
    // char chek1 = Serial.read();
    // delayMicroseconds(200);
    // char chek2 = Serial.read();
    // delayMicroseconds(100);
    // word result = ((word(chek1)) << 8) | (word(chek2));
    // word result2 = 0b0000000110000000;

    // char tt = 0b00000001;
    // MyInkShield.spray_ink2(word(chek1));
    // // Serial.print(' ');
    // Serial.print(result, HEX);
  }
}




//  char first_pat = Serial.read();
// word rlen = Serial.readBytes(buf, 2);
// Serial.println(word(buf[0]));
// Serial.println(buf[1]);

//   word test = (word(buf[1]) | (word(buf[0])<<8))>>4 ;
// Serial.println(word(buf[1]));
// Serial.println(word(buf[0]));
// Serial.println(test);


// word first = Serial.read();
// Serial.read();
// Serial.read();
// word second = Serial.read();
// Serial.println(first);
// Serial.println(second);
// uint8_t second_pat = Serial.read();
// uint16_t pattern = first_pat | (second_pat << 8);


//  x = Serial.readString().toInt();
//
// MyInkShield.spray_ink(test);
// Serial.print(second_pat);
//  Serial.print(second_pat);
// Serial.print(second_pat);