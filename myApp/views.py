from django.shortcuts import render
from django.http import JsonResponse
import joblib
import numpy as np
from .models import Products
# Create your views here.
from .utils import getScreenData, predictor
from collections import defaultdict
from .utils import GetSummaryData
import os
from django.conf import settings
def screenData(request):
    if request.method == 'GET':
        arealist, followlist = getScreenData.getSquareData()
        pieList = getScreenData.getPieData()
        mapData = getScreenData.getmapData()
        LineRowData, LineColData = getScreenData.getLineData()
        circlieList=getScreenData.getCircleData()
        return JsonResponse({
            'arealist': arealist,
            'followlist': followlist,
            'pieList': pieList,
            'mapData': mapData,
            'LineRowData': LineRowData,
            'LineColData': LineColData,
            'circlieList':circlieList
        })
def summary(request):
    if request.method == 'GET':
        housesarea, housesmaker=GetSummaryData.getChangeList()
        defaultmaker='不限'
        defaultarea='不限'
        if request.GET.get('maker'):defaultmaker=request.GET.get('maker')
        if request.GET.get('area'):defaultarea=request.GET.get('area')
        housesData=GetSummaryData.getSummary(defaultmaker, defaultarea)
        return JsonResponse({
            'housesarea': housesarea,
            'housesmaker': housesmaker,
            'housesData': housesData,
        })


#
# 修改后的预测视图(添加调试日志)
# 在文档1的视图中添加
from django.views.decorators.csrf import csrf_exempt
import logging
import json

@csrf_exempt  # 临时禁用CSRF验证
def predict_price(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            area = data.get('area')
            decoration = data.get('decoration')
            input_area = float(data.get('inputArea', 0))

            # 加载预处理对象和模型（确保路径正确）
            model_dir = settings.MODEL_ROOT
            le_region = joblib.load(os.path.join(model_dir, 'le_region.pkl'))
            le_decoration = joblib.load(os.path.join(model_dir, 'le_decoration.pkl'))
            scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
            model = joblib.load(os.path.join(model_dir, 'model.pkl'))
            # 转换和标准化数据
            area_encoded = le_region.transform([area])[0]
            decoration_encoded = le_decoration.transform([decoration])[0]
            area_scaled = scaler.transform([[input_area]])[0][0]

            # 预测
            features = np.array([[area_encoded, decoration_encoded, area_scaled]])
            prediction = model.predict(features)
            return JsonResponse({'price': round(prediction[0], 2)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_options(request):
    if request.method == 'GET':
        # 获取唯一区域和装修列表
        regions = Products.objects.values_list('区域', flat=True).distinct()
        decorations = Products.objects.values_list('装修', flat=True).distinct()

        return JsonResponse({
            'housesregion': list(regions),
            'housesdecoration': list(decorations)
        })