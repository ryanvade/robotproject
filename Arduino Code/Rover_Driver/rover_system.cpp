/*
 * This file will contain all of the neccessary function definitions
 * for the Rover's control systems and sensor functions.
 */


#include "rover_system.h"
#include "rover_params.h"
 
/*
 * Initiates forward or backward movement of the rover.
 * spd = speed between 0 and 255
 * dir = direction f = forward, b = backward
 */
 void drive(int spd, char dir)
{
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
    Serial3.println(ERR_CODE);
    Serial3.println(spd);
    Serial3.println(dir);
    halt();
  }
}

/*
 * Functionally the same as drive, but motors rotate
 *  in a different configuration to allow turning.
 * rate = turn rate (speed) between 0 and 255
 * dir = direction of rotation r = right, l = left
 */
void turn(int rate, char dir)
{
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
    Serial3.println(ERR_CODE);
    Serial3.println(rate);
    Serial3.println(dir);
    halt();
  }
}

/*
 * Halt function to stop the rover.
 */
void halt()
{
  Serial3.println("halt ack");
  analogWrite(M1_PWM, 0);
  analogWrite(M2_PWM, 0);
  analogWrite(M3_PWM, 0);
  analogWrite(M4_PWM, 0);
}

/*
 * Uses the HC-SR04 ultrasonic sensor to compute the distance
 * to the nearest object to the rover.
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
 * Functionally equivalent to ping() but does not 
 * return a serial acknowledgement
 */
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


