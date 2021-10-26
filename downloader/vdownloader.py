import concurrent.futures
import youtube_dl
import time
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TikTok:
    def __init__(self, username):
        self.username = username
        try:
            self.browser = webdriver.Chrome(chromedriver_autoinstaller.install())
        except:
            self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def scroll_bottom(self, last_height=0, wait_scroll=2, loading_xpath=None):
        self.check_captcha()
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        print("Loading Videos...")
        new_height = self.browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(1)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            return
        last_height = new_height
        time.sleep(wait_scroll)
        self.scroll_bottom(last_height)

    def get_links_and_download(self):
        print("Keep The Browser Tab Open, Do Not Minimize To Get Accurate Results...")
        self.browser.set_window_size(414, 816)
        self.browser.get("https://www.tiktok.com/@"+self.username+"?lang=en")
        self.check_captcha()
        self.scroll_bottom()
        links = self.browser.find_elements_by_tag_name("a")
        urls = []
        print("All Videos Loaded. Generating Links...")
        for link in links:
            if link.get_attribute("href"):
                if "@"+self.username+"/video/" in link.get_attribute("href"):
                    urls.append(link.get_attribute("href"))
        self.browser.close()
        if len(urls) > 0:
            print("{} Videos Found!".format(len(urls)))
            print("Starting Downlods...")
            time.sleep(0.5)
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                exe = {executor.submit(download_tiktok, url, self.username) for url in urls}
        else:
            print("No Videos Found For User: @"+self.username)
            exit()

    def check_captcha(self):
        captcha = self.browser.find_elements_by_xpath("//div[@class='verify-wrap']")
        if captcha:
            print("Open The Minimized Browser & Resolve The Captcha...")
            try:
                wait = WebDriverWait(self.browser, 100)
                wait.until(EC.presence_of_all_elements_located((By.ID, 'main')))
            except Exception as e:
                print("Unable to reach tiktok or get the element at it...")
                print("Close The Browser & Give It Another Go...")
                print("Report It, If It Is Happening Frequently!")
                exit(404)
        time.sleep(2)
        body_captcha = self.browser.find_elements_by_xpath("//body[@class='captcha-disable-scroll']")
        if body_captcha:
            print("Open The Minimized Browser & Resolve The Captcha...")
            try:
                wait = WebDriverWait(self.browser, 100)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//body[@class='']")))
            except Exception as e:
                print("Unable to reach tiktok or get the element at it..")
                print("Close The Browser & Give It Another Go...")
                print("Report It, If It Is Happening Frequently!")
                exit(404)
        time.sleep(1)


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


def get_link(tiktok_dict):
    user_name = tiktok_dict['author']['uniqueId']
    video_id = tiktok_dict['id']
    video_link = 'https://www.tiktok.com/@{}/video/{}?lang=en'.format(user_name, video_id)
    return video_link


def strip_username(username):
    if '@' in username:
        username = str.replace(username, '@', '')
    return username