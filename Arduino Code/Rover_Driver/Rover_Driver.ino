#include <PID_v1.h>
#include <avr/wdt.h> //library to use watchdog timers for AVR chips
#include "rover_system.h"
#include "rover_params.h"


/*
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
 * Top level global variables.
 * 
 * These are the non-constant global variables only used in the top level. They are declared here to avoid unnecessary user of extern.
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
  */
  
/*
 * Flag to determine if the Rover has stopped.
 * true = halted
 */
bool haltFlag = true;
 
/*
 * Controls the distance tolerance on the HC-SR04
 */
double tol = 1.0;

/*
 * Variables used in the encoder count ISRs.
 * old# = the previous value read from the QEM
 * new# = the current reading from the QEM
 */
volatile unsigned char new1;
volatile unsigned char old1;
volatile unsigned char new2;
volatile unsigned char old2;
volatile unsigned char new3;
volatile unsigned char old3;
volatile unsigned char new4;
volatile unsigned char old4;

/*
 * Encoder count variable. This count can go negative.
 */
volatile long  count1 = 0;
volatile long  count2 = 0;
volatile long  count3 = 0;
volatile long  count4 = 0;


/*
 * Holds the current RPM reading from each motor
 */
double RPMs[4] = {0, 0, 0, 0};

/*
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
 * PID functions and variables
 * 
 * These need to be included at the top level whereh the PID_v1.h file is visible.
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
  */

  
/*
 * PID varaibles. Used by refernce in the PID algorithm to
 * correct the inherent veer in the rover.
 */
double Input1, Output1, Setpoint1;
double Input2, Output2, Setpoint2;
double Input3, Output3, Setpoint3;
double Input4, Output4, Setpoint4;

/*
 * Values from another Github project using the Rover 5
 * 
 * kp = 0.2
 * ki = 1.5
 * kd = 0
 * 
 * kp - scales current error reading
 * ki - scales sum of previous error readings
 * kd - scales potential error readings (future)
 * 
 * A - agressive
 * C - conservative
 * 
 * best results thus far with:
 * kp = 0
 * ki = 1.7
 * kd = 0
 */
double kpC = 0.005;
double kiC = 1.7;
double kdC = 0.01;

double kpA = 0.005;
double kiA = 1.7;
double kdA = 0.01;

/*
 * PID objects used to independantly comput the PID algorithm
 * on each of the motors.
 * 
 * Syntax: PID pidObj(&in, &out, &set, kp, ki, kd, MODE)
 * Mode: DIRECT or REVERSE determines whetehr the PID
 *       algorithm increases or decreases the output
 *       if it is above the setpoint.
 */
PID m1PID(&Input1, &Output1, &Setpoint1, 0, 0, 0, DIRECT);
PID m2PID(&Input2, &Output2, &Setpoint2, 0, 0, 0, DIRECT);
PID m3PID(&Input3, &Output3, &Setpoint3, 0, 0, 0, DIRECT);
PID m4PID(&Input4, &Output4, &Setpoint4, 0, 0, 0, DIRECT);

/*
 * Compute the speed in RPMs for each motor.
 */
void speeds()
{
  double countAs[4] = {(double)count1, (double)count2, (double)count3 ,(double)count4};
  delay(50);
  double countBs[4] = {(double)count1, (double)count2, (double)count3, (double)count4};

  double diffs[4] = {countBs[0]-countAs[0], countBs[1]-countAs[1], countBs[2]-countAs[2], countBs[3]-countAs[3]};
  
  RPMs[0] = ((diffs[0]/encodRes) * 60.0) / (0.05);
  RPMs[1] = ((diffs[1]/encodRes) * 60.0) / (0.05);
  RPMs[2] = ((diffs[2]/encodRes) * 60.0) / (0.05);
  RPMs[3] = ((diffs[3]/encodRes) * 60.0) / (0.05);
}

/*
 * Implements PID to control motor speed at a constant 
 * value and prevent veer.
 */
 
