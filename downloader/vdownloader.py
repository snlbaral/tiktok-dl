import concurrent.futures
import youtube_dl
import time
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TikTokSelf:
    def scroll_bottom(browser, last_height=0, wait_scroll=2, loading_xpath=None):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        print("Loading Videos...")
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(1)
            new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            return
        last_height = new_height
        time.sleep(wait_scroll)
        TikTokSelf.scroll_bottom(browser, last_height)

    def get_links_and_download(username):
        try:
            browser = webdriver.Chrome(chromedriver_autoinstaller.install())
        except:
            browser = webdriver.Chrome(ChromeDriverManager().install())
        print("Keep The Browser Tab Open, Do Not Minimize To Get Accurate Results...")
        browser.set_window_size(414, 816)
        browser.get("https://www.tiktok.com/@"+username+"?lang=en")
        captcha = browser.find_elements_by_xpath("//div[@class='verify-wrap']")
        if captcha:
            print("Open The Minimized Browser & Resolve The Captcha...")
            try:
                wait = WebDriverWait(browser, 100)
                wait.until(EC.presence_of_all_elements_located((By.ID, 'main')))
            except Exception as e:
                print("Unable to reach tiktok or get the element at it...")
                print("Close The Browser & Give It Another Go...")
                print("Report It, If It Is Happening Frequently!")
                exit(404)
        time.sleep(2)
        body_captcha = browser.find_elements_by_xpath("//body[@class='captcha-disable-scroll']")
        if body_captcha:
            print("Open The Minimized Browser & Resolve The Captcha...")
            try:
                wait = WebDriverWait(browser, 100)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//body[@class='']")))
            except Exception as e:
                print("Unable to reach tiktok or get the element at it...")
                print("Close The Browser & Give It Another Go...")
                print("Report It, If It Is Happening Frequently!")
                exit(404)        	
        time.sleep(1)
        TikTokSelf.scroll_bottom(browser)
        links = browser.find_elements_by_tag_name("a")
        urls = []
        print("All Videos Loaded. Generating Links...")
        for link in links:
            if link.get_attribute("href"):
                if "@"+username+"/video/" in link.get_attribute("href"):
                    urls.append(link.get_attribute("href"))
        browser.close()
        if len(urls) > 0:
            print("{} Videos Found!".format(len(urls)))
            print("Starting Downlods...")
            time.sleep(0.5)
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                exe = {executor.submit(TikTok.download_tiktok, url, username) for url in urls}
        else:
            print("No Videos Found For User: @"+username)
            exit()



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