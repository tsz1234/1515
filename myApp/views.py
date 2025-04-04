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
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import pandas as pd
def screenData(request):
    if request.method == 'GET':
        arealist, followlist = getScreenData.getSquareData()
        pieList = getScreenData.getPieData()
        mapData = getScreenData.getmapData()
        LineRowData, LineColData = getScreenData.getLineData()
        circlieList = getScreenData.getCircleData()
        return JsonResponse({
            'arealist': arealist,
            'followlist': followlist,
            'pieList': pieList,
            'mapData': mapData,
            'LineRowData': LineRowData,
            'LineColData': LineColData,
            'circlieList': circlieList
        })

def summary(request):
    if request.method == 'GET':
        housesarea, housesmaker = GetSummaryData.getChangeList()
        defaultmaker = '不限'
        defaultarea = '不限'
        if request.GET.get('maker'):
            defaultmaker = request.GET.get('maker')
        if request.GET.get('area'):
            defaultarea = request.GET.get('area')
        housesData = GetSummaryData.getSummary(defaultmaker, defaultarea)
        return JsonResponse({
            'housesarea': housesarea,
            'housesmaker': housesmaker,
            'housesData': housesData,
        })

@csrf_exempt  # 临时禁用CSRF验证
def predict_price(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            area = data.get('area')
            decoration = data.get('decoration')
            input_area = float(data.get('inputArea', 0))
            floor = data.get('floor')  # 新增楼层输入
            year = data.get('year')  # 新增年份输入

            # 加载预处理对象和模型（确保路径正确）
            model_dir = settings.MODEL_ROOT
            le_floor = joblib.load(os.path.join(model_dir, 'le_floor.pkl'))
            le_year = joblib.load(os.path.join(model_dir, 'le_year.pkl'))  # 加载年份的 LabelEncoder
            encoder = joblib.load(os.path.join(model_dir, 'onehot_encoder.pkl'))
            scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
            model = joblib.load(os.path.join(model_dir, 'model_best.pkl'))

            # 转换和标准化数据
            floor_encoded = le_floor.transform([floor])[0]
            year_encoded = le_year.transform([year])[0]  # 对年份进行编码
            # 确保传入两个特征进行编码
            area_decoration_encoded = encoder.transform([[area, decoration]]).toarray()[0]
            area_scaled = scaler.transform([[input_area]])[0][0]

            # 构建特征向量
            features = np.concatenate([[floor_encoded, area_scaled, year_encoded], area_decoration_encoded])
            features = features.reshape(1, -1)

            # 调试信息：打印特征数量
            print(f"Number of features in prediction: {features.shape[1]}")

            # 检查特征数量是否匹配
            if features.shape[1] != model.n_features_in_:
                # 检查缺失的特征
                missing_features = model.n_features_in_ - features.shape[1]
                print(f"Missing {missing_features} features.")
                # 填充默认值
                default_features = np.zeros((1, missing_features))
                features = np.hstack((features, default_features))

            # 预测
            prediction = model.predict(features)
            return JsonResponse({'price': round(prediction[0], 2)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def get_options(request):
    if request.method == 'GET':
        # 获取唯一区域和装修列表
        regions = Products.objects.values_list('区域', flat=True).distinct()
        decorations = Products.objects.values_list('装修', flat=True).distinct()
        floors = Products.objects.values_list('楼层', flat=True).distinct()
        years = Products.objects.values_list('年份', flat=True).distinct()

        return JsonResponse({
            'housesregion': list(regions),
            'housesdecoration': list(decorations),
            'housesfloor': list(floors),
            'housesyear': list(years)
        })

from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from myApp.models import User
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return JsonResponse({
                    'code': 0,
                    'data': {
                        'userImg': 'https://avatars3.githubusercontent.com/u/22117876?s=460&v=4',
                        'userName': user.username,
                        'token': 'i_am_token'
                    }
                })
            else:
                return JsonResponse({
                    'code': 1,
                    'msg': '密码错误'
                })
        except User.DoesNotExist:
            return JsonResponse({
                'code': 1,
                'msg': '用户不存在'
            })
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import User

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({
                    'code': 1,
                    'msg': '用户名和密码不能为空'
                })
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'code': 1,
                    'msg': '用户名已存在'
                })
            hashed_password = make_password(password)
            print(f"Length of hashed password: {len(hashed_password)}")
            User.objects.create(username=username, password=hashed_password)
            return JsonResponse({
                'code': 0,
                'msg': '注册成功'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 1,
                'msg': '请求数据格式错误'
            })
# as415/myApp/views.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
import os
@csrf_exempt
def updateUserInfo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        otherInfo = request.POST.get('otherInfo')
        try:
            user = User.objects.get(username=username)
            # 这里可以将 otherInfo 保存到用户的其他字段中
            return JsonResponse({
                'code': 0,
                'msg': '资料保存成功'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'code': 1,
                'msg': '用户不存在'
            })
@csrf_exempt
def uploadAvatar(request):
    if request.method == 'POST':
        file = request.FILES.get('avatar')
        if file:
            # 保存文件到指定目录
            file_path = os.path.join('uploads', file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return JsonResponse({
                'code': 0,
                'data': {
                    'avatarUrl': file_path
                }
            })
        else:
            return JsonResponse({
                'code': 1,
                'msg': '未选择文件'
            })


logger = logging.getLogger(__name__)

@csrf_exempt
def changePassword(request):
    if request.method == 'POST':
        # 获取前端传来的旧密码和新密码
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')

        # 输入验证
        if not oldPassword or not newPassword:
            return JsonResponse({
                'code': 2,
                'msg': '旧密码和新密码不能为空'
            })

        # 密码强度验证（示例：新密码长度至少为 8 位）
        if len(newPassword) < 8:
            return JsonResponse({
                'code': 3,
                'msg': '新密码长度至少为 8 位'
            })

        try:
            # 假设用户已经登录，可以通过 request.user 获取当前用户
            user = request.user
            if check_password(oldPassword, user.password):
                # 验证旧密码正确，更新新密码
                user.password = make_password(newPassword)
                user.save()
                return JsonResponse({
                    'code': 0,
                    'msg': '密码修改成功'
                })
            else:
                # 旧密码错误
                return JsonResponse({
                    'code': 1,
                    'msg': '旧密码错误'
                })
        except Exception as e:
            # 记录异常信息
            logger.error(f"修改密码时出现错误: {e}")
            return JsonResponse({
                'code': 500,
                'msg': '服务器内部错误，请稍后再试'
            })