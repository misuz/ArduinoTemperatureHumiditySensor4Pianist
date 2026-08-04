# Ambient互換のWebサーバをミニマム構成で構築する方法

ambient.ioに依存しているのはあとあと困りそうでしたので、自分のサーバを立てて、そこでAmbient.io互換のWebサーバを立てることにしました。

OCI(Oracle Cloud Infrastructure)の永久無料サーバで構築できます。

## 簡単な手順

### OCIにUbuntu24.04.LTSサーバを立てます。

このとき、注意点としては、OCIのUbuntu24.04サーバは、デフォルトでiptablesが動作しており、ssh(TCP/22)以外は全ポートクローズの設定になっています。  
そのため、iptablesでポートTCP/8080の解放の設定が必要です。  
その後に、OCIのVNICのセキュリティ設定で、ポートTCP/8080を開放する設定も必要です。  


### Python3とsqlite3をインストール

`main.py`を適当なディレクトリに置きます。

`ambient.service` を `/etc/systemd/system/ambient.service`において  
```shell
systemctl enable ambient.service
```
とすると起動スクリプトが登録されます。

```shell
sudo systemctl start ambient.service
```

でポート8080でWebサーバが起動します。

Arduino IDEでlibraryフォルダを探し、Ambient.cを開き、サーバのアドレス(ambient.io)を上記のIPアドレスに置換します。ポートを80から8080に変更します。
Arduino IDEで再コンパイルをすれば、自動的にlibraryのソースコードも再コンパイルされます。

