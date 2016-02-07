#include <PID_v1.h>
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
#define    M1_PWM                 12 //changed from 46 - XXX
#define    M2_PWM                 9
#define    M3_PWM                 11 //changed from 44 - XXX
#define    M4_PWM                 10 //changed from 3 - XXX
#define    M1_DIR                   7
#define    M2_DIR                   2
#define    M3_DIR                   8
#define    M4_DIR                   3 //changed from 10 - XXX

/*
  Pins for the HC-SR04 ultrasonic sensor
  Trigger pin to send out a ultrasonic pulse.
  Echo pin to listen for the pulse echo.
*/
#define    SONAR_TRIG              6
#define    SONAR_ECHO             5

/*
  Encoder input pins used to trigger encoder count interrupts.
*/
#define    ENCODER_1_A              22
#define    ENCODER_1_B              23
#define    ENCODER_2_A              24
#define    ENCODER_2_B              25
#define    ENCODER_3_A              26
#define    ENCODER_3_B              27
#define    ENCODER_4_A              28
#define    ENCODER_4_B              29
#define    ENCODER_INT_1          21
#define    ENCODER_INT_2          20
#define    ENCODER_INT_3          19
#define    ENCODER_INT_4          18

/*
  Command characters and event characters:
  d = request to use drive function.This pin is attached to a built in LED on teh arduino.
  p = request to use ping function
  h = request to use halt function
  t = request to use turn function
  e = request encoder count
  x = error event occurred
  b = heartbeat signal character
  \r = terminating character for packet data
*/
const char     DRIVE_CODE    =    'd';
const char     PING_CODE      =    'p';
const char     HALT_CODE      =    'h';
const char     TURN_CODE     =    't';
const char     ENC_CODE      =    'e';
const char     ERR_CODE      =    'x';
const char     HTBT_CODE     =    'b';
const char     TERMINATOR    =    '\r';

/*
  Encoder count variable. This count can go negative.
*/
volatile long  count1 = 0;
volatile long  count2 = 0;
volatile long  count3 = 0;
volatile long  count4 = 0;

volatile unsigned char new1;
volatile unsigned char old1;
volatile unsigned char new2;
volatile unsigned char old2;
volatile unsigned char new3;
volatile unsigned char old3;
volatile unsigned char new4;
volatile unsigned char old4;

double Input1, Output1, Setpoint1;
double Input2, Output2, Setpoint2;
double Input3, Output3, Setpoint3;
double Input4, Output4, Setpoint4;

PID m1PID(&Input1, &Output1, &Setpoint1, 0, 0, 0, DIRECT);
PID m2PID(&Input2, &Output2, &Setpoint2, 0, 0, 0, DIRECT);
PID m3PID(&Input3, &Output3, &Setpoint3, 0, 0, 0, DIRECT);
PID m4PID(&Input4, &Output4, &Setpoint4, 0, 0, 0, DIRECT);

// Values from Github Project - should work
// kp=0.2, ki=1.5, kd=0;
// kp has a large effect, ki = 1.7 is the best we have found so far. 
// c = conservative, A = agressive
double kpC = 0.005;
double kiC = 1.7;
double kdC = 0.01;

double kpA = 0.005;
double kiA = 1.7;
double kdA = 0.01;

// Quadrature Encoder Matrix
int QEM [16] = {0, -1, 1, 2, 1, 0, 2, -1, -1, 2, 0, 1, 2, 1, -1, 0};

int j = 0;

double tol = 1.0;

double encodRes = 1000.0 / 3.0;

char currentDir = '\0';

boolean haltFlag = true;

long int timeOld = 0;

