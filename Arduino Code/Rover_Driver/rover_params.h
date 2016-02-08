/*
 * This file contains all of the #defines and global variables needed for
 * the rover to function.
 */


/*
 * Motor pins in order:
 * Motor 1 PWM
 * Motor 2 PWM
 * Motor 3 PWM
 * Motor 4 PWM
 * Motor 1 direction
 * Motor 2 direction
 * Motor 3 direction
 * Motro 4 direction
 *
 * PWM = pulse width modulation, used to control speed
 * direction = CW or CCW rotation of the motors
 *
 * These pin numbers are chosen purposefully to make sure
 * each track's motors have PWMs controlled by the same
 * hardware timer allowing them to be controlled at the
 * same frequency regardless of duty cycle.
 */
#define    M1_PWM       12 
#define    M2_PWM       9
#define    M3_PWM       11 
#define    M4_PWM       10 
#define    M1_DIR       7
#define    M2_DIR       2
#define    M3_DIR       8
#define    M4_DIR       3

/*
 * Pins for the HC-SR04 ultrasonic sensor
 * Trigger pin to send out a ultrasonic pulse.
 * Echo pin to listen for the pulse echo.
 */
#define    SONAR_TRIG       6
#define    SONAR_ECHO       5

/*
 * Encoder input pins used to trigger encoder count interrupts.
 */
#define    ENCODER_1_A      22
#define    ENCODER_1_B      23
#define    ENCODER_2_A      24
#define    ENCODER_2_B      25
#define    ENCODER_3_A      26
#define    ENCODER_3_B      27
#define    ENCODER_4_A      28
#define    ENCODER_4_B      29
#define    ENCODER_INT_1    21
#define    ENCODER_INT_2    20
#define    ENCODER_INT_3    19
#define    ENCODER_INT_4    18

/*
 * Command characters and event characters:
 * d = request to use drive function.This pin is attached to a built in LED on teh arduino.
 * p = request to use ping function
 * h = request to use halt function
 * t = request to use turn function
 * x = error event occurred
 * b = heartbeat signal character
 * \r = terminating character for packet data
 */
const char     DRIVE_CODE       =    'd';
const char     PING_CODE        =    'p';
const char     HALT_CODE        =    'h';
const char     TURN_CODE        =    't';
const char     ERR_CODE         =    'x';
const char     HTBT_CODE        =    'b';
const char     TERMINATOR       =    '\r';

/*
 * Quadrature encoder matrix. Determines whether to count up or down.
 */
const int QEM [16] = {0, -1, 1, 2, 1, 0, 2, -1, -1, 2, 0, 1, 2, 1, -1, 0};

/*
 * The resolution of the hall effect encoders.
 */
const double encodRes = 1000.0 / 3.0;
