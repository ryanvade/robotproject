/*
 * This file will contain all of the neccessary function declarations
 * for the Rover's control systems and sensor functions.
 */
 
#ifndef ROVER_SYSTEM_H
#define ROVER_SYSTEM_H

/*
 * Initiates forward or backward movement of the rover.
 * spd = speed between 0 and 255
 * dir = direction f = forward, b = backward
 */
void drive(int spd, char dir);

/*
 * Functionally the same as drive, but motors rotate
 *  in a different configuration to allow turning.
 * rate = turn rate (speed) between 0 and 255
 * dir = direction of rotation r = right, l = left
 */
void turn(int rate, char dir);

/*
 * Halt function to stop the rover.
 */
void halt();

/*
 * Uses the ultrasonic sensor to compute the distance
 * to the nearest object to the rover.
 */
void ping();

/*
 * Functionally equivalent to ping() but does not 
 * return a serial acknowledgement
 */
double dist();

/*
 * Initializes the PID parameters.
 */
void pidInit();

#endif
