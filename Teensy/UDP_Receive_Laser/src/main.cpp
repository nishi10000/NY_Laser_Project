/*
    UDPコマンドを受けて動作を行う。
    フレームの管理は行わない。※送信側に依存する。
*/

#include <SPI.h>          // needed for Arduino versions later than 0018
#include <Ethernet.h>
#include <EthernetUdp.h>  // UDP library from: bjoern@cs.stanford.edu 12/30/2008
#include <string.h> 

#define LASER_ON "laser_on"
#define LASER_OFF "laser_off"


// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {  
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168,11,177);

unsigned int localPort = 8888;              // local port to listen on

// buffers for receiving and sending data
char PacketBuffer[UDP_TX_PACKET_MAX_SIZE];  //buffer to hold incoming packet,
char  ReplyBuffer[] = "acknowledged";       // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

void setupToWIZ850io(){
  pinMode(9, OUTPUT);
  digitalWrite(9, LOW);    // begin reset the WIZ850io
  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);  // de-select WIZ850io
  digitalWrite(9, HIGH);   // end reset pulse
}


/*UDP部分の処理を分ける。*/
void udpReciver(){
    // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  for(unsigned i=0; i<sizeof(PacketBuffer);i++){
      PacketBuffer[i]='\0';  //Bufferを空ににする。
  };
  if(packetSize)
  {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remote = Udp.remoteIP();
    for (int i =0; i < 4; i++)
    {
      Serial.print(remote[i], DEC);
      if (i < 3)
      {
        Serial.print(".");
      }
    }
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    Udp.read(PacketBuffer,UDP_TX_PACKET_MAX_SIZE);
    Serial.println("Contents:");
    Serial.println(PacketBuffer);

    // send a reply, to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(ReplyBuffer);
    Udp.endPacket();
  }  
  //delay(10);
}

//PacketBufferに基づきGalvos電圧の調整、LaserのON/OFFを行う。
void bufferOperation(){
  if(strcmp(PacketBuffer,LASER_OFF)==0){
    Serial.println("laser_off");
  }
  if(strcmp(PacketBuffer,LASER_ON)==0){
    Serial.println("laser_on");
  }
  //TODO:DACの制御
}

void setup() {
  setupToWIZ850io();
  // start the Ethernet and UDP:  
  Ethernet.begin(mac,ip);
  Udp.begin(localPort);
  Serial.begin(9600);
}

void loop() {
  udpReciver();  //PacketBufferにUDPのデータを格納する。
  bufferOperation();  //PacketBufferに基づき動作を行う。
}


