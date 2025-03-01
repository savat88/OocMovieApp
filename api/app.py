from flask import Flask, Response, request
import requests

app = Flask(__name__)

@app.route('/play')  # เปลี่ยนเส้นทางจาก /proxy เป็น /play
def play():
    # รับพารามิเตอร์ stream_id
    stream_id = request.args.get('stream_id')
    if not stream_id:
        return "กรุณาระบุ stream_id", 400

    # ลิงก์สตรีมมิ่งจริง (ใช้ string formatting แบบ Python 2.7)
    stream_url = "http://45.150.128.170:8080/live/playidtv1/12345/{0}.ts".format(stream_id)

    # ตั้งค่า headers
    headers = {
        "User-Agent": "Muslim Player",
        "Accept": "*/*"
    }

    # ดึงข้อมูลสตรีมมิ่ง
    try:
        response = requests.get(stream_url, headers=headers, stream=True)
        if response.status_code != 200:
            return "ไม่สามารถเปิดสตรีมมิ่งได้", 500

        # ส่งข้อมูลสตรีมมิ่งไปยังผู้ใช้
        return Response(
            response.iter_content(chunk_size=1024),
            content_type="video/mp2t"
        )
    except Exception as e:
        return "เกิดข้อผิดพลาด: {0}".format(str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
  
