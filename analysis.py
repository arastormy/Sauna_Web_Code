from datetime import date
import numpy as np
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import json
import japanize_matplotlib

# # 数字以外の値が含まれているかを確認する
# for column in df2.columns:
#     non_numeric_values = df2.loc[~df2[column].astype(str).str.isdigit(), column].unique()
#     if len(non_numeric_values) > 0:
#         print("列:", column)
#         print("非数字の値:", non_numeric_values)
#         print()

# サ活のグラフを描画する関数
def plot_sakatsu_histogram(data, range_list, save_path):
    fig, axes = plt.subplots(1, len(range_list), figsize=(15, 5))

    for i, (start, end) in enumerate(range_list):
        axes[i].hist(data, bins=10, range=(start, end), edgecolor='k', color=(18/255, 77/255, 255/255))
        axes[i].set_xlabel('サ活', fontname='Hiragino Maru Gothic Pro', fontsize=16)
        axes[i].set_ylabel('度数', fontname='Hiragino Maru Gothic Pro', fontsize=16)

    fig.tight_layout()

    if os.path.exists(save_path):
        os.remove(save_path)
    plt.savefig(save_path)

    plt.clf()


# 散布図を描画する関数
def plot_scatter_plots(data, columns, x_value, save_path):
    fig, axes = plt.subplots(1, len(columns), figsize=(15, 5))

    for i, column in enumerate(columns):
        axes[i].scatter(data['サ活'], data[column], color=(18/255, 77/255, 255/255))
        axes[i].set_xlabel('サ活', fontname='Hiragino Maru Gothic Pro', fontsize=16)
        axes[i].set_ylabel(columns[i], fontname='Hiragino Maru Gothic Pro', fontsize=16)

        # x_valueの赤い破線を追加
        axes[i].axvline(x=x_value, color='r', linestyle='--')

    fig.tight_layout()

    if os.path.exists(save_path):
        os.remove(save_path)
    plt.savefig(save_path)

    plt.clf()


# ヒストグラムを作成し、分析結果を取得する関数
def plot_histograms_and_get_results(data, columns, top_n, save_path, results):
    fig, axes = plt.subplots(1, len(columns), figsize=(15, 5))

    top_bins = []  # 上位の bin の値を格納するリスト

    for i, column in enumerate(columns):
        values, bins, _ = axes[i].hist(data[column], bins=10, edgecolor='k', color=(18/255, 77/255, 255/255))
        axes[i].set_xlabel(columns[i], fontname='Hiragino Maru Gothic Pro', fontsize=16)
        axes[i].set_ylabel('度数', fontname='Hiragino Maru Gothic Pro', fontsize=16)

        # 上位の bin の値を抽出
        top_indices = values.argsort()[-top_n:][::-1]
        top_bins.append(bins[top_indices])

        # 結果を格納
        column_names = ['sauna', 'mizuburo', 'price']  # カラム名のリスト
        column_name = column_names[i]
        results[column_name] = {
            'min': np.min(top_bins[-1]),
            'max': np.max(top_bins[-1])
        }

    fig.tight_layout()

    if os.path.exists(save_path):
        os.remove(save_path)
    plt.savefig(save_path)

    plt.clf()


# 棒グラフと箱ひげ図を作成し、分析結果を取得する関数
def plot_bar_and_box_plots(data, save_path, results, top_n=2):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # figsizeを調整

    # 度数が0でない要素のみを抽出
    df3 = data['県名'].value_counts()
    df3 = df3[df3 > 0]

    # 県名の棒グラフ
    axes[0].bar(df3.index, df3.values, align='center', color=(18/255, 77/255, 255/255), edgecolor='k')
    axes[0].set_xlabel('県名', fontname='Hiragino Maru Gothic Pro', fontsize=19)
    axes[0].set_ylabel('度数', fontname='Hiragino Maru Gothic Pro', fontsize=19)
    axes[0].set_xticks(np.arange(len(df3.index)))  # x軸の目盛りを設定
    axes[0].set_xticklabels(df3.index, rotation='vertical', fontsize=14)  # x軸のラベルを縦書きにする

    top_prefectures = df3.nlargest(top_n).index.tolist()
    results['location'] = top_prefectures

    # 外気浴の箱ひげ図
    data.plot.box(ax=axes[1], vert=False, column='サ活', by='外気浴', sym='', color=(18/255, 77/255, 255/255))
    axes[1].set_xlabel('外気浴', fontname='Hiragino Maru Gothic Pro', fontsize=19)

    # ロウリュの箱ひげ図
    data.plot.box(ax=axes[2], vert=False, column='サ活', by='ロウリュ', sym='', color=(18/255, 77/255, 255/255))
    axes[2].set_xlabel('ロウリュ', fontname='Hiragino Maru Gothic Pro', fontsize=19)

    results['gaikiyoku'] = '◯'
    results['louly'] = '◯'

    # グラフのレイアウトを調整
    fig.tight_layout()

    # ファイル保存
    if os.path.exists(save_path):
        os.remove(save_path)
    plt.savefig(save_path)

    plt.clf()


