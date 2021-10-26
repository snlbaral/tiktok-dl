from downloader.vdownloader import TikTok
from downloader.vdownloader import strip_username

if __name__ == '__main__':
    username = input("TikTok UserName: \n")
    username = strip_username(username)
    try:
        tiktok = TikTok(username)
        tiktok.get_links_and_download()
    except Exception as e:
        print(e)
