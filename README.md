# ArduinoTemperatureHumiditySensor4Pianist
Temperature and Humidity Sensor for Piano conditioning by ESP32 Arduino and DHT11 sensor module.

ピアノの温度・湿度をインターネットを経由して管理するためのプロジェクトです。

## 表示例
IoTデータ可視化サービス[Ambient](https://ambidata.io/)を利用させていただいております。ありがとうございます。
![](chart.png)


## 部品
- マイコン Freenove ESP32 WROVER (カメラモジュール不要)   (1,000～3,000円くらい。WiFiモジュールがついていれば一番安いものでOK)
- 温度湿度センサー DHT11 Temperature and Humidity Sensor module.  (550円くらい)
- 抵抗器 electrical resistor 4.7KΩ x 1  (5円くらい)
- ブレッドボード Breadboard x 1 (400円くらい)
- ワイヤリングケーブル 3本 wire cables x 3.
- USB電源アダプタ（不要になったスマホ用の電源アダプタでOK）

**部品の一覧**
![使用機材](ESP32-DHT11.jpg)

**完成図**
ブレッドボードが小さすぎてセンサーが傾いてしまったのでもう少し大きいボードのほうがよいです。
![完成図](ESP32-DHT11-1.jpg)


## 開発環境

#### Arduino IDE 2.3.8
- [Arduino IDE](https://www.arduino.cc/en/software/)

**Libraries**
- Arduino IDEのツールメニューから「ライブラリを管理...」を選択してインストールできます。以下の2つをインストール。
- [Ambient ESP32 ESP8266 lib by Ambient.](https://github.com/AmbientDataInc/Ambient_ESP8266_lib)
- [DHT sensor library by Adafruit 1.4.7](https://github.com/adafruit/DHT-sensor-library)

## ソースコード

src/main.cをArduino IDEのエディタに貼り付けて、コンパイルします。

ソースコードは[こちらのサイト](https://qiita.com/denden888/items/101bd1ee937f85f355ea)を参考にさせていただきました。ありがとうございます。
