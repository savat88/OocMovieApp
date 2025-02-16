from flask import Flask, request, jsonify
from pyngrok import ngrok  # ใช้ pyngrok แทน flask_ngrok
from yt_dlp import YoutubeDL

app = Flask(__name__)

# เลือกพอร์ตที่ไม่ถูกใช้งาน เช่น 5001
#public_url = ngrok.connect(5001)  # ใช้พอร์ต 5001
#print(' * ngrok tunnel "http://127.0.0.1:5001" -> "http://{}"'.format(public_url))

# ฟังก์ชันในการดึง URL ของวิดีโอ
def clean_youtube_url(url):
    return url.split('?')[0]

def get_video_url(video_url):
    try:
        ydl_opts = {
            'geo_bypass': True,  # ข้ามข้อจำกัดทางภูมิศาสตร์
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # ตัวระบุผู้ใช้
            'cookies': 'cookies.txt',  # ถ้าคุณมีคุกกี้สามารถใช้ไฟล์ cookies.txt
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            progressive_streams = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') != 'none']
            progressive_streams.sort(key=lambda x: x.get('height', 0), reverse=True)
            best_stream = progressive_streams[0] if progressive_streams else None
            return best_stream['url'] if best_stream else None
    except Exception as e:
        return str(e)

@app.route('/get-video-url', methods=['POST'])
def get_video_url_api():
    data = request.json
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': 'กรุณาใส่ URL'}), 400

    clean_url = clean_youtube_url(video_url)
    video_stream_url = get_video_url(clean_url)

    if video_stream_url:
        return jsonify({'video_url': video_stream_url}), 200
    else:
        return jsonify({'error': 'ไม่สามารถดึงลิงก์วิดีโอได้'}), 400

if __name__ == '__main__':
    app.run()  # ใช้พอร์ต 5001
