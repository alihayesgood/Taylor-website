import yt_dlp
import os

def download_pop_hits():
    if not os.path.exists('./music'):
        os.makedirs('./music')

    # 这里列出你想下载的歌
    songs = [
        "Taylor Swift cardigan",
        "Taylor Swift august",
        "Sabrina Carpenter Espresso",
        "Billie Eilish Birds of a Feather"
    ]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './music/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch1', # 搜索并取第一个结果
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for song in songs:
            print(f"🎤 正在为你搜寻: {song}...")
            try:
                ydl.download([song])
            except Exception as e:
                print(f"❌ 下载 {song} 失败，可能需要安装 FFmpeg: {e}")

if __name__ == "__main__":
    download_pop_hits()