#include <SoftwareSerial.h>

SoftwareSerial epir(6,7);  // create SoftwareSerial to talk to the EPIR  (RX, TX)
String buffer;//buffer string to hold each digit
String result;

void setup()
{
  Serial.begin(9600);
  epir.begin(9600);
  pinMode(4,OUTPUT);
  
  
}
void loop()
{
  digitalWrite(4,1);
  
  
        while (Serial.available() > 0)
        {
                char c = Serial.read();  //gets one byte (one digit) from serial buffer
                buffer += c; //adds digit to string
                delay(2);  //give buffer time to fill. probably not needed
        }
 
         if (buffer.length() > 0)
        {
                Serial.println("+<" + buffer + ">");  //Print the assembled string. Should match what was sent
                int n = buffer.toInt();  //convert buffer into an integer
 
                epir.write(n); //write the angle to the sensor
               
                Serial.print("Rcv: "); //print the ack/nack message or present value (depending on command)
                buffer=""; //clear string for future input
                while (epir.available() > 0)
                {
                        char c = epir.read();  //gets one byte (one digit) from serial buffer
                        result += c; //adds digit to string
                        delay(2);  //give buffer time to fill. probably not needed
                }
                Serial.println(result);
                result = "";
        }
}

