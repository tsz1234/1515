from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os
from django.conf import settings
from myApp.models import *
from myApp.utils.GetBaseData import getAllHuoses
import pandas as pd

def train_model():
    houses = list(getAllHuoses())
    valid_houses = [
        i for i in houses
        if i.单价 and i.单价.strip() != ''
           and i.面积 and i.面积.strip() != ''
           and i.区域 and i.区域.strip() != ''
           and i.装修 and i.装修.strip() != ''
           and i.楼层 and i.楼层.strip() != ''
           and i.年份 and i.年份.strip() != ''
    ]
    # 构建包含区域特征的 DataFrame
    df = pd.DataFrame([{
        '区域': i.区域,
        '面积': float(i.面积),
        '装修': i.装修,
        '单价': float(i.单价.replace(',', '').replace('元/平', '')),
        '楼层': i.楼层,
        '年份': i.年份
    } for i in valid_houses])


    encoder = OneHotEncoder()
    categorical_features = df[['区域', '装修']]
    encoded_features = encoder.fit_transform(categorical_features)
    feature_names = encoder.get_feature_names_out(categorical_features.columns)
    encoded_df = pd.DataFrame(encoded_features.toarray(), columns=feature_names)

    le_floor = LabelEncoder()
    df['楼层编码'] = le_floor.fit_transform(df['楼层'])

    le_year = LabelEncoder()
    df['年份编码'] = le_year.fit_transform(df['年份'])

    df = pd.concat([df.reset_index(drop=True), encoded_df], axis=1)

    scaler = StandardScaler()
    df['面积标准化'] = scaler.fit_transform(df[['面积']])

    save_dir = settings.MODEL_ROOT
    os.makedirs(save_dir, exist_ok=True)
    joblib.dump(encoder, os.path.join(save_dir, 'onehot_encoder.pkl'))
    joblib.dump(scaler, os.path.join(save_dir, 'scaler.pkl'))
    joblib.dump(le_floor, os.path.join(save_dir, 'le_floor.pkl'))
    joblib.dump(le_year, os.path.join(save_dir, 'le_year.pkl'))

    X = df.drop(['区域', '装修', '单价', '楼层', '年份'], axis=1)
    y = df['单价']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, os.path.join(save_dir, 'model_best.pkl'))

def get_options():
    houses = list(getAllHuoses())
    regions = sorted(list(set(i.区域 for i in houses)))
    decorations = sorted(list(set(i.装修 for i in houses)))
    return regions, decorations