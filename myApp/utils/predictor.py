# myApp/utils/train_model.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from django.conf import settings
from myApp.models import *
from myApp.utils.GetBaseData import getAllHuoses


def train_model():
    houses = list(getAllHuoses())
    valid_houses = [
        i for i in houses
        if i.单价 and i.单价.strip() != ''  # 确保单价非空
           and i.面积 and i.面积.strip() != ''  # 确保面积非空
           and i.区域 and i.区域.strip() != ''  # 确保区域非空
           and i.装修 and i.装修.strip() != ''  # 确保装修非空
    ]
    # 构建包含区域特征的DataFrame
    df = pd.DataFrame([{
        '区域': i.区域,
        '面积': float(i.面积),
        '装修': i.装修,
        '单价': float(i.单价.replace(',', '').replace('元/平', ''))
    } for i in valid_houses])

    # 特征工程
    le_region = LabelEncoder()
    le_decoration = LabelEncoder()
    df['区域编码'] = le_region.fit_transform(df['区域'])
    df['装修编码'] = le_decoration.fit_transform(df['装修'])

    # 数值标准化
    scaler = StandardScaler()
    df['面积标准化'] = scaler.fit_transform(df[['面积']])

    # 保存预处理对象
    save_dir = settings.MODEL_ROOT
    os.makedirs(save_dir, exist_ok=True)
    joblib.dump(le_region, os.path.join(save_dir, 'le_region.pkl'))
    joblib.dump(le_decoration, os.path.join(save_dir, 'le_decoration.pkl'))
    joblib.dump(scaler, os.path.join(save_dir, 'scaler.pkl'))

    # 训练模型
    X = df[['区域编码', '装修编码', '面积标准化']]
    y = df['单价']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, os.path.join(save_dir, 'model.pkl'))


def get_options():
    houses = list(getAllHuoses())
    regions = sorted(list(set(i.区域 for i in houses)))
    decorations = sorted(list(set(i.装修 for i in houses)))
    return regions, decorations