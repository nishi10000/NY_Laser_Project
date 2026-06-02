# NY_Laser_Project

レーザーポインター/レーザープロジェクターを自作するための初期プロジェクトです。
Python + OpenCVで画像や動画から座標データを作成し、Teensy側で読み込んでGalvoへ出力する構成を試しています。

## 概要

- Python + OpenCVで画像/動画を解析
- 画像や動画からレーザー描画用の座標データを生成
- 生成した`.txt`データをSDカード等へ保存
- Teensy 3.6でデータを読み込み、X/Yをanalog outputしてGalvoへ出力

## 構成

- `Python/` - 画像/動画から座標データを生成するPythonツール
- `Teensy/` - Teensy側の読み込み/出力プログラム
- `LICENSE` - ライセンス

## Python側

GUI付きの変換ツールがあります。

- `Python/GUI.py` - Tkinter GUI
- `Python/movie_to_txt.py` - 動画からテキストデータへ変換
- `Python/Image_Output.py` など - 画像変換系の試作コード

必要な主なライブラリ:

- Python
- OpenCV (`cv2`)
- NumPy

## Demo

![1](https://user-images.githubusercontent.com/34505055/79874389-4126b900-8423-11ea-8205-ff25dad1f37c.gif)

![GUI](https://user-images.githubusercontent.com/34505055/79874393-42f07c80-8423-11ea-8aac-e892a3af829f.gif)

## 関連

この後継/発展版として、UDP通信やC++/OpenCV活用を試したプロジェクトがあります。

- [NY_Laser_project_v2.0](https://github.com/nishi10000/NY_Laser_project_v2.0)
