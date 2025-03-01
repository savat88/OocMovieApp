import requests
from flask import Response

def handler(request):
    try:
        # รับพารามิเตอร์ stream_id จากคำขอ
        stream_id = request.args.get('stream_id')
        if not stream_id:
            return "กรุณาระบุพารามิเตอร์ stream_id", 400

        # สร้างลิงก์สตรีม
        stream_url = "http://45.150.128.170:8080/live/playidtv1/12345/{0}.ts".format(stream_id)

        # ตั้งค่า headers
        headers = {
            "User-Agent": "Muslim Player",
            "Accept": "*/*"
        }

        # ดึงข้อมูลสตรีม
        response = requests.get(stream_url, headers=headers, stream=True)

        # ตรวจสอบสถานะการตอบกลับ
        if response.status_code != 200:
            return f"ไม่สามารถเปิดสตรีมมิ่งได้, สถานะ: {response.status_code}", 500

        # ส่งข้อมูลสตรีมไปยังผู้ใช้
        return Response(
            response.iter_content(chunk_size=1024),
            content_type="video/mp2t"
        )
    except requests.exceptions.RequestException as e:
        # จับข้อผิดพลาดจาก requests
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}", 500
    except Exception as e:
        # จับข้อผิดพลาดทั่วไป
        return f"เกิดข้อผิดพลาด: {str(e)}", 500
