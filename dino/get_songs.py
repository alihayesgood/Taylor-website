import yt_dlp
import os

def download_pop_hits():
    # 建立音乐文件夹
    if not os.path.exists('./music'):
        os.makedirs('./music')

    # 你想下载的 Taylor Swift folklore 专辑曲目和格莱美金曲
    # 只要名字写对，它就能搜到
    songs = [
        "Taylor Swift cardigan",
        "Taylor Swift august",
        "Taylor Swift willow",
        "Taylor Swift mirrorball",
        "Sabrina Carpenter Espresso",
        "Billie Eilish Birds of a Feather",
        "Teddy Swims Lose Control"
    ]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './music/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # --- 加入下面这两行进行伪装 ---
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        # ---------------------------
        'default_search': 'ytsearch1',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for song in songs:
            print(f"🎵 正在为你获取: {song}...")
            try:
                ydl.download([song])
            except Exception as e:
                print(f"❌ 下载失败: {e}")

if __name__ == "__main__":
    download_pop_hits()