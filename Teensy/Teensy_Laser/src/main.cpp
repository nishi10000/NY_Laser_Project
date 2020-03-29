/*
  SD card read
 
 * SD card attached to SPI bus as follows:
 ** MOSI - pin 11, pin 7 on Teensy with audio board
 ** MISO - pin 12
 ** CLK - pin 13, pin 14 on Teensy with audio board
 ** CS - pin 4, pin 10 on Teensy with audio board
  
 */
#include <Arduino.h>
#include <SD.h>
#include <SPI.h>
#include <MsTimer2.h>
File myFile;
const int chipSelect = BUILTIN_SDCARD;// Teensy 3.5 & 3.6 on-board: BUILTIN_SDCARD
#define file_name "movie_~1.txt"//img_test.txt//movie_~1.txt
#define lazer_on_message "lazer_on,"
#define lazer_off_message "lazer_off,"
#define frame_start_message "frame_start,"
#define frame_end_message "frame_end,"
#define lazer_output 2//pwmpin
#define lazer_on 4095
#define lazer_off 0
#define flame_time 30//30ms
#define stop_time 3//(us)loop_stoptime
//#define DEBUG //デバッグ時に記載コメントアウトする事によってifdef解除

String str;
String buff;

int x_val_count=0;//x,yを分けるカウンター
int x_val=0;//読み取ったｘとｙの値を格納する。
int y_val=0;

bool flame_end=false;//flameが終わったときに、フレームが終わったときtrueになる。

elapsedMicros wait_time = 0;
File root;

//TODO:1フレームの間は同じフレームをループさせる。
void flame_timer(){
  if(flame_end!=true){
    flame_end=true;
  }
}
//SDカードの中身を確認する。
void printDirectory(File dir, int numTabs) {
  while (true) {

    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }
    for (uint8_t i = 0; i < numTabs; i++) {
      
      Serial.print('\t');
    }
    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      printDirectory(entry, numTabs + 1);
    } else {
      // files have sizes, directories do not
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
    }
    entry.close();
  }
}

void stop_loop(elapsedMicros time){//TODO:要確認int time->elapsedMicrosに
  while (wait_time < time) ; // wait
  wait_time = wait_time - time;
}

void setup()
{
  analogWriteResolution(12);
  Serial.begin(9600);
  while (!Serial) {
     // wait for serial port to connect. Needed for Leonardo only
  }
  Serial.print("Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    Serial.println("initialization failed!");
    delay(500);
    return;
  }
  Serial.println("initialization done.");
//SDカードの中身を確認する。
  root = SD.open("/");
  printDirectory(root,0);
  Serial.println("done!");
  Serial.println("setup!");
  MsTimer2::set(15, flame_timer); //30fps...15だったら60fps
  MsTimer2::start();
}


void loop()
{
  int flame_start_pos=0;
	myFile = SD.open(file_name, FILE_READ);
  str="";//str初期化
  buff="";
  int count=0;
  if(!myFile){
    Serial.println("Can not open file!");//もしもSDカードが読み込めなかった場合は、SDカードのディレクトリを確認する。
    root = SD.open("/");
    printDirectory(root,0);
    Serial.println("done!");
    Serial.println("loop");
    delay(500);
    return;
  }
  while (myFile.available()) {
    str = char(myFile.read());//1biteずつ格納される。
    count++;
    buff += str;
    if(str==','){
      /*構想
      ：framestartの場所を記憶してflame時間分経過していなければ、ループさせる。
      */
      if(buff.equals(frame_start_message)){
        flame_start_pos=myFile.position();
        #ifdef DEBUG
        Serial.println("FRAME_START");
        #endif
      }else
      if(buff.equals(lazer_off_message)){
        #ifdef DEBUG
        Serial.println("LAZER_OFF");  
        #endif
        analogWrite(lazer_output,lazer_off);        
      }else
      if(buff.equals(lazer_on_message)){
        #ifdef DEBUG
        Serial.println("LAZER_ON");
        #endif
        analogWrite(lazer_output,lazer_on);          
      }else
      if(buff.equals(frame_end_message)){
        if(!flame_end){//もし時間がフレーム分経過していなかったら、読み込みのポイントをflame_start_posへシークさせる。
          #ifdef DEBUG
          Serial.println("FRAME_REPEAT");
          #endif
          myFile.seek(flame_start_pos);
        }else{
          flame_end=false;
          #ifdef DEBUG
          Serial.println("FRAME_END");
          #endif
        }
      }else{
        buff=buff.trim();
        buff.remove(buff.indexOf(","), 1);
        int val = buff.toInt();
        if(x_val_count==0){
          x_val_count++;
          x_val=val;
          analogWrite(A21, map(x_val,0,480,0,4095));
          #ifdef DEBUG
          Serial.print("x:");
          Serial.println(map(x_val,0,480,0,4095));
          #endif
        }else{
          x_val_count=0;
          y_val=val;
          analogWrite(A22, map(y_val,0,480,0,4095));
          #ifdef DEBUG
          Serial.print("y:");
          Serial.println(map(y_val,0,480,0,4095));
          #endif
        }
      }
      stop_loop(stop_time);
      
      buff="";
    }
  }
  myFile.close();
}

