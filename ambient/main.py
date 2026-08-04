# Ambient互換の最もシンプルなWebサーバ

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI()

def init_db():
    conn = sqlite3.connect('ambient.db')
    c = conn.cursor()
    # センサーデータ用テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT,
            created_at TEXT,
            d1 REAL, d2 REAL, d3 REAL, d4 REAL, d5 REAL, d6 REAL, d7 REAL, d8 REAL
        )
    ''')
    # チャンネルおよび WRITE_KEY 管理用テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            write_key TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- 1. データ受信 (POST) [WRITE_KEY 検証付き] ---
@app.post("/api/v2/channels/{channel_id}/data")
async def receive_ambient_data(channel_id: str, request: Request):
    body = await request.json()
    write_key = body.get('writeKey')

    if not write_key:
        raise HTTPException(status_code=400, detail="writeKey is required")

    conn = sqlite3.connect('ambient.db')
    c = conn.cursor()

    # チャンネルの登録状況を確認
    c.execute('SELECT write_key FROM channels WHERE channel_id = ?', (channel_id,))
    row = c.fetchone()

    if row is None:
        # 未登録のチャンネルの場合、初回の writeKey を自動登録する
        c.execute('INSERT INTO channels (channel_id, write_key) VALUES (?, ?)', (channel_id, write_key))
        conn.commit()
    else:
        # 登録済みの場合は writeKey を照合
        saved_write_key = row[0]
        if saved_write_key != write_key:
            conn.close()
            raise HTTPException(status_code=403, detail="Invalid writeKey")

    # データ保存
    created_at = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO sensor_data (channel_id, created_at, d1, d2, d3, d4, d5, d6, d7, d8)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        channel_id, created_at,
        body.get('d1'), body.get('d2'), body.get('d3'), body.get('d4'),
        body.get('d5'), body.get('d6'), body.get('d7'), body.get('d8')
    ))
    conn.commit()
    conn.close()

    return {"status": "ok"}

# --- 2. グラフ用データ取得 (GET API) ---
@app.get("/api/v2/channels/{channel_id}/data")
async def get_ambient_data(channel_id: str, limit: int = 100):
    conn = sqlite3.connect('ambient.db')
    c = conn.cursor()
    c.execute('''
        SELECT created_at, d1, d2, d3, d4, d5, d6, d7, d8
        FROM sensor_data
        WHERE channel_id = ?
        ORDER BY id DESC LIMIT ?
    ''', (channel_id, limit))
    rows = c.fetchall()
    conn.close()

    rows.reverse()

    data = []
    for r in rows:
        data.append({
            "created_at": r[0],
            "d1": r[1], "d2": r[2], "d3": r[3], "d4": r[4],
            "d5": r[5], "d6": r[6], "d7": r[7], "d8": r[8]
        })
    return JSONResponse(content=data)

# --- 3. ダッシュボード画面 (HTML + Chart.js) ---
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ambient Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: sans-serif; margin: 20px; background: #f4f6f8; }
            .container { max-width: 1000px; margin: 0 auto; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
            h1 { color: #333; margin-top: 0; }
            .controls { margin-bottom: 15px; }
            select, input { padding: 6px 12px; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>My Piano データダッシュボード</h1>
                <div class="controls">
                    <label>チャンネルID: </label>
                    <input type="text" id="channelId" value="100492" placeholder="100492">
                    <button onclick="loadChart()">更新</button>
                </div>
                <canvas id="sensorChart" width="400" height="200"></canvas>
            </div>
        </div>

        <script>
            let myChart = null;

            async function loadChart() {
                const channelId = document.getElementById('channelId').value;
                const response = await fetch(`/api/v2/channels/${channelId}/data?limit=50`);
                const data = await response.json();

                const labels = data.map(item => item.created_at);
                const d1Data = data.map(item => item.d1);
                const d2Data = data.map(item => item.d2);

                const ctx = document.getElementById('sensorChart').getContext('2d');

                if (myChart) {
                    myChart.destroy();
                }

                myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'd1 (温度)',
                                data: d1Data,
                                borderColor: 'rgb(255, 99, 132)',
                                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                                tension: 0.2,
                                spanGaps: true
                            },
                            {
                                label: 'd2 (湿度)',
                                data: d2Data,
                                borderColor: 'rgb(54, 162, 235)',
                                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                                tension: 0.2,
                                spanGaps: true
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: { title: { display: true, text: '日時' } },
                            y: { title: { display: true, text: '数値' } }
                        }
                    }
                });
            }

            loadChart();
            setInterval(loadChart, 30000);
        </script>
    </body>
    </html>
    """
    return html_content
