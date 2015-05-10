#include "Adafruit_WS2801.h"
#include "SPI.h"

int dataPin = 8;
int clockPin = 9;

Adafruit_WS2801 strip = Adafruit_WS2801(25, dataPin, clockPin);
void setup() {
  // put your setup code here, to run once:
  strip.begin();
  strip.show();
  Serial.begin(9600);
}

void colorWipe(uint32_t c, uint8_t wait) {
 int i;
 for (i=0; i < strip.numPixels(); i++){
   strip.setPixelColor(i, c);
   strip.show();
   delay(wait);
 } 
}


uint32_t Color(byte r, byte g, byte b) {
  uint32_t c;
  c = r;
  c <<= 8;
  c |= g;
  c <<= 8;
  c |= b;
  return c;
}




unsigned long readULongFromBytes() {
  union u_tag {
    byte b[4];
    unsigned long ulval;
  } u;
  u.b[0] = Serial.read();
  u.b[1] = Serial.read();
  u.b[2] = Serial.read();
  u.b[3] = Serial.read();
  Serial.write(u.ulval);
  return u.ulval;
}

unsigned long red[25];
unsigned long green[25];
unsigned long blue[25];
bool r = false;
bool g = false;
bool b = false;
unsigned long counter = 0;


void set_value(unsigned long value){
  if (value==400){
    r=false;
    g=false;
    b=false;
    strip.setPixelColor(counter, Color(red[counter],green[counter],blue[counter]));
    strip.show();
    counter++;
    if (counter==25){
      counter=0;
    }
  }
  else if (!r){
    red[counter] = value;
    r=true;
  }
  else if (!g){
    green[counter] = value;
    g=true;
  }
  else if (!b){
    blue[counter] = value;
  }
  
}

void loop() {
 if(Serial.available() >= 4) {
    //red[counter] = readULongFromBytes();
    //green[counter] = readULongFromBytes();
    //blue[counter] = readULongFromBytes();
    //strip.setPixelColor(counter, Color(red[counter],green[counter],blue[counter]));
    //strip.show();
 
    set_value(readULongFromBytes());
   
    
    
		
	
                
   
 
 }
  

  // put your main code here, to run repeatedly:
 // colorWipe(Color(255,0,0), 50);
 // colorWipe(Color(0,255,0), 50);
 // colorWipe(Color(0,0,255), 50);

}



