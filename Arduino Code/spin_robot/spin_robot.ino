

unsigned int motor1PWM = 12;
unsigned int motor3PWM = 11;
unsigned int motor2PWM = 9;
unsigned int motor4PWM = 10;

unsigned int dir1 = 7;
unsigned int dir2 = 2;
unsigned int dir3 = 8;
unsigned int dir4 = 3;

//unsigned int GND1 = 12;
//unsigned int GND2 = 11;

void setup()
{
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(dir3, OUTPUT);
  pinMode(dir4, OUTPUT);
  
  pinMode(motor1PWM, OUTPUT);
  pinMode(motor2PWM, OUTPUT);
  pinMode(motor3PWM, OUTPUT);
  pinMode(motor4PWM, OUTPUT);
}

void loop()
{
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);
  digitalWrite(dir3, LOW);
  digitalWrite(dir4, HIGH);
  
  digitalWrite(motor1PWM, 35);
  digitalWrite(motor2PWM, 35);
  digitalWrite(motor3PWM, 35);
  digitalWrite(motor4PWM, 35);
  
  delay(1000);
  
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);
  digitalWrite(dir3, HIGH);
  digitalWrite(dir4, LOW);
  
  delay(1000);
}
