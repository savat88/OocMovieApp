from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    url = "http://45.144.165.187:8080/playidtv1/12345/17715"  # เปลี่ยนเป็น URL ที่ต้องการ
   # headers = {
    #    "User-Agent": "Custom User-Agent"  # เปลี่ยนให้เป็นข้อความที่ไม่มีตัวอักษรพิเศษ
  #  }

    # หรือถ้าต้องการใช้ภาษาไทย, แนะนำให้ encode ข้อความเป็น utf-8
    headers = {
         "User-Agent": "ไม่อนุญาตแกะลิงค์".encode('utf-8')
     }

    response = requests.get(url, headers=headers, stream=True)

    return Response(
        response.iter_content(chunk_size=1024),
        content_type=response.headers.get('Content-Type', 'application/vnd.apple.mpegurl')
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # ใช้ host='0.0.0.0' และ port=8080
