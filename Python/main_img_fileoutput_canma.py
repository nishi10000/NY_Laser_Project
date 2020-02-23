'''
動画を取り込む。
動画のサイズを落とす。 640 * 480
動画を２値化を行う。
エッジ検出を行う。
座標を取り出す。
ファイルとして出力する。
new カンマ区切りにする。
'''

import numpy as np
import cv2
import socket
import math
from matplotlib import pyplot as plt

#define
#Curryのしきい値
Edge_min = 0
Edge_max = 10 #読み込まれる線が1pxの幅だと100では認識しない。


file_path='C:/Users/herom/Desktop/NY_Laser_Project/test_sample/sample.jpg'

lazer_on_message='lazer_on,'
lazer_off_message='lazer_off,'
frame_start_message='frame_start,'
frame_end_message='frame_end,'
'''
def send_udp_message(message):
    try:
        udp.sendto(message.encode(), address) #文字列をバイトデータに変換してaddress宛に送信
    except KeyboardInterrupt:#強制終了を検知したらソケットを閉じる
        udp.close()
'''

# アスペクト比を固定して、指定した解像度にリサイズする。
def scale_to_resolation(img, resolation):
    h, w = img.shape[:2]
    scale = math.sqrt(resolation / (h * w))
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)

    # アスペクト比を固定して、指定した大きさに収まるようリサイズする。
def scale_box(img, width, height):
    scale = min(width / img.shape[1], height / img.shape[0])
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)

def my_len(l):#リストの数を数える
    count = 0
    if isinstance(l, list):
        for v in l:
            count += my_len(v)
        return count
    else:
        return 1

#画像を取り込む
try:
    img = cv2.imread(file_path,cv2.IMREAD_UNCHANGED)
    print (img.shape)
    
#取り込めなかった場合。
except cv2.error:
    print('you can not open file')

#send_message初期化
send_message=''


#dst = scale_to_resolation(img, 640 * 480)
dst=scale_box(img,640,480)
#黒い画像をdst後のスケールで作成する
black_img = np.zeros((dst.shape[0],dst.shape[1],3), np.uint8)
print(dst.shape)
#ブラーをかけてノイズを飛ばす。
blur=cv2.blur(dst,(3,3))
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
cv2.drawContours(black_img, contours, -1, (0,255,255), 1)

#'''udpの送信でFPSが落ちる。おそらくpytyon状のfor分の影響だと考えられる。
#ポイントの数を下げる関数を考えるかｃ＋＋にするか。
#send_udp_message(frame_start_message)
send_message=send_message+frame_start_message
for i in range(len(contours)):
    #print(my_len(contours))
    first_flag=1
    #send_udp_message(lazer_off_message)
    send_message=send_message+lazer_off_message
    for j in range(len(contours[i])):
        for k in range(len(contours[i][j])):
            #print(len(contours[i][j]))            
            data=', '.join(map(str, contours[i][j][k]))
            msg = data #送信する文字列
            #print(msg)
            if first_flag==1:
                first_flag=0                    
            elif first_flag==0:
                #send_udp_message(lazer_on_message)
                send_message=send_message+lazer_on_message
                first_flag=2
            #send_udp_message(msg)
            send_message=send_message+msg
            send_message=send_message+','
send_message=send_message+frame_end_message 
            
#'''



path_w = 'C:/Users/herom/Desktop/NY_Laser_Project/output/img_test.txt'

s = send_message

with open(path_w, mode='w') as f:
    f.write(s)

plt.imshow(black_img)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

