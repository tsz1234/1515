from collections import defaultdict

from myApp.utils.GetBaseData import *


def getSquareData():
    houses = list(getAllHuoses())

    # 使用 defaultdict 自动初始化装修类型
    housesVolumn = defaultdict(int)

    for i in houses:
        # 直接累加关注量（自动处理首次出现的装修类型）
        housesVolumn[i.装修] += int(i.关注量)

    # 按关注量降序排序
    sorted_items = sorted(housesVolumn.items(), key=lambda x: x[1], reverse=True)

    # 获取前7个装修类型及其关注量
    top_items = sorted_items[:7]

    # 拆分为两个列表
    arealist = [item[0] for item in top_items]
    followlist = [item[1] for item in top_items]

    return arealist, followlist


def getPieData():
    houses = list(getAllHuoses())
    housestype = {}
    for i in houses:
        if housestype.get(i.结构, -1) == -1:
            housestype[i.结构] = 1
        else:
            housestype[i.结构] += 1
    pieList = []
    for k, v in housestype.items():
        pieList.append({
            'name': k,
            'value': v
        })
    return pieList


def getmapData():
    houses = list(getAllHuoses())
    houseseara = {}
    for i in houses:
        if houseseara.get(i.区域, -1) == -1:
            houseseara[i.区域] = 1
        else:
            houseseara[i.区域] += 1
    original_data = []
    for k, v in houseseara.items():
        original_data.append({
            'name': k,
            'value': v
        })
    lists = {
        '雨花区': ['赤岗冲', '德思勤东塘', '高桥', '桂花村', '侯家塘', '黄土岭', '井湾子', '金盆岭', '暮云', '尚东',
                   '韶山南路', '树木岭', '跳马铁道学院', '万家丽南路', '武广新城', '喜盈门', '窑岭雨花亭', '左家塘'],
        '岳麓区': ['滨江新城', '东方红', '枫林三路', '观沙岭', '含浦', '河西步步高', '河西大学城', '河西人人乐',
                   '金星北', '金星中路', '雷锋大道', '雷锋镇', '麓谷东', '麓谷西', '梅溪湖北岸', '梅溪湖南岸',
                   '汽车西站', '溁湾镇', '商学院', '市政府', '桐梓坡', '王家湾', '阳光100', '洋湖垸', '银盆岭',
                   '岳麓其他', '岳麓山北'],
        '天心区': ['德思勤', '东塘', '侯家塘', '黄土岭', '金盆岭', '暮云', '南郊公园', '汽车南站', '省政府', '书院路',
                   '跳马', '铁道学院', '五一广场', '湘府路', '新开铺'],
        '开福区': ['北辰三角洲', '福元西路', '广电', '金霞', '开福其他', '开福区政府', '烈士公园', '青竹湖', '市一中',
                   '四方坪', '松桂园', '伍家岭', '湘江世纪城', '月湖', '中南汽车世界'],
        '芙蓉区': ['德政园', '芙蓉区政府', '火车站', '浏城桥', '马王堆', '汽车东站', '尚东', '松桂园', '晚报'],
        '望城区': ['金星北', '青竹湖', '望城区'],
        '长沙县': ['长沙县', '金霞', '开元路', '汽车东站', '泉塘', '松雅湖', '万家丽北', '万家丽南路', '星沙其他',
                   '月湖'],
    }

    # 步骤1：构建元素→列表名的映射字典
    element_to_listname = {}
    for list_name, elements in lists.items():
        for element in elements:
            element_to_listname[element] = list_name  # 直接使用字符串作为键，而非tuple

    # 步骤2：更新原始字典中的name
    updated_data = []
    for item in original_data:
        original_name = item['name']
        if original_name in element_to_listname:
            new_name = element_to_listname[original_name]
            updated_data.append({'name': new_name, 'value': item['value']})
        else:
            updated_data.append(item)  # 未匹配则保留原name

    # 步骤3：合并同名项并累加value
    merged_dict = defaultdict(int)
    for item in updated_data:
        merged_dict[item['name']] += item['value']

    # 转换为最终结果格式
    mapData = [{'name': k, 'value': v} for k, v in merged_dict.items()]
    return mapData


def getLineData():
    houses = list(getAllHuoses())
    priceDict = {'0-10': 0, '10-50': 0, '50-100': 0, '100-200': 0, '200-300': 0, '300万以上': 0, }
    for i in houses:
        p = float(i.总价)
        if p < 10:
            priceDict['0-10'] += 1
        elif 10 <= p < 50:  # 10 ≤ p < 50
            priceDict['10-50'] += 1
        elif 50 <= p < 100:  # 50 ≤ p < 100
            priceDict['50-100'] += 1
        elif 100 <= p < 200:  # 100 ≤ p < 200
            priceDict['100-200'] += 1
        elif 200 <= p < 300:  # 200 ≤ p < 300
            priceDict['200-300'] += 1
        else:
            priceDict['300万以上'] += 1
    LineRowData = list(priceDict.keys())
    LineColData = list(priceDict.values())
    return LineRowData, LineColData


def getCircleData():
    houses = list(getAllHuoses())
    sumDict = {}
    sumPrice = 0.0  # 明确浮点类型

    # 第一阶段：累加总价
    for i in houses:
        try:
            p = float(i.总价)
        except ValueError:
            continue  # 跳过无效数据

        sumPrice += p
        region = i.户型.strip()  # 清理区域名称

        # 使用更安全的字典累加方式
        sumDict[region] = sumDict.get(region, 0.0) + p

    # 处理空数据情况
    if not sumDict or sumPrice <= 0:
        return []

    # 第二阶段：计算百分比
    circleList = []
    for key, value in sumDict.items():
        try:
            percentage = round(value / sumPrice * 100, 2)  # 保留两位小数
        except ZeroDivisionError:
            percentage = 0.0

        circleList.append({
            'name': key,
            'value': percentage  # 直接保留浮点数
        })

    return circleList
