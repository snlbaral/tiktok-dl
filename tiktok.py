from downloader.vdownloader import TikTok
from TikTokApi import TikTokApi

if __name__ == '__main__':
    username = input("TikTok username: \n")
    username = TikTok.strip_username(username)
    api = TikTokApi()
    try:
        user_videos = api.byUsername(username, count=2000)
        if len(user_videos) == 0:
            print("No videos found by", username)
        else:
            print(len(user_videos), "videos found.")
            no_of_videos = input("Input the no of videos you want to download\n")
            n_videos = TikTok.is_integer(no_of_videos)
            if n_videos is False:
                exit("No of videos should be a type number")
            user_videos = user_videos[:n_videos]        
            user_videos = [TikTok.get_link(v) for v in user_videos]
            for url in user_videos:
                TikTok.download_tiktok(url, username)
    except Exception as e:
        print(e)
