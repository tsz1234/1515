import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import csv
import time
import random
from sqlalchemy import create_engine
import re


def get_subdistrict_links():
    """获取每个行政区对应的各个子区域链接"""
    brower.get('https://cs.lianjia.com/ershoufang/')
    try:
        WebDriverWait(brower, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.position div[data-role="ershoufang"] a'))
        )
        links = []
        subdistrict_elements = brower.find_elements(By.CSS_SELECTOR, '.position div[data-role="ershoufang"] a')
        for element in subdistrict_elements:
            link = element.get_attribute('href')
            links.append(link)
        return links
    except Exception as e:
        print("获取子区域链接失败:", e)
        return []


def spider_fn(link):
    def init_csv():
        with open('lianjia.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['标题', '总价', '单价', '户型', '面积',
                             '朝向', '装修', '楼层', '年份', '结构', '小区', '区域', '关注量', '发布时间'])

    def search_product():
        brower.get(link)

    def parse_items():
        try:
            WebDriverWait(brower, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.sellListContent li'))
            )

            items = brower.find_elements(By.CSS_SELECTOR, '.sellListContent li[class*="clear"]')
            if not items:
                print("未找到房源数据，可能触发反爬！")
                return False

            for item in items:
                try:
                    data = extract_data(item)
                    save_to_csv(data)
                except Exception as e:
                    print(f"数据提取失败: {str(e)}")
                    continue
            return True
        except Exception as e:
            print("页面解析失败:", e)
            return False

    def extract_data(item):
        # 核心数据提取函数
        title = item.find_element(By.CSS_SELECTOR, '.title a').text.strip()
        total_price = item.find_element(By.CSS_SELECTOR, '.totalPrice').text.replace('万', '')
        unit_price = item.find_element(By.CSS_SELECTOR, '.unitPrice span').text.replace('单价', '')

        house_info = [i.strip() for i in item.find_element(By.CSS_SELECTOR, '.houseInfo').text.split('|')]
        position_info = [i.strip() for i in item.find_element(By.CSS_SELECTOR, '.positionInfo').text.split('-')]
        follow_info = item.find_element(By.CSS_SELECTOR, '.followInfo').text.split('/')
        year = ''
        if len(house_info) > 5:
            year_match = re.search(r'\d+', house_info[5])
            year = year_match.group() if year_match and '年' in house_info[5] else '暂无数据'

        # 结构处理逻辑
        structure = ''
        if len(house_info) > 5:
            if re.search(r'\d+年', house_info[5]):
                structure = house_info[6] if len(house_info) > 6 else '暂无数据'
            else:
                structure = house_info[5] if any(kw in house_info[5] for kw in ['板楼', '塔楼', '结合']) else '暂无数据'

        floor = house_info[4] if len(house_info) > 4 else '暂无数据'

        return {
            '标题': title,
            '总价': total_price,
            '单价': unit_price,
            '户型': house_info[0],
            '面积': house_info[1].replace('平米', ''),
            '朝向': house_info[2],
            '装修': house_info[3] if len(house_info) > 3 else '',
            '楼层': floor,
            '年份': year,
            '结构': structure,
            '小区': position_info[0],
            '区域': position_info[1] if len(position_info) > 1 else '',
            '关注量': follow_info[0].replace('人关注', ''),
            '发布时间': follow_info[-1].strip()
        }

    def save_to_csv(data):
        with open('lianjia.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(data.values())

    def handle_pagination():
        max_page = 100  # 最大抓取页数
        current_page = 1

        while current_page <= max_page:
            print(f"正在抓取第 {current_page} 页...")
            url = link.replace('/ershoufang/', f'/ershoufang/pg{current_page}/')

            # 页面加载重试机制
            retry_count = 0
            while retry_count < 3:
                try:
                    brower.get(url)
                    # 等待关键元素加载
                    WebDriverWait(brower, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.sellListContent li'))
                    )
                    # 验证是否为空页面
                    if not brower.find_elements(By.CSS_SELECTOR, '.sellListContent li'):
                        print("到达最后一页，终止抓取")
                        return
                    break
                except Exception as e:
                    retry_count += 1
                    print(f"页面加载失败，第{retry_count}次重试: {str(e)}")
                    time.sleep(2)
            else:
                print("连续3次加载失败，终止抓取")
                return

            # 解析数据
            if not parse_items():
                print("数据解析失败，终止抓取")
                return

            # 智能页数限制（检测实际页码）
            try:
                actual_page = int(brower.find_element(By.CSS_SELECTOR, 'a[class*="selected"]').text)
                if actual_page != current_page:
                    print(f"页码不匹配，预期{current_page}，实际{actual_page}，终止抓取")
                    return
            except:
                pass

            # 随机延迟（3-8秒）
            time.sleep(random.randint(3, 8))
            current_page += 1

    def main():
        init_csv()
        search_product()
        handle_pagination()
        save_to_sql()

    def save_to_sql():
        products = pd.read_csv('./lianjia.csv')
        df = pd.DataFrame(products)
        # 检查并填充缺失值
        df['楼层'] = df['楼层'].fillna('暂无数据')
        conn = create_engine('mysql+pymysql://root:2003@localhost:3306/ershoufangdata?charset=utf8')
        df.to_sql('houses', conn, index=False, if_exists='append')
        print('导入数据成功')

    main()


if __name__ == '__main__':
    # 浏览器配置（兼容最新Chrome驱动）
    options = webdriver.ChromeOptions()

    # 基础反爬参数
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")

    # 调试模式配置（需先手动启动带调试端口的Chrome）
    # chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\ChromeProfile"

    # 无头模式配置（如需启用请取消注释）
    # options.add_argument("--headless=new")
    # options.add_argument("--window-size=1920,1080")

    # 驱动服务配置
    service = Service(executable_path='./chromedriver.exe')
    brower = webdriver.Chrome(service=service, options=options)

    # 高级反爬策略
    brower.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
            configurable: true
        });
        '''
    })
    try:
        subdistrict_links = get_subdistrict_links()
        for link in subdistrict_links:
            spider_fn(link)
    finally:
        brower.quit()