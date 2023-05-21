from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import json



# スクレイピングを行う関数
def Get_elements(df, col):
  soup = BeautifulSoup(open('./sauna_in_japan/page1.html', encoding='utf-8'), 'html.parser')
  last_page = soup.find_all(class_='c-pagenation_link')
  last_page = last_page[-1].find('a').text
  last_page = int(last_page) # 最終のページ数を格納
  
  for page in range(1, last_page+1):
    soup = BeautifulSoup(open('./sauna_in_japan/page{}.html'.format(page), encoding='utf-8'), 'html.parser')
    # 各要素を取得
    name_list = [
        name.find('h3').text.replace('\n            ', '').replace('\n          ', '') 
        for name in soup.find_all(class_="p-saunaItemName")
    ]
    man_list = soup.find_all(class_=["p-saunaItemSpec_content p-saunaItemSpec_content--man", "p-saunaItemSpec_content p-saunaItemSpec_content--unisex"])
    sauna_list = [
        sauna.find(class_='p-saunaItemSpec_item p-saunaItemSpec_item--sauna')\
            .find(class_='p-saunaItemSpec_value').text.replace(' ℃', '').replace('\n                   ', '').replace('\n', '') for sauna in man_list
    ]
    mizuburo_list = [
        mizuburo.find(class_='p-saunaItemSpec_item p-saunaItemSpec_item--mizuburo')\
            .find(class_='p-saunaItemSpec_value').text.replace(' ℃', '').replace('\n                   ', '').replace('\n', '') for mizuburo in man_list
    ]
    gaikiyoku_list = [
        gaikiyoku.find(class_='p-saunaItemSpec_item p-saunaItemSpec_item--gaikiyoku')\
            .find(class_='p-saunaItemSpec_value').find('img').get('alt') for gaikiyoku in man_list
    ]
    for i, gaikiyoku in enumerate(gaikiyoku_list):
        if gaikiyoku =='有り':
            gaikiyoku_list[i] = 1
        elif gaikiyoku == '無し':
            gaikiyoku_list[i] = 0

    loyly_list = [
        loyly.find(class_='p-saunaItemSpec_item p-saunaItemSpec_item--loyly')\
            .find(class_='p-saunaItemSpec_value').find('img').get('alt') for loyly in man_list
    ]
    for i, loyly in enumerate(loyly_list):
        if loyly =='有り':
            loyly_list[i] = 1
        else:
            loyly_list[i] = 0
    price_list = [
        price.text.replace('\n                                            ', '').replace('円〜                ', '')
        for price in soup.find_all(class_='p-saunaItem_information is-price')
    ]
    sakatsu_list = [
        sakatsu.text.replace('サ活', '').replace('\n            \n                                          ','')\
            .replace('\n                                      \n', '') for sakatsu in soup.find_all(class_='p-saunaItem_action')[1::2]
    ]
    location_list = [
        location.text.split('-')[1].split('\xa0')[0]
        for location in soup.find_all(class_="p-saunaItem_address")
    ]
    location_list = [location.replace('\n    ', '') for location in location_list]

    count = len(name_list) # そのページのサウナ件数
    df_unit = pd.DataFrame(columns=col) # ページごとの仮のDataframe

    # 空のリストに、整形したデータを格納
    for i in range(count):
        row = []
        row.append(name_list[i])
        row.append(sauna_list[i])
        row.append(mizuburo_list[i])
        row.append(gaikiyoku_list[i])
        row.append(loyly_list[i])
        row.append(price_list[i])
        row.append(sakatsu_list[i])
        row.append(location_list[i])

        df_unit.loc[i] = row

    df = pd.concat([df, df_unit], ignore_index=True) # 1ページごとに元のDataframeに追加  
          
  return df


# 検収条件を確認・記録する関数
def Inspection(df):
  soup = BeautifulSoup(open('./sauna_in_japan/page1.html', encoding='utf-8'), 'html.parser') # 1ページ目を取得
  hit_sum = soup.find(class_='p-result_number').find('span').text # ヒット件数の部分を取得
  with open('./csv/acceptance_conditions.csv', 'a', encoding='shift_jis', errors='ignore') as file:
    file.write('\n' + str(hit_sum) + ', ' + str(len(df))) # サイト側のヒット件数と、実際の取得件数を記録
  # JSONをファイルに書き込み
  if os.path.exists('./js/var.js'):
    os.remove('./js/var.js')
  with open('./js/var.js', 'w', encoding='shift_jis') as f:
    f.write(f'var hit_sum = {str(hit_sum)};')


# メイン関数
def Main():
  print('start scraping!\n')
  program_time = time.time()

  col = ['名称', 'サウナ温度', '水風呂温度', '外気浴', 'ロウリュ', '料金', 'サ活', '県名'] 
  data = pd.DataFrame(columns=col) # 取得データを格納するDataframeを作成
  data = Get_elements(data, col) # スクレイピングの関数を実行
  data = data.replace({1: "◯", 0: "×", "": "-",}) # 値が1の部分を"○"に、0の部分を"x"に変換

  if os.path.exists('./csv/acceptance_conditions.csv'):
    os.remove('./csv/acceptance_conditions.csv')
  with open('./csv/acceptance_conditions.csv', 'a', encoding='shift_jis', errors='ignore') as file:
    file.write('検索ヒット件数, データ取得件数') # 検収条件を記録するファイルを作成

  Inspection(data) # 検収条件の関数を実行

  # データをjsに
  data_json = data.to_json(orient='records')
  if os.path.exists('./js/data.js'):
    os.remove('./js/data.js')
  with open('./js/data.js', 'w', encoding='shift_jis') as f:
    f.write(f'var data = {data_json};')

  # データをcsvに
  if os.path.exists('./csv/master_data.csv'):
    os.remove('./csv/master_data.csv')
  with open('./csv/master_data.csv', 'a', encoding='shift_jis', errors='ignore') as f:
    data.to_csv(f, index=False)

  program_time = time.time() - program_time
  print('completed!\nelapsed_time:{}'.format(program_time) + '[sec]\n')


# 以下実行コード
if __name__ == "__main__":
  Main()