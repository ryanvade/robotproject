void setup()
{
        //start a serial connection
		Serial.begin(115200);
		//following is for LED test
        pinMode(13, OUTPUT);
        digitalWrite(13, LOW);
}
 
void loop()
{		//can we connect to the serial port?
        if(Serial.available() > 0)
        {
                byte data = Serial.read();
                Serial.write(data);
 
                if(data == 1)
                        digitalWrite(13, HIGH);
                if(data == 0)
                        digitalWrite(13, LOW);
 
                Serial.flush();
        }
}
