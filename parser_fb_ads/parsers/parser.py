import time
import os
from load_django import *
from facebook_ads.models import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By



class FacebookAdsParser:
    """Articles csraper, see main() function to navigate throught code, what and how it does"""
    def __init__(self):
        self.DEBUG = False
        chrome_options = Options()
        service = Service(executable_path=os.path.abspath('chromedriver'))
        # chrome_options.add_argument("--window-size=500,1200")
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--enable-javascript')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--lang=en')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()


    def scrape_ads(self):

        # Находим елементы с обьявлениями
        ads = self.driver.find_elements(By.XPATH, '//div[@class="_7jvw x2izyaf x1hq5gj4 x1d52u69"]')
        existing_ads_id = {item.ad_id for item in Ad.objects.all()}

        if len(ads) == 0:
            print('[INFO] no ads availiable with this settings, try to change selected country or selected ad type')
            return False
        time.sleep(5)

        # Собираем данные с обьявления
        for ad in ads:

            try:
                ad_id = ad.find_element(By.XPATH,".//div[@class='x1rg5ohu x67bb7w']//span[@class='x8t9es0 xw23nyj xo1l8bm x63nzvj x108nfp6 xq9mrsl x1h4wwuj xeuugli']").text.lstrip('ID: ')
            except NoSuchElementException:
                ad_id = ''

            if ad_id in existing_ads_id:
                continue

            try:
                status = ad.find_element(By.XPATH,".//span[@class='x8t9es0 xw23nyj xo1l8bm x63nzvj x108nfp6 xq9mrsl x1h4wwuj xeuugli x1i64zmx']").text.strip()                 
            except NoSuchElementException:
                status = ''

            try:
                date = ad.find_element(By.XPATH,".//span[@class='x8t9es0 xw23nyj xo1l8bm x63nzvj x108nfp6 xq9mrsl x1h4wwuj xeuugli']").text.strip() 
            except NoSuchElementException:
                date = ''

            styles = {
                'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/yx/r/wn_rj7MQOhG.png"); -webkit-mask-position: 0px -522px;' : 'Facebook',
                'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/y6/r/y1FuvrbyrJG.png"); -webkit-mask-position: -14px -601px;' : 'Instagram',
                'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/yZ/r/BIcOqnqNbE9.png"); -webkit-mask-position: -106px -186px;' : 'Audience Network',
                'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/yZ/r/BIcOqnqNbE9.png"); -webkit-mask-position: -68px -289px;' : 'Messenger',
            }
            platform_block = ad.find_element(By.XPATH, './/div[@class="xeuugli x2lwn1j x6s0dn4 x78zum5 x1q0g3np"]')
            platform_items = platform_block.find_elements(By.XPATH, './/div[@class="xtwfq29"]')
            platforms_list = []

            for platform in platform_items:
                try:
                    platform_name = styles.get(platform.get_attribute('style'))
                    platforms_list.append(platform_name)
                except:
                    platforms_list = None
            if not platforms_list:
                platforms_list = None

            try:
                audience_size = ad.find_element(By.XPATH,'.//div[@class="x6s0dn4 x78zum5"]').text.strip() 
            except NoSuchElementException:
                audience_size = ''

            try:
                payment = ad.find_element(By.XPATH,'.//span[contains(text(), "(USD):")]').text.strip() 
            except NoSuchElementException:
                payment = ''

            try:
                impressions = ad.find_element(By.XPATH,'.//span[contains(text(), "Impressions")]').text.strip() 
            except NoSuchElementException:
                impressions = ''

            try:
                name_author = ad.find_element(By.XPATH,".//span[@class='x8t9es0 x1fvot60 xxio538 x108nfp6 xq9mrsl x1h4wwuj x117nqv4 xeuugli']").text.strip() 
            except NoSuchElementException:
                name_author = ''

            try:
                link = ad.find_element(By.XPATH,".//a[@class='xt0psk2 x1hl2dhg xt0b8zv x8t9es0 x1fvot60 xxio538 xjnfcd9 xq9mrsl x1yc453h x1h4wwuj x1fcty0u']")
                link = link.get_attribute('href')
            except NoSuchElementException:
                link = 'Ссылка отсутсвует'
           


            try:
                text = ad.find_element(By.XPATH, ".//div[@class='_7jyr _a25-']").text.strip() 
            except NoSuchElementException:
                text = 'Текст объявления отсутвует'
                if link == 'Ссылка отсутсвует':
                    text = 'Содержание объявления нарушает политику Фейсбук'

            if self.DEBUG:
                print(ad_id)
                print(status)
                print(date)
                print(platforms_list)
                print(payment)
                print(impressions)
                print(name_author)
                print(link)
                print(text)

            defaults = {
                'status': status,
                'date': date,
                'platforms': platforms_list,
                'audience_size': audience_size,
                'payment': payment,
                'impressions': impressions,
                'name_author': name_author,
                'link': link,
                'text': text,
            }

            # Создаем экземпляр модели Ad и сохраняем данные
            obj, created = Ad.objects.get_or_create(ad_id=ad_id, defaults=defaults)

            print(f'{date}, Обьект {ad_id} добавлен')


def main():
    parser = FacebookAdsParser()
    keywords = Keywords.objects.all()

    with parser.driver as driver:

        # get an ad type from database or apply default value
        try:
            ad_type_obj = AdTypeSettings.objects.get(active=True)
            ad_type = ad_type_obj.name
        except AdTypeSettings.DoesNotExist:
            ad_type = 'all'

        # get a country from database or apply default value
        try:
            country_obj = CountrySettings.objects.get(active=True)
            country_code = country_obj.name
        except CountrySettings.DoesNotExist:
            country_code = 'ALL'  # can be changed on current country the user is located
        
        for keyword in keywords:
            #go to the page, wait
            url = f'https://www.facebook.com/ads/library/?active_status=all&ad_type={ad_type}&country={country_code}&q={keyword.query}&search_type=keyword_unordered&media_type=all'
            driver.get(url)
            time.sleep(5)

            last_height = driver.execute_script('return document.body.scrollHeight')  #find default scrollheight

            parser.scrape_ads()

            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #scroll 
            time.sleep(5)

            new_height = driver.execute_script('return document.body.scrollHeight')  #find new scroll height

            while new_height > last_height:  # while default is not equal to new:       
                parser.scrape_ads()  #load data
                
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #scroll 
                time.sleep(5)

                last_height, new_height = new_height, driver.execute_script('return document.body.scrollHeight')  #  refresh values



if __name__ == '__main__':
    main()

