from myApp.models import *
from .getScreenData import *


def getChangeList():
    houses = list(getAllHuoses())
    housesarea = []
    housesmaker = []
    for i in houses:
        housesarea.append(i.区域)
        housesmaker.append(i.装修)
    housesarea = list(set(housesarea))
    housesmaker = list(set(housesmaker))
    return housesarea, housesmaker


def getSummary(defaultmaker, defaultarea):
    if defaultmaker == "不限" and defaultarea == "不限":
        houses = list(getAllHuoses())
    elif defaultarea == "不限":
        houses = Products.objects.filter(装修=defaultmaker)
    elif defaultmaker == "不限":
        houses = Products.objects.filter(区域=defaultarea)
    else:
        houses = Products.objects.filter(区域=defaultarea, 装修=defaultmaker)
    housesData = []
    for i in houses:
        housesData.append({
            'id': i.id,
            'title': i.标题,
            'totalprice': i.总价,
            'area': i.区域,
            'community': i.小区,
            'Acreage': i.面积,
            'high': i.楼层,
            'age': i.年份,
            'maker': i.装修
        })
    return housesData
