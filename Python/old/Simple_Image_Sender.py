import matplotlib.pyplot as plt
import numpy as np
import cv2
import socket
import socket #通信用

#define
#Curryのしきい値
Edge_min = 100
Edge_max = 200


#画像(shimarisu.jpg)の読み込み
img = cv2.imread("C:/Users/herom/Pictures/sample/sample1.png")

#define
#Curryのしきい値
Edge_min = 100
Edge_max = 200

lazer_on_message='lazer_on'
lazer_off_message='lazer_off'

#画像サイズを求める。
height, width = img.shape[:2]
print(height) 
print(width)

#画像の表示
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # OpenCV は色がGBR順なのでRGB順に並べ替える
plt.show()

#ブラーをかけてノイズを飛ばす。
blur=cv2.blur(img,(3,3))

# グレースケース化
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

#CannyにてEdge取り出し。
edges = cv2.Canny(gray,Edge_min,Edge_max)

#二値化
ret,thresh2 = cv2.threshold(edges,127,255,cv2.THRESH_BINARY)

#output_image
output = thresh2

#画像の表示
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB)) # OpenCV は色がGBR順なのでRGB順に並べ替える
plt.show()

#輪郭の取り出し
contours, hierarchy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#輪郭を描画
cv2.drawContours(img, contours, -1, (0,255,0), 3)

output=gray
#画像の表示
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # OpenCV は色がGBR順なのでRGB順に並べ替える
plt.show()


#print(contours)
address = ('127.0.0.1', 1308) #送信相手のIPアドレスと通信に使うポート番号の設定
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #udpという名前のUDPソケットを生成

def send_udp_message(message):
    try:
        udp.sendto(message.encode(), address) #文字列をバイトデータに変換してaddress宛に送信
    except KeyboardInterrupt:#強制終了を検知したらソケットを閉じる
        udp.close()   

for i in range(len(contours)):
    first_flag=1
    send_udp_message(lazer_off_message)
    for j in range(len(contours[i])):
        for k in range(len(contours[i][j])):
            #print(len(contours[i][j]))            
            #for l in range(len(contours[i][j][k])):
            data=', '.join(map(str, contours[i][j][k]))
            msg = data #送信する文字列
            print(msg)
            if first_flag==1:
                first_flag=0                    
            elif first_flag==0:
                send_udp_message(lazer_on_message)
                first_flag=2
            send_udp_message(msg)