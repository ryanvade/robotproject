#include <SoftwareSerial.h>

SoftwareSerial ss(6,7);  // create SoftwareSerial to talk to the EPIR
String buffer; //buffer string to hold each digit

void setup()
{
  Serial.begin(9600);
  ss.begin(9600);
}
 
void loop()
{
        while (Serial.available() > 0)
        {
                char c = Serial.read();  //gets one byte (one digit) from serial buffer
                buffer += c; //adds digit to string
                delay(2);  //give buffer time to fill. probably not needed
        }
 
        if (buffer.length() > 0)
        {
                Serial.println("+<" + buffer + ">");  //Print the assembled string. Should match what was sent
               // int n = buffer.toInt();  //convert buffer into an integer
 
                ss.write(buffer); //write the angle to the sensor
                
                Serial.print("Rcv: "); //print the ack/nack message or present value (depending on command)
                Serial.println(ss.read());
                
                buffer=""; //clear string for future input
        }
}