void setup()
{
  interrupts();
  Serial3.begin(19200);
  TCCR2B = TCCR2B & 0b11111000 | 0x04;
  TCCR1B = TCCR1B & 0b11111000 | 0x03;  //start UART0 with a baud of 19200 Bps
  //wdt_enable (WDTO_8S); //enable the watchdog timer at 8S countdown

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

  pinMode(ENCODER_1_A, INPUT);
  pinMode(ENCODER_1_B, INPUT);
  pinMode(ENCODER_2_A, INPUT);
  pinMode(ENCODER_2_B, INPUT);
  pinMode(ENCODER_3_A, INPUT);
  pinMode(ENCODER_3_B, INPUT);
  pinMode(ENCODER_4_A, INPUT);
  pinMode(ENCODER_4_B, INPUT);
  pinMode(ENCODER_INT_1, INPUT);
  pinMode(ENCODER_INT_2, INPUT);
  pinMode(ENCODER_INT_3, INPUT);
  pinMode(ENCODER_INT_4, INPUT);

  /*
    Set the drive mode for the ultrasonic sensor.
    Trigger is used to create a pulse, so must be an output.
    Echo is used to sense a response so it must be input.
  */
  pinMode(SONAR_TRIG, OUTPUT);
  pinMode(SONAR_ECHO, INPUT);

  /*
    XXX
    Sets the PWM timers to 488hz on each side.
  */
  TCCR2B = TCCR2B & 0b11111000 | 0x04;
  TCCR1B = TCCR1B & 0b11111000 | 0x03;

  attachInterrupt(2, ecount1, CHANGE);
  attachInterrupt(3, ecount2, CHANGE);
  attachInterrupt(4, ecount3, CHANGE);
  attachInterrupt(5, ecount4, CHANGE);

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


  m1PID.SetTunings(kpC, kiC, kdC);
  m1PID.SetSampleTime(50);
  m1PID.SetOutputLimits(0, 255);
  m1PID.SetMode(AUTOMATIC);
  m1PID.SetControllerDirection(DIRECT);

  m2PID.SetTunings(kpC, kiC, kdC);
  m2PID.SetSampleTime(50);
  m2PID.SetOutputLimits(0, 255);
  m2PID.SetMode(AUTOMATIC);
  m2PID.SetControllerDirection(DIRECT);

  m3PID.SetTunings(kpC, kiC, kdC);
  m3PID.SetSampleTime(50);
  m3PID.SetOutputLimits(0, 255);
  m3PID.SetMode(AUTOMATIC);
  m3PID.SetControllerDirection(DIRECT);

  m4PID.SetTunings(kpC, kiC, kdC);
  m4PID.SetSampleTime(50);
  m4PID.SetOutputLimits(0, 255);
  m4PID.SetMode(AUTOMATIC);
  m4PID.SetControllerDirection(DIRECT);

  Setpoint1 = 0;
  Setpoint2 = 0;
  Setpoint3 = 0;
  Setpoint4 = 0;

  /*
    Wait for Serial3 to initialize before proceeding.
  */
  while (!Serial3);
  Serial3.println("Ready!");
}

void loop()
{
  char command = 0; //char to hold command byte

  //if a byte is waiting in the Serial3 buffer
  if (Serial3.available() > 0)
  {
    //wdt_reset(); //reset the watchdog timer (prevents shutdown!)
    command = Serial3.read(); //read the byte and store it.
  }

  char data[8]; //data packet
  int spd;
  int rate;


  //    if(dist() < (10.0 + tol) || dist() < (10.0 - tol))
  //     {
  //        analogWrite(M1_PWM, 0);
  //        analogWrite(M2_PWM, 0);
  //        analogWrite(M3_PWM, 0);
  //        analogWrite(M4_PWM, 0);
  //        haltFlag = true;
  //     }

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
  switch (command)
  {
    case DRIVE_CODE: //drive request made
      /*
        Read an 8 normalizeMotors();byte packet. 8 bytes not really needed, just gives extra padding
        to ensure terminator '\r' is received. If terminator is received then
        only bytes up to the terminator are read and the terminator is thrown away
      */
      Serial3.readBytesUntil(TERMINATOR, data, 8);
      spd = atoi(&data[1]); //convert lower bytes to int and store in spd
      drive(spd, data[0]); //transfer to drive function   if(m1 == slowest + tolerance)
      break;
    case HALT_CODE: //halt request made
      halt();
      break;
    case TURN_CODE: //turn request made
      {
        Serial3.readBytesUntil(TERMINATOR, data, 8);
        rate = atoi(&data[1]);
        turn(rate, data[0]);
        break;
      }
    case PING_CODE: //ping request made
      ping();
      break;
    //        case ENC_CODE: //count request made
    //            encoder_request();
    //            break;
    //case HTBT_CODE: //heartbeat received
    //  Serial3.println("I am still alive");
    // break;
    case 0: //special cases. if nothing in the buffer 0 is constantly read.
    case TERMINATOR: //some commands do not handle terminator '\r' leaving it in buffer
      //in either of these events we do not want to throw an error, merely toss out the command.
      break;
    default: //an invalid command received or problem in transmission.
      Serial3.write(ERR_CODE); //reply with error event character
      break;
  }

  if(!haltFlag)
  {
    //if(millis() - timeOld >= 100)
    //{
      normalizeMotors();
      //timeOld = millis();
    //}
  }

  /*if (!haltFlag)
  {
    m1PID.Compute();
    m2PID.Compute();
    m3PID.Compute();5000
    m4PID.Compute();
    switch (currentDir)
    {
      case 'f':
        drive(Setpoint1, 'f');
        break;
      case 'b':
        drive(Setpoint1, 'b');
        break;
      case 'l':
        turn(Setpoint1, 'l');
        break;
      case 'r':
        drive(Setpoint1, 'r');
        break;
      default:
        break;
    }
  }*/



  Serial3.flush(); //clear the buffer
}


