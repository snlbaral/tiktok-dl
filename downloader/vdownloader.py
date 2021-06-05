import youtube_dl
from TikTokApi import TikTokApi


class TikTok:
    def get_link(tiktok_dict):
        user_name = tiktok_dict['author']['uniqueId']
        video_id = tiktok_dict['id']
        video_link = 'https://www.tiktok.com/@{}/video/{}?lang=en'.format(user_name, video_id)
        return video_link

    def download_tiktok(url, path):
        ydl_opts = {
            'outtmpl': 'downloads\%s \%(extractor)s-%(id)s-%(title)s.%(ext)s'.replace("%s ", path),
            'ignoreerrors': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def is_integer(input_number):
        is_true = False
        try:
            int(input_number)
            is_true = int(input_number)
        except ValueError:
            is_true = False
        return is_true

    def strip_username(username):
        if '@' in username:
            username = str.replace(username, '@', '')
        return username


