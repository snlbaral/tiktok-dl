import concurrent.futures
from downloader.vdownloader import strip_username, is_integer, get_link, download_tiktok
from TikTokApi import TikTokApi

if __name__ == '__main__':
    username = input("TikTok username: \n")
    username = strip_username(username)
    api = TikTokApi()
    try:
        # api = TikTokApi(custom_verifyFP = "CODE")
        user_videos = api.by_username(username, count=200)
        if len(user_videos) == 0:
            print("No videos found by", username)
        else:
            print(len(user_videos), "videos found.")
            no_of_videos = input("Input the no of videos you want to download\n")
            n_videos = is_integer(no_of_videos)
            if n_videos is False:
                exit("No of videos should be a type number")
            user_videos = user_videos[:n_videos]        
            user_videos = [get_link(v) for v in user_videos]
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                exe = {executor.submit(download_tiktok, url, username) for url in user_videos}
    except Exception as e:
        print(e)
