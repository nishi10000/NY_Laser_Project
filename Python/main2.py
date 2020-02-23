import numpy as np
import cv2
import socket
#define
#Curryのしきい値
Edge_min = 100
Edge_max = 200

lazer_on_message='lazer_on'
lazer_off_message='lazer_off'
frame_start_message='frame_start'
def send_udp_message(message):
    try:
        udp.sendto(message.encode(), address) #文字列をバイトデータに変換してaddress宛に送信
    except KeyboardInterrupt:#強制終了を検知したらソケットを閉じる
        udp.close()

def my_len(l):
    count = 0
    if isinstance(l, list):
        for v in l:
            count += my_len(v)
        return count
    else:
        return 1

cap = cv2.VideoCapture('C:/Users/herom/Videos/AKIRA 　金田と鉄雄の対決-Vk_AuM6ozks.mp4')
ret, frame = cap.read()
#画像サイズを求める。
height, width = frame.shape[:2]
print(height) 
print(width)
while(cap.isOpened()):
    ret, frame = cap.read()

    #ブラーをかけてノイズを飛ばす。
    blur=cv2.blur(frame,(3,3))
    # グレースケース化
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    #CannyにてEdge取り出し。
    edges = cv2.Canny(gray,Edge_min,Edge_max)

    #二値化
    ret,thresh2 = cv2.threshold(edges,127,255,cv2.THRESH_BINARY)

    #output_image
    output = thresh2

    #輪郭の取り出し
    contours, hierarchy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #輪郭を描画
    cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    address = ('127.0.0.1', 1308) #送信相手のIPアドレスと通信に使うポート番号の設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #udpという名前のUDPソケットを生成

    #'''udpの送信でFPSが落ちる。おそらくpytyon状のfor分の影響だと考えられる。
    #ポイントの数を下げる関数を考えるかｃ＋＋にするか。
    send_udp_message(frame_start_message)
    for i in range(len(contours)):
        #print(my_len(contours))
        #print(type(contours))
        first_flag=1
        send_udp_message(lazer_off_message)
        for j in range(len(contours[i])):
            for k in range(len(contours[i][j])):
                #print(len(contours[i][j]))            
                #for l in range(len(contours[i][j][k])):
                data=', '.join(map(str, contours[i][j][k]))
                msg = data #送信する文字列
                #print(msg)
                if first_flag==1:
                    first_flag=0                    
                elif first_flag==0:
                    send_udp_message(lazer_on_message)
                    first_flag=2
                send_udp_message(msg)
            
                
    #'''
    
    cv2.imshow('frame',output)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

