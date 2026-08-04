# Ambient互換のWebサーバをミニマム構成で構築する方法

ambient.ioに依存しているのはあとあと困りそうでしたので、自分のサーバを立てて、そこでAmbient.io互換のWebサーバを立てることにしました。

OCI(Oracle Cloud Infrastructure)の永久無料サーバで構築できます。

OCIにUbuntu24.04.LTSサーバを立て、
Python3とsqlite3をインストールし、
`main.py`を適当なディレクトリに置きます。

`ambient.service` を `/etc/systemd/system/ambient.service`において  
`systemctl enable ambient.service`  
とすると起動スクリプトが登録されます。

`sudo systemctl start ambient.service`

でポート8080でWebサーバが起動します。

Arduino IDEでlibraryフォルダを探し、Ambient.cを開き、サーバのアドレス(ambient.io)を上記のIPアドレスに置換します。ポートを80から8080に変更します。
Arduino IDEで再コンパイルをすれば、自動的にlibraryのソースコードも再コンパイルされます。

