#include <Servo.h> 

int SERVOPin = 9;
int val = 0;
Servo myservo; 
int pos = 0;
int angle = 60;

void setup() {
  Serial.begin(9600);
  myservo.attach(SERVOPin);
  delay(100);
  myservo.write(angle);
}

void loop() {
  if (Serial.available()>0){
  val = Serial.parseInt();
  //Serial.println(val);
}

if (val == 1){
  for(pos = angle; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(10);    // waits 15ms for the servo to reach the position 
  }
  for(pos = 0; pos < angle; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(10);     // waits 15ms for the servo to reach the position 
    //val = 0;
    if(pos < angle -1){
      val = 0;
    }
  } 
}

}
