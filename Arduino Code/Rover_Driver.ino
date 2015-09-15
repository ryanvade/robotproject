
#include <avr/wdt.h> //library to use watchdog timers for AVR chips

/*
Motor pins in order:
Motor 1 PWM
Motor 2 PWM
Motor 3 PWM
Motor 4 PWM
Motor 1 direction
Motor 2 direction
Motor 3 direction
Motro 4 direction

PWM = pulse width modulation, used to control speed
direction = CW or CCW rotation of the motors
*/
#define    M1_PWM                46
#define    M2_PWM                 9
#define    M3_PWM                44
#define    M4_PWM                 3
#define    M1_DIR                 7
#define    M2_DIR                 2
#define    M3_DIR                 8
#define    M4_DIR                10

/*
Pins for the HC-SR04 ultrasonic sensor
Trigger pin to send out a ultrasonic pulse.
Echo pin to listen for the pulse echo.
*/
#define    SONAR_TRIG             6
#define    SONAR_ECHO             5

/*
Encoder input pins used to trigger encoder count interrupts.
*/
#define    ENCODER_A              21
#define    ENCODER_B              20

/*
Command characters and event characters:
d = request to use drive function.
p = request to use ping function
h = request to use halt function
t = request to use turn function
e = request encoder count
x = error event occurred
b = heartbeat signal character
\r = terminating character for packet data
*/
const char     DRIVE_CODE    =    'd';
const char     PING_CODE     =    'p';
const char     HALT_CODE     =    'h';
const char     TURN_CODE     =    't';
const char     ENC_CODE      =    'e';
const char     ERR_CODE      =    'x';
const char     HTBT_CODE     =    'b';
const char     TERMINATOR    =    '\r';

/*
Encoder count variable. This count can go negative.
*/
long int count = 0;

int j = 0;

void setup()
{
  Serial.begin(19200);  //start UART0 with a baud of 19200 Bps
  wdt_enable (WDTO_8S); //enable the watchdog timer at 8S countdown
  
  /*
  Set the drive mode of all of the motor pins to output.
  Motors do not have any feedback so no input pin is needed
  */
  pinMode(M1_DIR, OUTPUT);
  pinMode(M2_DIR, OUTPUT);
  pinMode(M3_DIR, OUTPUT);
  pinMode(M4_DIR, OUTPUT);
  pinMode(M1_PWM, OUTPUT);
  pinMode(M2_PWM, OUTPUT);
  pinMode(M3_PWM, OUTPUT);
  pinMode(M4_PWM, OUTPUT);
  
  /*
  Set the drive mode for the ultrasonic sensor.
  Trigger is used to create a pulse, so must be an output.
  Echo is used to sense a response so it must be input.
  */
  pinMode(SONAR_TRIG, OUTPUT);
  pinMode(SONAR_ECHO, INPUT);
  
  /*
  ISR #2 is attached to pin 21. Routine ljmps to ecount funtion
  */
  attachInterrupt(2, ecount, RISING);
  
  /*
  Initialize all of the motors to 0 (ie. off)
  */
  analogWrite(M1_PWM, 0);
  analogWrite(M2_PWM, 0);
  analogWrite(M3_PWM, 0);
  analogWrite(M4_PWM, 0);
  
  /*
  Set pin 13 to output. This pin is attached to a built in LED on teh arduino.
  This LED will turn on to indicate that the program is now running
  */
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  //Serial.println("Ready!");
}

void loop()
{
    char command = 0; //char to hold command byte
    
    //if a byte is waiting in the serial buffer
    if(Serial.available() > 0)
    {
        wdt_reset(); //reset the watchdog timer (prevents shutdown!)
        command = Serial.read(); //read the byte and store it.
    }
        
    char data[8]; //data packet
    int spd;
    int rate;
    
    /*
    Determines the appropriate function to use based on packet data.
    Typical packet is as follows:
    [command][param]...[param][terminator]
    no spaces, no capitals.
    ex:
    To drive forward at 120 speed
    "df120\r"
    
    all packets should be strings.
    */
    switch(command)
    {
        case DRIVE_CODE: //drive request made
        {
            /*
            Read an 8 byte packet. 8 bytes not really needed, just gives extra padding
            to ensure terminator '\r' is received. If terminator is received then
            only bytes up to the terminator are read and the terminator is thrown away
            */
            Serial.readBytesUntil(TERMINATOR, data, 8); 
            spd = atoi(&data[1]); //convert lower bytes to int and store in spd
            drive(spd, data[0]); //transfer to drive function
            break;
        }
        case HALT_CODE: //halt request made
            halt();
            break;
        case TURN_CODE: //turn request made
        {
            Serial.readBytesUntil(TERMINATOR, data, 8);
            rate = atoi(&data[1]);
            turn(rate, data[0]);
            break;
        }
        case PING_CODE: //ping request made
            ping();
            break;
        case ENC_CODE: //count request made
            encoder_request();
            break;
        case HTBT_CODE: //heartbeat received
            Serial.println("I am still alive");
            break;
        case 0: //special cases. if nothing in the buffer 0 is constantly read.
        case TERMINATOR: //some commands do not handle terminator '\r' leaving it in buffer
            //in either of these events we do not want to throw an error, merely toss out the command.
            break;
        default: //an invalid command received or problem in transmission.
            Serial.write(ERR_CODE); //reply with error event character
            break;
    }
    
    Serial.flush(); //clear the buffer
}

