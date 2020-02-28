/*
  SD card read/write
 
 This example shows how to read and write data to and from an SD card file 	
 The circuit:
 * SD card attached to SPI bus as follows:
 ** MOSI - pin 11, pin 7 on Teensy with audio board
 ** MISO - pin 12
 ** CLK - pin 13, pin 14 on Teensy with audio board
 ** CS - pin 4, pin 10 on Teensy with audio board
 
 created   Nov 2010
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe
 
 This example code is in the public domain.
 	 
 */
 
#include <SD.h>
#include <SPI.h>

File myFile;
// change this to match your SD shield or module;
// Arduino Ethernet shield: pin 4
// Adafruit SD shields and modules: pin 10
// Sparkfun SD shield: pin 8
// Teensy audio board: pin 10
// Teensy 3.5 & 3.6 on-board: BUILTIN_SDCARD
// Wiz820+SD board: pin 4
// Teensy 2.0: pin 0
// Teensy++ 2.0: pin 20
const int chipSelect = BUILTIN_SDCARD;
#define file_name "img_test.txt"
#define lazer_on_message "lazer_on,"
#define lazer_off_message "lazer_off,"
#define frame_start_message "frame_start,"
#define frame_end_message "frame_end,"
#define lazer_output 2//pwmpin
#define lazer_on 255
#define lazer_off 0

String str;
String buff;

int datacount=0;//x,yを分けるカウンター
int x_val=0;//読み取ったｘとｙの値を格納する。
int y_val=0;



elapsedMicros usec = 0;

//TODO:1フレームの間は同じフレームをループさせる。

void setup()
{
  
  analogWriteResolution(12);
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
   while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  //Serial.print("Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    //Serial.println("initialization failed!");
    return;
  }
  //Serial.println("initialization done.");
    // open the file. 
 


}

void loop()
{
	// nothing happens after setup
   myFile = SD.open(file_name, FILE_WRITE);
  // re-open the file for reading:
  str="";//str初期化
  buff="";

  myFile = SD.open(file_name);
  if (myFile) {
    //Serial.println(file_name);
    //Serial.println("start_file_read");
    // read from the file until there's nothing else in it:
    int count=0;
    while (myFile.available()) {
      
        str = char(myFile.read());//1biteずつ格納される。
        count++;
        //Serial.print("count=");
        //Serial.println(count);
        
        buff += str;
        
        if(str==','){

          if(buff.equals(frame_start_message)){
            //Serial.println("FRAME_START");          
            buff="";
          }else
          if(buff.equals(lazer_off_message)){
            //Serial.println("LAZER_OFF");  
            analogWrite(lazer_output,lazer_off);        
            buff="";
          }else
          if(buff.equals(lazer_on_message)){
            //Serial.println("LAZER_ON");
            analogWrite(lazer_output,lazer_on);          
            buff="";
          }else
          if(buff.equals(frame_start_message)){
            //Serial.println("FRAME_START");
            buff="";          
          }else
          if(buff.equals(frame_end_message)){
            //Serial.println("FRAME_END");
            buff="";          
          }else{
            //Serial.print("buff=");
            //Serial.println(buff);
            buff=buff.trim();
            
            buff.remove(buff.indexOf(","), 1);
            //Serial.println(buff);
            int val = buff.toInt();
            //Serial.println(val);
            if(datacount==0){
              datacount++;
              x_val=val;
            }else{
              datacount=0;
              y_val=val;
            }
            //Serial.print("x_val:");
            //Serial.println(x_val);
            //Serial.print("y_val:");
            //Serial.println(y_val);
            analogWrite(A21, map(x_val,0,640,0,4095));
            analogWrite(A22, map(y_val,0,640,0,4095));
            //Serial.print("map_y_val:");
            Serial.println(map(y_val,0,640,0,4095));
            while (usec < 3) ; // wait
            usec = usec - 3;
            buff="";
          }
        }
      
    }
    // close the file:
    myFile.close();
  } else {
  	// if the file didn't open, print an error:
    //Serial.println("error opening test.txt");
  }
}