void normalizeMotors()
{
  speeds();
  Input1 = abs(RPMs[0]);
  Input2 = abs(RPMs[1]);
  Input3 = abs(RPMs[2]);
  Input4 = abs(RPMs[3]);

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
 * Initializes the PID parameters.
 */
void pidInit()
{
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
}


/*
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
 * Main program
 * 
 * This is where the main control loop is implemented
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
 */
 
/*
 * Runs wen the Arduino powers on or restars (ie. after reset) and then never again.
 * Used to configure hardware and software parameters for the Rover.
 */
void setup()
{
  interrupts(); //enable interrupts
  Serial3.begin(19200); //start UART3 at 19200 baud
  
  //wdt_enable (WDTO_8S); //enable the watchdog timer at 8 second countdown

  /*
   * Set the drive mode of all of the motor pins to output.
   * Motors do not have any feedback so no input pin is needed
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
   * Set the ecoder pins as inputs
   */
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
   * Set the drive mode for the ultrasonic sensor.
   * Trigger is used to create a pulse, so must be an output.
   * Echo is used to sense a response so it must be input.
   */
  pinMode(SONAR_TRIG, OUTPUT);
  pinMode(SONAR_ECHO, INPUT);

  /*
   * Sets the PWM timers to 488hz on each track.
   */
  TCCR2B = TCCR2B & 0b11111000 | 0x04;
  TCCR1B = TCCR1B & 0b11111000 | 0x03;

  /*
   * Set the interrupt vector to use all interrupts as a change from read
   * mode and attach the ISRs to each pin respectively.
   * 
   * NOTE:
   * The first input (2, 3, 4, 5) is not the pin number, but the interrupt number.
   * Each GPIO interrupt in the AVR interrupt vector is assigned a number and this
   * is used to identify it rather than the pin number!
   */
  attachInterrupt(2, ecount1, CHANGE);
  attachInterrupt(3, ecount2, CHANGE);
  attachInterrupt(4, ecount3, CHANGE);
  attachInterrupt(5, ecount4, CHANGE);

  /*
   * Initialize all of the motors to 0 (ie. off)
   */
  analogWrite(M1_PWM, 0);
  analogWrite(M2_PWM, 0);
  analogWrite(M3_PWM, 0);
  analogWrite(M4_PWM, 0);

  /*
   * Set pin 13 to output. This pin is attached to a built in LED on teh arduino.
   * This LED will turn on to indicate that the program is now running
   */
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);

  /*
   * Set the PID parameters.
   */
  pidInit();
  
  /*
    Wait for Serial3 to initialize before proceeding.
  */
  while (!Serial3);
  Serial3.println("Ready!");
}

/*
 * Main control loop. Runs indefinitely as long as Arduino is powered.
 */
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
   * Determines the appropriate function to use based on packet data.
   * Typical packet is as follows:
   * [command][param]...[param][terminator]
   * no spaces, no capitals.
   * ex:
   * To drive forward at 120 speed
   * "df120\r"
   *
   * all packets should be strings.
   */
  switch (command)
  {
    case DRIVE_CODE: //drive request made
       /*
        * Read an 8 normalizeMotors();byte packet. 8 bytes not really needed, just gives extra padding
        * to ensure terminator '\r' is received. If terminator is received then
        * only bytes up to the terminator are read and the terminator is thrown away
        */
        Serial3.readBytesUntil(TERMINATOR, data, 8);
        spd = atoi(&data[1]); //convert lower bytes to int and store in spd
        drive(spd, data[0]); //transfer to drive function   if(m1 == slowest + tolerance)
            
        Setpoint1 = (double)spd;
        Setpoint2 = (double)spd;
        Setpoint3 = (double)spd;
        Setpoint4 = (double)spd;

        haltFlag = false;
        break;
    case HALT_CODE: //halt request made
        halt();
        
        Setpoint1 = 0;
        Setpoint2 = 0;
        Setpoint3 = 0;
        Setpoint4 = 0;

        haltFlag = true;
        break;
    case TURN_CODE: //turn request made
        Serial3.readBytesUntil(TERMINATOR, data, 8);
        rate = atoi(&data[1]);
        turn(rate, data[0]);
            
        Setpoint1 = (double)rate;
        Setpoint2 = (double)rate;
        Setpoint3 = (double)rate;
        Setpoint4 = (double)rate;
        
        haltFlag = false;
        break;
    case PING_CODE: //ping request made
        ping();
        break;
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
      normalizeMotors(); //use PID to correct veer
  }

  Serial3.flush(); //clear the buffer
}

/*
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
 * Encoder ISRs
 * 
 * Using the Arduino Mega's 4 interrupt pins, these functions are called on every rising and falling edge of the Rover 5
 * motor driver board's encoder mixer output. This mixer is just an XOR gate that takes both encoder values as input.
 * 
 * ____/""""\____/""""\____/""""\____   A
 * ______/""""\____/""""\____/""""\__   B
 * 
 * 
 * The encoder readings are first converted from binary to decimal with A being the most significatn bit
 * ie.
 * AB | Dec
 * 00 |  0
 * 01 |  1
 * 10 |  2
 * 11 |  3
 * 
 * Depnding on the direction of rotation we get the following patterns:
 * 00 | 0
 * 01 | 1
 * 11 | 3
 * 10 | 2
 * 
 * or
 * 
 * 00 | 0
 * 10 | 2
 * 11 | 3
 * 01 | 1
 * 
 * Using the XOR encoder mixing logic we get a single square wave with twice the frequency of the encoder interrupts.
 * Though the QEM matrix in code is a flat 1x16 array, it can be thought of as a 4x4 array.
 * 
 *    0  1  2  3
 * 0 |0 -1 +1  X| 
 * 1 |+1 0  X -1| 
 * 2 |-1 X  0 +1| 
 * 3 |X +1 -1  0| 
 * 
 * So an encoder input sequence of 0, 1, 2, 3 will give an output of +1 from the QEM
 * and an encoder input sequence of 0, 2, 3, 1 will give an output of -1 from the QEM 
 * 
 * X is a state that the QEM should never actually index to since the interrupts are generated by an XOR
 * and each X state is the result of the ecoder reading 11 at the time of the interrupt.
 * =======================================================================================================================================================================
 * =======================================================================================================================================================================
 */


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
