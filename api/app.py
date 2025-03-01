from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/api/app')
def play():
    stream_id = request.args.get('stream_id')
    if not stream_id:
        return "กรุณาระบุ stream_id", 400

    stream_url = "http://45.150.128.170:8080/live/playidtv1/12345/{0}.ts".format(stream_id)

    headers = {"User-Agent": "Muslim Player", "Accept": "*/*"}

    try:
        response = requests.get(stream_url, headers=headers, stream=True)
        if response.status_code != 200:
            return f"ไม่สามารถเปิดสตรีมมิ่งได้, สถานะ: {response.status_code}", 500
        return Response(response.iter_content(chunk_size=1024), content_type="video/mp2t")
    except requests.exceptions.RequestException as e:
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}", 500
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
