'''
動画を取り込んで、txtファイルに変換。

通信仕様変更したほうがいい気がする。
コマンド系は、改行コード
のみframe_start \ n
lazer_off \ n

座標系は、、カンマ
区切りと改行23,285 \ n
24,284 \ n

基本は改行コードで切り分けていき、カンマ区切りで座標のｘ、yを分ける。
'''

import numpy as np
import cv2
import socket
import math
#define
#Curryのしきい値
Edge_min = 100
Edge_max = 200

delay = 1
#C:/Users/herom/Desktop/NY_Laser_Project/NY_Laser_Project/test_sample_image/blading.mov
#C:/Users/nishiharay/Desktop/NY_Laser_Project/trunk/output_txt/output.txt
file_path='C:/Users/nishiharay/Videos/max_media_movie/blading.mov'
file_write_path = 'C:/Users/nishiharay/Desktop/NY_Laser_Project/trunk/output_txt/output.txt'

lazer_on_message='lazer_on\n'
lazer_off_message='lazer_off\n'
frame_start_message='frame_start\n'
frame_end_message='frame_end\n'

#画像取り込み後の最大サイズ。
Image_Scale_X=480
Image_Scale_Y=480

# アスペクト比を固定して、指定した解像度にリサイズする。
def scale_to_resolation(img, resolation):
    h, w = img.shape[:2]
    scale = math.sqrt(resolation / (h * w))
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)

# アスペクト比を固定して、指定した大きさに収まるようリサイズする。
def scale_box(img, width, height):
    scale = min(width / img.shape[1], height / img.shape[0])
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)

#動画を取り込む
try:
    cap = cv2.VideoCapture(file_path)
#取り込めなかった場合。
except cv2.error:
    print('you can not open file')

#ビデオ情報表示
print('width:',cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print('height:',cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('FPS:',cap.get(cv2.CAP_PROP_FPS))
print('FrameCount:',cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameconut=cap.get(cv2.CAP_PROP_FRAME_COUNT)
print('Movie_time:',cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))

#1frameに変換
ret, frame = cap.read()

#動画保存用変数
#fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
#out = cv2.VideoWriter('output.mp4',fourcc, cap.get(cv2.CAP_PROP_FPS), (Image_Scale_X,Image_Scale_Y),True)

#send_message初期化
send_message=''
while(cap.isOpened()):
    ret, frame = cap.read()
    #frameをリサイズ
    scaled_img=scale_box(frame,Image_Scale_X,Image_Scale_Y)
    #ブラーをかけてノイズを飛ばす。
    blur=cv2.blur(scaled_img,(3,3))
    # グレースケース化
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    #画像を反転
    gray=cv2.flip(gray,0)

    #CannyにてEdge取り出し。
    edges = cv2.Canny(gray,Edge_min,Edge_max)

    #二値化
    ret,thresh2 = cv2.threshold(edges,127,255,cv2.THRESH_BINARY)

    #output_image
    output = thresh2

    #輪郭の取り出し
    contours, hierarchy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #輪郭を描画
    cv2.drawContours(frame, contours, -1, (0,255,0), 1)
    #動画を表示
    '''
    if ret:
        cv2.imshow("Check_Movie", output)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    #'''
    #動画として書き出し
    #out.write(output)
    #'''udpの送信でFPSが落ちる。おそらくpytyon状のfor分の影響だと考えられる。
    #ポイントの数を下げる関数を考えるかｃ＋＋にするか。
    send_message=send_message+frame_start_message
    for i in range(len(contours)):
        first_flag=1
        send_message=send_message+lazer_off_message
        for j in range(len(contours[i])):
            for k in range(len(contours[i][j])):
                data=','.join(map(str, contours[i][j][k]))
                msg = data #送信する文字列
                if first_flag==1:
                    first_flag=0                    
                elif first_flag==0:
                    send_message=send_message+lazer_on_message
                    first_flag=2
                send_message=send_message+msg
                send_message=send_message+'\n'
    send_message=send_message+frame_end_message        
                
    #'''
    #今のフレーム数を確認する。
    print(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if (cap.get(cv2.CAP_PROP_POS_FRAMES)==frameconut):
    #保存するためループを抜ける。
        break

with open(file_write_path, mode='w') as f:
    f.write(send_message)

cap.release()
cv2.destroyAllWindows()