/*
Initiates forward or backward movement of the rover.
spd = speed between 0 and 255
dir = direction f = forward, b = backward
*/
void drive(int spd, int dir)
{
    Serial.println("drive ack"); //acknowledge the command
    if(dir == 'f')
    {
          analogWrite(M1_PWM, spd);
          digitalWrite(M1_DIR, 1);
          analogWrite(M2_PWM, spd);
          digitalWrite(M2_DIR, 0);
          analogWrite(M3_PWM, spd);
          digitalWrite(M3_DIR, 1);
          analogWrite(M4_PWM, spd);
          digitalWrite(M4_DIR, 0);
    }
    else if(dir == 'b')
    {
          analogWrite(M1_PWM, spd);
          digitalWrite(M1_DIR, 0);
          analogWrite(M2_PWM, spd);
          digitalWrite(M2_DIR, 1);
          analogWrite(M3_PWM, spd);
          digitalWrite(M3_DIR, 0);
          analogWrite(M4_PWM, spd);
          digitalWrite(M4_DIR, 1);
    }
    else
    {
          Serial.println(ERR_CODE);
          Serial.println(spd);
          Serial.println(dir);
          analogWrite(M1_PWM, 0);
          analogWrite(M2_PWM, 0);
          analogWrite(M3_PWM, 0);
          analogWrite(M4_PWM, 0);
    }
}

/*
Halt function to stop the rover.
*/
void halt()
{
    Serial.println("halt ack");
    analogWrite(M1_PWM, 0);
    analogWrite(M2_PWM, 0);
    analogWrite(M3_PWM, 0);
    analogWrite(M4_PWM, 0);
}

/*
Uses the ultrasonic sensor to compute the distance
to the nearest object to the rover.
*/
void ping()
{
    Serial.println("ping ack");
    digitalWrite(SONAR_TRIG, LOW); //drive trigger low to settle the pin
    delayMicroseconds(2); //wait for it to settle.
    digitalWrite(SONAR_TRIG, HIGH); //start a pulse
    delayMicroseconds(5); //wait
    digitalWrite(SONAR_TRIG, LOW); //end pulse.
    
    long duration;
    int cm;
    
    duration = pulseIn(SONAR_ECHO, HIGH); //listen for echo and record time in microseconds
    cm = duration/29/2; //convert time to distance in centimeters.
    Serial.write(cm); //send the distance.
    
}

/*
Gives the current encoder count when requested
*/
void encoder_request()
{
    Serial.println("encoder ack");
    Serial.write(count);
}

/*
Functionally the same as drive, but motors turn in a 
different configuration to allow turning.
rate = turn rate (speed) between 0 and 255
dir = direction of rotation r = right, l = left
*/
void turn(int rate, int dir)
{
    Serial.println("turn ack");
    if(dir == 'r')
    {
          analogWrite(M1_PWM, rate);
          digitalWrite(M1_DIR, 1);
          analogWrite(M2_PWM, rate);
          digitalWrite(M2_DIR, 0);
          analogWrite(M3_PWM, rate);
          digitalWrite(M3_DIR, 0);
          analogWrite(M4_PWM, rate);
          digitalWrite(M4_DIR, 1);
    }
    else if(dir == 'l')
    {
          analogWrite(M1_PWM, rate);
          digitalWrite(M1_DIR, 0);
          analogWrite(M2_PWM, rate);
          digitalWrite(M2_DIR, 1);
          analogWrite(M3_PWM, rate);
          digitalWrite(M3_DIR, 1);
          analogWrite(M4_PWM, rate);
          digitalWrite(M4_DIR, 0);
    }
    else
    {
          Serial.println(ERR_CODE);
          Serial.println(rate);
          Serial.println(dir);
          analogWrite(M1_PWM, 0);
          analogWrite(M2_PWM, 0);
          analogWrite(M3_PWM, 0);
          analogWrite(M4_PWM, 0);
    }
}

/*
Encoder ISR to genertate a count
*/
void ecount()
{
   if(digitalRead(ENCODER_A) && digitalRead(ENCODER_B))
       count--;
   else
       count++; 
}
