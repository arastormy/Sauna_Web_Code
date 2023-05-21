# coding: utf-8

from bs4 import BeautifulSoup
import requests
import time
import shutil
import os
import datetime

# urlを取得する関数
def Get_html(url, retry_times): 
    time.sleep(2.0)
    errs = [500, 502, 503]
    for t in range(retry_times + 1):
        r = requests.get(url)
        if t < retry_times:
            if r.status_code in errs:
                continue
        r.raise_for_status()
        return r


# サウナ一覧のurlを取得する関数
def Sauna_html(target_url, key, now_page, last_page):
    r = Get_html(target_url.format(now_page), 3) # htmlを取得

    with open('./{}/page{}.html'.format(key, now_page), 'w', encoding='utf_8') as file:
        file.write(r.text)
    
    if now_page != last_page:
        return now_page + 1
    else:
        with open('./csv/information_data.csv', 'a', encoding='utf_8') as file:
            file.write('\n' + str(key) + 'の取得サウナ一覧ページ数, ' + str(now_page)) # 合計取得ページを記録
        return 0


def Main():
    print('start crawling!\n')
    program_time = time.time()

    dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) # 日本の時刻に合わせる
    if os.path.exists('./csv/information_data.csv'):
      os.remove('./csv/information_data.csv')
    with open('./csv/information_data.csv', 'a', encoding='utf_8') as file: # csvを作成
        file.write(str(dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')) + ' 時点　取得開始, ページ数') # 取得開始日時を記録
    del dt_now

    urls = {
        'sauna_in_japan': 'https://sauna-ikitai.com/search?ordering=post_counts_desc&target_gender%5B%5D=male&page={}',
    } # ジャンルとurlの辞書を作成
       
    for key, url in urls.items():

        folder_name = './{}'.format(key)

        # フォルダが存在する場合は削除
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
        # フォルダを作成
        os.makedirs(folder_name)
        
        r = Get_html(url.format(1), 3)
        soup = BeautifulSoup(r.text, 'html.parser')
        last_page = soup.find_all(class_='c-pagenation_link')
        last_page = last_page[-1].find('a').text
        last_page = int(last_page)
        print(f'Get data to page {last_page} of {key}\n')
        
        page = 1
        while True:
            page = Sauna_html(url, key, page, last_page) # 店舗一覧のurl,　ジャンル, ページ数　
            if page == 0: # 最後のページなら
                break
    program_time = time.time() - program_time
    print('completed!\nelapsed_time:{}'.format(program_time) + '[sec]\n')            


if __name__ == "__main__":
    Main()