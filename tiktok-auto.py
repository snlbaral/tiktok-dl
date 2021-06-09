from downloader.vdownloader import TikTokSelf, TikTok

if __name__ == '__main__':
    username = input("TikTok UserName: \n")
    username = TikTok.strip_username(username)
    try:
        TikTokSelf.get_links_and_download(username)
    except Exception as e:
        print(e)