/*
  Initiates forward or backward movement of the rover.
  spd = speed between 0 and 255
  dir = direction f = forward, b = backward
*/
void drive(int spd, char dir)
{
  Setpoint1 = (double)spd;
  Setpoint2 = (double)spd;
  Setpoint3 = (double)spd;
  Setpoint4 = (double)spd;
  //currentDir = dir;

  Serial3.println(Setpoint1);
  Serial3.println(Input1);
  Serial3.println(Output1);

  Serial3.println("drive ack"); //acknowledge the command
  if (dir == 'f')
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
  else if (dir == 'b')
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
    Setpoint1 = 0;
    Setpoint2 = 0;
    Setpoint3 = 0;
    Setpoint4 = 0;
    Serial3.println(ERR_CODE);
    Serial3.println(spd);
    Serial3.println(dir);
    analogWrite(M1_PWM, 0);
    analogWrite(M2_PWM, 0);
    analogWrite(M3_PWM, 0);
    analogWrite(M4_PWM, 0);
  }
  haltFlag = false;
  //delay(250);
}

void normalizeMotors()
{
  Input1 = abs(speed1());
  Input2 = abs(speed2());
  Input3 = abs(speed3());
  Input4 = abs(speed4());

/*  if(abs(Setpoint1 - Input1) > 50)
  {
    m1PID.SetTunings(kpA, kiA, kdA);
  }
  else
  {
    m1PID.SetTunings(kpC, kiC, kdC);
  }

  if(abs(Setpoint2 - Input2) > 50)
  {
    m2PID.SetTunings(kpA, kiA, kdA);
  }
  else
  {
    m2PID.SetTunings(kpC, kiC, kdC);
  }

  if(abs(Setpoint3 - Input3) > 50)
  {
    m3PID.SetTunings(kpA, kiA, kdA);
  }
  else
  {
    m3PID.SetTunings(kpC, kiC, kdC);
  }

  if(abs(Setpoint4 - Input4) > 50)
  {
    m4PID.SetTunings(kpA, kiA, kdA);
  }
  else
  {
    m4PID.SetTunings(kpC, kiC, kdC);
  }
  */
  m4PID.Compute();
  m3PID.Compute();
  m2PID.Compute();
  m1PID.Compute();
  analogWrite(M1_PWM, Output1);
  analogWrite(M2_PWM, Output2);
  analogWrite(M3_PWM, Output3);
  analogWrite(M4_PWM, Output4);
}

/*
  Halt function to stop the rover.
*/
void halt()
{
  Setpoint1 = 0;
  Setpoint2 = 0;
  Setpoint3 = 0;
  Setpoint4 = 0;
  Serial3.println("halt ack");
  analogWrite(M1_PWM, 0);
  analogWrite(M2_PWM, 0);
  analogWrite(M3_PWM, 0);
  analogWrite(M4_PWM, 0);
  haltFlag = true;
}

