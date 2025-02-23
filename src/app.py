from flask import Flask, Response
import requests

app = Flask(__name__)

m3u8_urls = [
    "http://45.144.165.187:8080/playidtv1/12345/17237",
    "http://45.144.165.187:8080/playidtv1/12345/37", 
    "http://45.144.165.187:8080/playidtv1/12345/17788"
    "http://45.144.165.187:8080/playidtv1/12345/18922"
    "http://45.144.165.187:8080/playidtv1/12345/18833"
    "http://45.144.165.187:8080/playidtv1/12345/11052"
    "http://45.144.165.187:8080/playidtv1/12345/18669"
    "http://45.144.165.187:8080/playidtv1/12345/9198.m3u8"
    "http://45.144.165.187:8080/playidtv1/12345/84"
    "http://45.144.165.187:8080/playidtv1/12345/15672"
]

@app.route('/proxy/<int:index>')
def proxy(index):
    if index < 0 or index >= len(m3u8_urls):
        return "URL not found", 404
    
    url = m3u8_urls[index]

    headers = {
        "User-Agent": "ไม่อนุญาตแกะลิงค์".encode('utf-8')
    }

    response = requests.get(url, headers=headers, stream=True)

    return Response(
        response.iter_content(chunk_size=1024),
        content_type=response.headers.get('Content-Type', 'application/vnd.apple.mpegurl')
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
