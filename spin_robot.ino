

unsigned int motor1PWM = 5;
unsigned int motor3PWM = 6;
unsigned int motor2PWM = 9;
unsigned int motor4PWM = 3;

unsigned int dir1 = 4;
unsigned int dir2 = 2;
unsigned int dir3 = 7;
unsigned int dir4 = 10;

unsigned int GND1 = 12;
unsigned int GND2 = 11;

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
  
  pinMode(GND1, OUTPUT);
  pinMode(GND2, OUTPUT);
 
  digitalWrite(GND1, LOW);
  digitalWrite(GND2, LOW); 
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
  
  delay(5000);
  
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);
  digitalWrite(dir3, HIGH);
  digitalWrite(dir4, LOW);
  
  delay(5000);
}
