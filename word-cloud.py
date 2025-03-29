import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from pymysql import connect

def get_img(field, target_img_src, res_img_src):
    conn = connect(host="localhost", user="root", passwd="2003", database="ershoufangdata", charset="utf8")
    cursor = conn.cursor()

    sql = f"SELECT `{field}` FROM houses"
    cursor.execute(sql)
    data = cursor.fetchall()

    # 修改后的核心代码
    text = ' '.join([str(row[0]).strip() for row in data if row[0] and str(row[0]).strip() != ''])

    data_cut = jieba.cut(text, cut_all=False, HMM=True)
    string = ' '.join(data_cut)

    img = Image.open(target_img_src)
    img_arr = np.array(img)
    wc = WordCloud(
        font_path='STHUPO.TTF',
        mask=img_arr,
        background_color='white',
        max_words=200,
        collocations=False
    )
    wc.generate(string)

    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(res_img_src, dpi=800, bbox_inches='tight')
    plt.close()

    cursor.close()
    conn.close()

# 调用示例
get_img('区域', './vue-admin-template-master/src/assets/imgs/12.png',
        './vue-admin-template-master/src/assets/imgs/gas.jpg')