# 取得した分析結果を整形する関数
def process_results(results, columns):
    for column in columns:
        results[column]['min'] = int(results[column]['min'])
        results[column]['max'] = int(results[column]['max'])

    results['price']['min'] = int(round(results['price']['min'], -2))
    results['price']['max'] = int(round(results['price']['max'], -2))

# メイン関数
def Main():
    print('start analysis!\n')
    program_time = time.time()

    #　分析に使用するハイパーパラメータ
    threshold = 10000
    hist_top = 4
    bar_top = 2

    # CSVを読み込む
    df = pd.read_csv('./csv/master_data.csv', encoding='shift_jis')

    # 分析結果を格納する辞書を定義
    results = {}
    results['current_date'] = date.today().strftime("%Y/%m/%d") # 分析を行った日付
    results['hit_sum'] = len(df) # 取得したデータ数
    results['threshold'] = threshold

    # 欠損値除外処理
    df2 = df.replace(['', '-', '\n                    -\n                                    '], np.nan).copy()  # 欠損値をNaNに変換
    df2['サウナ温度'] = df2['サウナ温度'].str.strip().astype(float)  # サウナ温度の列から空白を削除して数値データに変換
    df2['水風呂温度'] = df2['水風呂温度'].str.strip().astype(float)  # 水風呂温度の列から空白を削除して数値データに変換
    df2 = df2.dropna()  # NaNを削除

    # Pandasの型変換
    df2 = df2.astype({'サウナ温度': 'float', '水風呂温度': 'float', '外気浴': 'object', 'ロウリュ': 'object', '料金': 'int', 'サ活': 'int'})

    results['rawdata'] = len(df2) # 分析に使用するデータ数

    # サ活のヒストグラム作成
    save_path = './image/hist_sakatsu.png'
    plot_sakatsu_histogram(df2['サ活'], [(0, 1000), (1000, 10000), (10000, 30000)], save_path)

    # 散布図作成
    columns = ['サウナ温度', '水風呂温度', '料金']
    save_path = './image/scatter_plots.png'
    plot_scatter_plots(df2, columns, threshold, save_path)

    # サ活が5000以上のデータのみ抽出
    df2 = df2[df2['サ活'] >= threshold]

    # サ活が5000以上のヒストグラム
    columns = ['サウナ温度', '水風呂温度', '料金']
    save_path = './image/hist_all.png'
    plot_histograms_and_get_results(df2, columns, hist_top, save_path, results)

    # サ活が5000以上の棒グラフとヒストグラム
    save_path = './image/hist_box.png'
    plot_bar_and_box_plots(df2, save_path, results, bar_top)

    # 分析結果を整形
    columns = ['sauna', 'mizuburo', 'price']
    process_results(results, columns)

    print(f'results = {results}')

    # 分析結果をjsonに変換してファイルに書き込み
    json_data = json.dumps(results)

    if os.path.exists('./js/var.js'):
        os.remove('./js/var.js')
    with open('./js/var.js', 'w') as file:
        file.write(f'var results = {json_data};')

    program_time = time.time() - program_time
    print('completed!\nelapsed_time:{}'.format(program_time) + '[sec]')

# 以下実行コード
if __name__ == "__main__":
    Main()