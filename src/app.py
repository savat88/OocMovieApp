from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

def clean_youtube_url(url):
    # ตัดพารามิเตอร์ออกจาก URL
    return url.split('?')[0]

def get_video_url(video_url):
    try:
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])

            # เลือกสตรีมที่มีทั้งเสียงและวิดีโอ (progressive)
            progressive_streams = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') != 'none']

            # เรียงลำดับสตรีมตามคุณภาพ (ความสูงของวิดีโอ)
            progressive_streams.sort(key=lambda x: x.get('height', 0), reverse=True)

            # เลือกสตรีมที่ดีที่สุด
            best_stream = progressive_streams[0] if progressive_streams else None
            return best_stream['url'] if best_stream else None

    except Exception as e:
        print("เกิดข้อผิดพลาด:", e)
        return None

@app.route('/get-video-url', methods=['POST'])
def get_video_url_api():
    data = request.json
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': 'กรุณาใส่ URL'}), 400

    # ทำความสะอาด URL โดยตัดพารามิเตอร์ออก
    clean_url = clean_youtube_url(video_url)
    video_stream_url = get_video_url(clean_url)

    if video_stream_url:
        return jsonify({'video_url': video_stream_url}), 200
    else:
        return jsonify({'error': 'ไม่สามารถดึงลิงก์วิดีโอได้'}), 400

if __name__ == '__main__':
    app.run()
