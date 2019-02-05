#include "DualMC33926MotorShield.h"

DualMC33926MotorShield md;

void stopIfFault()
{
  if (md.getFault())
  {
    Serial.println("fault");
     while(1);
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.flush();
  Serial.println("Dual MC33926 Motor Shield");
  md.init();
}

String incomingByte = "";

String m[10];

int i = 0;

void loop()
{
  if (Serial.available()) {
    String string = Serial.readString();
    char str[10];
    string.toCharArray(str, 10);
    char* ptr = strtok(str, " ");
          
    while(ptr != NULL) {
      Serial.println(ptr);
      m[i] = ptr;
      i = i + 1;
      ptr = strtok(NULL, " ");
     }
   }
   
   if(m[0] == "0") {
    Serial.flush();
    md.setM1Speed(0);
    md.setM2Speed(0);
    Serial.println("left = 0");
    Serial.println("right = 0");
   } else if (m[0] == "1") {
    Serial.flush();
    md.setM1Speed(m[1].toInt());
    md.setM2Speed(m[2].toInt());
    Serial.println("left = " + String(m[1]));
    Serial.println("right = " + String(m[2]));
   }

   i = 0;
}