/*
  Uses the ultrasonic sensor to compute the distance
  to the nearest object to the rover.
*/
void ping()
{
  Serial3.println("ping ack");
  digitalWrite(SONAR_TRIG, LOW); //drive trigger low to settle the pin
  delayMicroseconds(2); //wait for it to settle.
  digitalWrite(SONAR_TRIG, HIGH); //start a pulse
  delayMicroseconds(5); //wait
  digitalWrite(SONAR_TRIG, LOW); //end pulse.

  long duration;
  float cm;

  duration = pulseIn(SONAR_ECHO, HIGH); //listen for echo and record time in microseconds
  cm = duration / 29.0 / 2.0; //convert time to distance in centimeters.

  Serial3.println(cm); //send the distance.

}

/*
  Functionally the same a
  m1PID.Compute();s drive, but motors turn in a
  different configuration to allow turning.
  rate = turn rate (speed) between 0 and 255
  dir = direction of rotation r = right, l = left
*/
void turn(int rate, char dir)
{
  Setpoint1 = (double)rate;
  Setpoint2 = (double)rate;
  Setpoint3 = (double)rate;
  Setpoint4 = (double)rate;

  Serial3.println("turn ack");
  if (dir == 'r')
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
  else if (dir == 'l')
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
    Setpoint1 = 0;
    Setpoint2 = 0;
    Setpoint3 = 0;
    Setpoint4 = 0;
    Serial3.println(ERR_CODE);
    Serial3.println(rate);
    Serial3.println(dir);
    analogWrite(M1_PWM, 0);
    analogWrite(M2_PWM, 0);
    analogWrite(M3_PWM, 0);
    analogWrite(M4_PWM, 0);
  }
  haltFlag = false;
  //delay(10);
}

/*
  XXX
  Changed all speed functions to calculate speed in RPMs to make it easier for
  future calculations.
*/
double speed1()
{
  long countA = count1;
  delay(15);
  long countB = count1;

  long numCounts = countB - countA;

  double RPM = ((numCounts / encodRes) * 60) / (0.015);

  return RPM;
}

double speed2()
{
  long countA = count2;
  delay(15);
  long countB = count2;

  long numCounts = countB - countA;

  double RPM = ((numCounts / encodRes) * 60) / (0.015);

  return RPM;
}

double speed3()
{
  long countA = count3;
  delay(15);
  long countB = count3;

  long numCounts = countB - countA;

  double RPM = ((numCounts / encodRes) * 60) / (0.015);

  return RPM;
}

double speed4()
{
  long countA = count4;
  delay(15);
  long countB = count4;

  long numCounts = countB - countA;

  double RPM = ((numCounts / encodRes) * 60) / (0.015);

  return RPM;
}

double dist()
{
  digitalWrite(SONAR_TRIG, LOW); //drive trigger low to settle the pin
  delayMicroseconds(2); //wait for it to settle.
  digitalWrite(SONAR_TRIG, HIGH); //start a pulse
  delayMicroseconds(5); //wait
  digitalWrite(SONAR_TRIG, LOW); //end pulse.

  long duration;
  float cm;

  duration = pulseIn(SONAR_ECHO, HIGH); //listen for echo and record time in microseconds
  cm = duration / 29.0 / 2.0; //convert time to distance in centimeters.

  return cm;
}

void ecount1()
{
  old1 = new1;
  new1 = digitalRead(ENCODER_1_A) * 2 + digitalRead(ENCODER_1_B);
  count1 += QEM[old1 * 4 + new1];
}

void ecount2()
{
  old2 = new2;
  new2 = digitalRead(ENCODER_2_A) * 2 + digitalRead(ENCODER_2_B);
  count2 += QEM[old2 * 4 + new2];
}

void ecount3()
{
  old3 = new3;
  new3 = digitalRead(ENCODER_3_A) * 2 + digitalRead(ENCODER_3_B);
  count3 += QEM[old3 * 4 + new3];
}

void ecount4()
{
  old4 = new4;
  new4 = digitalRead(ENCODER_4_A) * 2 + digitalRead(ENCODER_4_B);
  count4 += QEM[old4 * 4 + new4];
}
