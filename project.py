#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql, urllib.request, csv, re, datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dateutil.relativedelta import relativedelta

#基隆市KEL Keelung
KEL_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%9F%BA%E9%9A%86%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#新北市NTPC New_Taipei
NTPC_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E6%96%B0%E5%8C%97%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#台北市TPE Taipei
TPE_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%8F%B0%E5%8C%97%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#桃園市TYN Taoyuan
TYN_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E6%A1%83%E5%9C%92%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#新竹縣HSZ0 Hsinchu_County
HSZ0_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E6%96%B0%E7%AB%B9%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#新竹市HSZ1 Hsinchu_City
HSZ1_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E6%96%B0%E7%AB%B9%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#苗栗縣ZMI Miaoli
ZMI_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E8%8B%97%E6%A0%97%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#台中市TXG Taichung
TXG_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%8F%B0%E4%B8%AD%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#彰化縣CHW Changhua
CHW_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%BD%B0%E5%8C%96%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#南投縣NTC Nantou
NTC_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%8D%97%E6%8A%95%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#雲林縣YUN Yunlin
YUN_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E9%9B%B2%E6%9E%97%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#嘉義縣CYI0 Chiayi_County
CYI0_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%98%89%E7%BE%A9%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#嘉義市CYI1 Chiayi_City
CYI1_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%98%89%E7%BE%A9%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#台南市TNN Tainan
TNN_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%8F%B0%E5%8D%97%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#高雄市KHH Kaohsiung
KHH_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E9%AB%98%E9%9B%84%E5%B8%82%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#屏東縣PIF Pingtung
PIF_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%B1%8F%E6%9D%B1%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#宜蘭縣ILA Yilan
ILA_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%AE%9C%E8%98%AD%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#花蓮縣HUN Hualien
HUN_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E8%8A%B1%E8%93%AE%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#台東縣TTT Taitung
TTT_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E5%8F%B0%E6%9D%B1%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#澎湖縣PEH Penghu
PEH_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E6%BE%8E%E6%B9%96%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#金門縣KNH Kinmen
KNH_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E9%87%91%E9%96%80%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"
#連江縣LNN Lienchiang
LNN_url = "https://raw.githubusercontent.com/lintao89/project_data/main/%E9%80%A3%E6%B1%9F%E7%B8%A3%E6%AF%8F%E6%97%A5%E7%A2%BA%E8%A8%BA%E6%95%B8.csv"

def create():
    conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = '20010303',
        database = '2'
    )
    cursor = conn.cursor()
    
    #台中市TXG Taichung
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Taichung (個案研判日 Date NULL, 縣市 VARCHAR(255) NULL, 確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Taichung;')
    sql_insert = '''insert into Taichung value(%s, %s, %s);'''

    with urllib.request.urlopen(TXG_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()

    #基隆市KEL Keelung
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Keelung (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Keelung;')
    sql_insert = '''insert into Keelung value(%s, %s, %s);'''
        
    with urllib.request.urlopen(KEL_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #新北市NTPC New_Taipei
    sql_create = '''
    CREATE TABLE IF NOT EXISTS New_Taipei (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate New_Taipei;')
    sql_insert = '''insert into New_Taipei value(%s, %s, %s);'''
        
    with urllib.request.urlopen(NTPC_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #台北市TPE Taipei
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Taipei (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Taipei;')
    sql_insert = '''insert into Taipei value(%s, %s, %s);'''
        
    with urllib.request.urlopen(TPE_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #桃園市TYN Taoyuan
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Taoyuan (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Taoyuan;')
    sql_insert = '''insert into Taoyuan value(%s, %s, %s);'''
        
    with urllib.request.urlopen(TYN_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #新竹縣HSZ0 Hsinchu_County
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Hsinchu_County (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Hsinchu_County;')
    sql_insert = '''insert into Hsinchu_County value(%s, %s, %s);'''
        
    with urllib.request.urlopen(HSZ0_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #新竹市HSZ1 Hsinchu_City
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Hsinchu_City (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Hsinchu_City;')
    sql_insert = '''insert into Hsinchu_City value(%s, %s, %s);'''
        
    with urllib.request.urlopen(HSZ1_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #苗栗縣ZMI Miaoli
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Miaoli (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Miaoli;')
    sql_insert = '''insert into Miaoli value(%s, %s, %s);'''
        
    with urllib.request.urlopen(ZMI_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #彰化縣CHW Changhua
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Changhua (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Changhua;')
    sql_insert = '''insert into Changhua value(%s, %s, %s);'''
        
    with urllib.request.urlopen(CHW_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #南投縣NTC Nantou
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Nantou (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Nantou;')
    sql_insert = '''insert into Nantou value(%s, %s, %s);'''
        
    with urllib.request.urlopen(NTC_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #雲林縣YUN Yunlin
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Yunlin (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Yunlin;')
    sql_insert = '''insert into Yunlin value(%s, %s, %s);'''
        
    with urllib.request.urlopen(YUN_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #嘉義縣CYI0 Chiayi_County
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Chiayi_County (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Chiayi_County;')
    sql_insert = '''insert into Chiayi_County value(%s, %s, %s);'''
        
    with urllib.request.urlopen(CYI0_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #嘉義市CYI1 Chiayi_City
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Chiayi_City (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Chiayi_City;')
    sql_insert = '''insert into Chiayi_City value(%s, %s, %s);'''
        
    with urllib.request.urlopen(CYI1_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #台南市TNN Tainan
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Tainan (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Tainan;')
    sql_insert = '''insert into Tainan value(%s, %s, %s);'''
        
    with urllib.request.urlopen(TNN_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #高雄市KHH Kaohsiung
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Kaohsiung (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Kaohsiung;')
    sql_insert = '''insert into Kaohsiung value(%s, %s, %s);'''
        
    with urllib.request.urlopen(KHH_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #屏東縣PIF Pingtung
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Pingtung (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Pingtung;')
    sql_insert = '''insert into Pingtung value(%s, %s, %s);'''
        
    with urllib.request.urlopen(PIF_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #宜蘭縣ILA Yilan
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Yilan (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Yilan;')
    sql_insert = '''insert into Yilan value(%s, %s, %s);'''
        
    with urllib.request.urlopen(ILA_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #花蓮縣HUN Hualien
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Hualien (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Hualien;')
    sql_insert = '''insert into Hualien value(%s, %s, %s);'''
        
    with urllib.request.urlopen(HUN_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #台東縣TTT Taitung
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Taitung (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Taitung;')
    sql_insert = '''insert into Taitung value(%s, %s, %s);'''
        
    with urllib.request.urlopen(TTT_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #澎湖縣PEH Penghu
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Penghu (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Penghu;')
    sql_insert = '''insert into Penghu value(%s, %s, %s);'''
        
    with urllib.request.urlopen(PEH_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #金門縣KNH Kinmen
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Kinmen (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Kinmen;')
    sql_insert = '''insert into Kinmen value(%s, %s, %s);'''
        
    with urllib.request.urlopen(KNH_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #連江縣LNN Lienchiang
    sql_create = '''
    CREATE TABLE IF NOT EXISTS Lienchiang (個案研判日 Date NULL,縣市 VARCHAR(255) NULL,確定病例數 VARCHAR(255) NULL);'''
    cursor.execute(sql_create)
    cursor.execute('truncate Lienchiang;')
    sql_insert = '''insert into Lienchiang value(%s, %s, %s);'''
        
    with urllib.request.urlopen(LNN_url) as f:
        f.readline().decode('UTF-8')
        while (True):
            res = f.readline().strip().decode(encoding='UTF-8').split(',')
            # 到沒資料離開迴圈
            if res != ['']:
                cursor.execute(sql_insert,[res[0], res[1], res[2]])
                #print(res)
            else:
                break
        conn.commit()
    
    #cursor.close()
    #conn.close()

create()


# In[2]:


# 初始化sqlalchemy
db = SQLAlchemy()
app = Flask(__name__, static_url_path="/")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:20010303@localhost:3306/2"
# [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]

db.init_app(app)
#db = SQLAlchemy(app)

first_url = "https://htmlpreview.github.io/?https://github.com/zu-z/project/blob/main/first_web.html"
#https://raw.githubusercontent.com/zu-z/project/main/first_web.html
second_url = "https://htmlpreview.github.io/?https://github.com/zu-z/project/blob/main/second_web.html"
#https://raw.githubusercontent.com/zu-z/project/main/second_web.html

@app.route("/")
def first_web():
    #return redirect(first_url)
    return render_template('first_web.html')

@app.route("/second_web", methods=["POST","GET"])
def second_web():
    print(request.method)
    if request.method == "POST":
        user_input = request.values['user_input']
        user_date = request.values['user_date']
    else:
        user_input = request.args.get('user_input')
        user_date = request.args.get('user_date')
    
    date = datetime.datetime.strptime(user_date, "%Y-%m-%d")
    
    if(user_input == '一天'):
        user_date_ = user_date
        date_all = []
        date_all.append(user_date_)
        
        #基隆市KEL Keelung
        sql = """ SELECT 確定病例數 from Keelung where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KEL = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_KEL) == 0):
            data_all_KEL.append("('0',)")
        
        #新北市NTPC New_Taipei
        sql = """ SELECT 確定病例數 from New_Taipei where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_NTPC = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_NTPC) == 0):
            data_all_NTPC.append("('0',)")
        
        #台北市TPE Taipei
        sql = """ SELECT 確定病例數 from Taipei where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TPE = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_TPE) == 0):
            data_all_TPE.append("('0',)")
        
        #桃園市TYN Taoyuan
        sql = """ SELECT 確定病例數 from Taoyuan where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TYN = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_TYN) == 0):
            data_all_TYN.append("('0',)")
        
        #新竹縣HSZ0 Hsinchu_County
        sql = """ SELECT 確定病例數 from Hsinchu_County where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HSZ0 = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_HSZ0) == 0):
            data_all_HSZ0.append("('0',)")
        
        #新竹市HSZ1 Hsinchu_City
        sql = """ SELECT 確定病例數 from Hsinchu_City where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HSZ1 = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_HSZ1) == 0):
            data_all_HSZ1.append("('0',)")
        
        #苗栗縣ZMI Miaoli
        sql = """ SELECT 確定病例數 from Miaoli where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_ZMI = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_ZMI) == 0):
            data_all_ZMI.append("('0',)")
        
        #台中市TXG Taichung
        sql = """ SELECT 確定病例數 from Taichung where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TXG = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_TXG) == 0):
            data_all_TXG.append("('0',)")
        
        #彰化縣CHW Changhua
        sql = """ SELECT 確定病例數 from Changhua where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CHW = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_CHW) == 0):
            data_all_CHW.append("('0',)")
        
        #南投縣NTC Nantou
        sql = """ SELECT 確定病例數 from Nantou where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_NTC = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_NTC) == 0):
            data_all_NTC.append("('0',)")
        
        #雲林縣YUN Yunlin
        sql = """ SELECT 確定病例數 from Yunlin where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_YUN = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_YUN) == 0):
            data_all_YUN.append("('0',)")
        
        #嘉義縣CYI0 Chiayi_County
        sql = """ SELECT 確定病例數 from Chiayi_County where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CYI0 = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_CYI0) == 0):
            data_all_CYI0.append("('0',)")
        
        #嘉義市CYI1 Chiayi_City
        sql = """ SELECT 確定病例數 from Chiayi_City where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CYI1 = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_CYI1) == 0):
            data_all_CYI1.append("('0',)")
        
        #台南市TNN Tainan
        sql = """ SELECT 確定病例數 from Tainan where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TNN = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_TNN) == 0):
            data_all_TNN.append("('0',)")
        
        #高雄市KHH Kaohsiung
        sql = """ SELECT 確定病例數 from Kaohsiung where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KHH = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_KHH) == 0):
            data_all_KHH.append("('0',)")
        
        #屏東縣PIF Pingtung
        sql = """ SELECT 確定病例數 from Pingtung where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_PIF = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_PIF) == 0):
            data_all_PIF.append("('0',)")
        
        #宜蘭縣ILA Yilan
        sql = """ SELECT 確定病例數 from Yilan where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_ILA = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_ILA) == 0):
            data_all_ILA.append("('0',)")
        
        #花蓮縣HUN Hualien
        sql = """ SELECT 確定病例數 from Hualien where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HUN = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_HUN) == 0):
            data_all_HUN.append("('0',)")
        
        #台東縣TTT Taitung
        sql = """ SELECT 確定病例數 from Taitung where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TTT = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_TTT) == 0):
            data_all_TTT.append("('0',)")
        
        #澎湖縣PEH Penghu
        sql = """ SELECT 確定病例數 from Penghu where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_PEH = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_PEH) == 0):
            data_all_PEH.append("('0',)")
        
        #金門縣KNH Kinmen
        sql = """ SELECT 確定病例數 from Kinmen where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KNH = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_KNH) == 0):
            data_all_KNH.append("('0',)")
        
        #連江縣LNN Lienchiang
        sql = """ SELECT 確定病例數 from Lienchiang where 個案研判日 = "%s" ;""" %(user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_LNN = db.engine.execute(sql).fetchall() #取出全部資料
        if (len(data_all_LNN) == 0):
            data_all_LNN.append("('0',)")

    elif(user_input == '一周'):
        user_date_ = (date + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        date_all = []
        for i in range(7):
            date_all += ((date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")).split()
        print(date_all)
        print(type(date_all))
        
        #基隆市KEL Keelung
        sql = """ SELECT 確定病例數 from Keelung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KEL = db.engine.execute(sql).fetchall() #取出全部資料
        
        #新北市NTPC New_Taipei
        sql = """ SELECT 確定病例數 from New_Taipei where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_NTPC = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台北市TPE Taipei
        sql = """ SELECT 確定病例數 from Taipei where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TPE = db.engine.execute(sql).fetchall() #取出全部資料
        
        #桃園市TYN Taoyuan
        sql = """ SELECT 確定病例數 from Taoyuan where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TYN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #新竹縣HSZ0 Hsinchu_County
        sql = """ SELECT 確定病例數 from Hsinchu_County where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HSZ0 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #新竹市HSZ1 Hsinchu_City
        sql = """ SELECT 確定病例數 from Hsinchu_City where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HSZ1 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #苗栗縣ZMI Miaoli
        sql = """ SELECT 確定病例數 from Miaoli where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_ZMI = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台中市TXG Taichung
        sql = """ SELECT 確定病例數 from Taichung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TXG = db.engine.execute(sql).fetchall() #取出全部資料
        
        #彰化縣CHW Changhua
        sql = """ SELECT 確定病例數 from Changhua where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CHW = db.engine.execute(sql).fetchall() #取出全部資料
        
        #南投縣NTC Nantou
        sql = """ SELECT 確定病例數 from Nantou where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_NTC = db.engine.execute(sql).fetchall() #取出全部資料
        
        #雲林縣YUN Yunlin
        sql = """ SELECT 確定病例數 from Yunlin where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_YUN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #嘉義縣CYI0 Chiayi_County
        sql = """ SELECT 確定病例數 from Chiayi_County where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CYI0 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #嘉義市CYI1 Chiayi_City
        sql = """ SELECT 確定病例數 from Chiayi_City where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CYI1 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台南市TNN Tainan
        sql = """ SELECT 確定病例數 from Tainan where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TNN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #高雄市KHH Kaohsiung
        sql = """ SELECT 確定病例數 from Kaohsiung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KHH = db.engine.execute(sql).fetchall() #取出全部資料
        
        #屏東縣PIF Pingtung
        sql = """ SELECT 確定病例數 from Pingtung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_PIF = db.engine.execute(sql).fetchall() #取出全部資料
        
        #宜蘭縣ILA Yilan
        sql = """ SELECT 確定病例數 from Yilan where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_ILA = db.engine.execute(sql).fetchall() #取出全部資料
        
        #花蓮縣HUN Hualien
        sql = """ SELECT 確定病例數 from Hualien where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HUN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台東縣TTT Taitung
        sql = """ SELECT 確定病例數 from Taitung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TTT = db.engine.execute(sql).fetchall() #取出全部資料
        
        #澎湖縣PEH Penghu
        sql = """ SELECT 確定病例數 from Penghu where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_PEH = db.engine.execute(sql).fetchall() #取出全部資料
        
        #金門縣KNH Kinmen
        sql = """ SELECT 確定病例數 from Kinmen where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KNH = db.engine.execute(sql).fetchall() #取出全部資料
        
        #連江縣LNN Lienchiang
        sql = """ SELECT 確定病例數 from Lienchiang where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_LNN = db.engine.execute(sql).fetchall() #取出全部資料
            
    elif(user_input == '一月'):
        user_date_ = (date + relativedelta(months = +1)).strftime("%Y-%m-%d")
        d_start = datetime.datetime.strptime(user_date, "%Y-%m-%d")
        d_end = datetime.datetime.strptime(user_date_, "%Y-%m-%d")
        d_delta = d_end - d_start
        date_all = []
        for i in range(d_delta.days+1):
            date_all += ((date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")).split()
        print(date_all)
        print(type(date_all))
        
        #基隆市KEL Keelung
        sql = """ SELECT 確定病例數 from Keelung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KEL = db.engine.execute(sql).fetchall() #取出全部資料
        
        #新北市NTPC New_Taipei
        sql = """ SELECT 確定病例數 from New_Taipei where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_NTPC = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台北市TPE Taipei
        sql = """ SELECT 確定病例數 from Taipei where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TPE = db.engine.execute(sql).fetchall() #取出全部資料
        
        #桃園市TYN Taoyuan
        sql = """ SELECT 確定病例數 from Taoyuan where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TYN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #新竹縣HSZ0 Hsinchu_County
        sql = """ SELECT 確定病例數 from Hsinchu_County where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HSZ0 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #新竹市HSZ1 Hsinchu_City
        sql = """ SELECT 確定病例數 from Hsinchu_City where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HSZ1 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #苗栗縣ZMI Miaoli
        sql = """ SELECT 確定病例數 from Miaoli where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_ZMI = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台中市TXG Taichung
        sql = """ SELECT 確定病例數 from Taichung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TXG = db.engine.execute(sql).fetchall() #取出全部資料
        
        #彰化縣CHW Changhua
        sql = """ SELECT 確定病例數 from Changhua where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CHW = db.engine.execute(sql).fetchall() #取出全部資料
        
        #南投縣NTC Nantou
        sql = """ SELECT 確定病例數 from Nantou where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_NTC = db.engine.execute(sql).fetchall() #取出全部資料
        
        #雲林縣YUN Yunlin
        sql = """ SELECT 確定病例數 from Yunlin where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_YUN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #嘉義縣CYI0 Chiayi_County
        sql = """ SELECT 確定病例數 from Chiayi_County where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CYI0 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #嘉義市CYI1 Chiayi_City
        sql = """ SELECT 確定病例數 from Chiayi_City where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_CYI1 = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台南市TNN Tainan
        sql = """ SELECT 確定病例數 from Tainan where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TNN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #高雄市KHH Kaohsiung
        sql = """ SELECT 確定病例數 from Kaohsiung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KHH = db.engine.execute(sql).fetchall() #取出全部資料
        
        #屏東縣PIF Pingtung
        sql = """ SELECT 確定病例數 from Pingtung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_PIF = db.engine.execute(sql).fetchall() #取出全部資料
        
        #宜蘭縣ILA Yilan
        sql = """ SELECT 確定病例數 from Yilan where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_ILA = db.engine.execute(sql).fetchall() #取出全部資料
        
        #花蓮縣HUN Hualien
        sql = """ SELECT 確定病例數 from Hualien where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_HUN = db.engine.execute(sql).fetchall() #取出全部資料
        
        #台東縣TTT Taitung
        sql = """ SELECT 確定病例數 from Taitung where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_TTT = db.engine.execute(sql).fetchall() #取出全部資料
        
        #澎湖縣PEH Penghu
        sql = """ SELECT 確定病例數 from Penghu where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_PEH = db.engine.execute(sql).fetchall() #取出全部資料
        
        #金門縣KNH Kinmen
        sql = """ SELECT 確定病例數 from Kinmen where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_KNH = db.engine.execute(sql).fetchall() #取出全部資料
        
        #連江縣LNN Lienchiang
        sql = """ SELECT 確定病例數 from Lienchiang where 個案研判日 >= "%s" AND 個案研判日 <= "%s" ;""" %(user_date, user_date_)
        db.engine.execute(sql) #執行 SQL 指令
        data_all_LNN = db.engine.execute(sql).fetchall() #取出全部資料
        
    
    # list轉string後，取re數字(list)
    data_re01 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_KEL))
    data_re02 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_NTPC))
    data_re03 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_TPE))
    data_re04 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_TYN))
    data_re05 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_HSZ0))
    data_re06 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_HSZ1))
    data_re07 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_ZMI))
    data_re08 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_TXG))
    data_re09 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_CHW))
    data_re10 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_NTC))
    data_re11 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_YUN))
    data_re12 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_CYI0))
    data_re13 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_CYI1))
    data_re14 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_TNN))
    data_re15 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_KHH))
    data_re16 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_PIF))
    data_re17 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_ILA))
    data_re18 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_HUN))
    data_re19 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_TTT))
    data_re20 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_PEH))
    data_re21 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_KNH))
    data_re22 = re.findall(r"\d+", ",".join("%s" %id for id in data_all_LNN))
    
    if (len(data_re01) == 0):
        data_re01.append('0')
    if (len(data_re02) == 0):
        data_re02.append('0')
    if (len(data_re03) == 0):
        data_re03.append('0')
    if (len(data_re04) == 0):
        data_re04.append('0')
    if (len(data_re05) == 0):
        data_re05.append('0')
    if (len(data_re06) == 0):
        data_re06.append('0')
    if (len(data_re07) == 0):
        data_re07.append('0')
    if (len(data_re08) == 0):
        data_re08.append('0')
    if (len(data_re09) == 0):
        data_re09.append('0')
    if (len(data_re10) == 0):
        data_re10.append('0')
    if (len(data_re11) == 0):
        data_re11.append('0')
    if (len(data_re12) == 0):
        data_re12.append('0')
    if (len(data_re13) == 0):
        data_re13.append('0')
    if (len(data_re14) == 0):
        data_re14.append('0')
    if (len(data_re15) == 0):
        data_re15.append('0')
    if (len(data_re16) == 0):
        data_re16.append('0')
    if (len(data_re17) == 0):
        data_re17.append('0')
    if (len(data_re18) == 0):
        data_re18.append('0')
    if (len(data_re19) == 0):
        data_re19.append('0')
    if (len(data_re20) == 0):
        data_re20.append('0')
    if (len(data_re21) == 0):
        data_re21.append('0')
    if (len(data_re22) == 0):
        data_re22.append('0')
    
    # 全國人數加總list
    data_all = []
    for i in range(len(data_re01)): 
        total = (int(data_re01[i]) + int(data_re02[i]) + int(data_re03[i]) + int(data_re04[i]) + 
                 int(data_re05[i]) + int(data_re06[i]) + int(data_re07[i]) + int(data_re08[i]) + 
                 int(data_re09[i]) + int(data_re10[i]) + int(data_re11[i]) + int(data_re12[i]) + 
                 int(data_re13[i]) + int(data_re14[i]) + int(data_re15[i]) + int(data_re16[i]) + 
                 int(data_re17[i]) + int(data_re18[i]) + int(data_re19[i]) + int(data_re20[i]) + 
                 int(data_re21[i]) + int(data_re22[i]))
        print(total)
        data_all.append(total)
    print(data_all)
    
    # 日期最後一天的確診人數
    today_data = data_all[-1]
    data_KEL = data_re01[-1]
    data_NTPC = data_re02[-1]
    data_TPE = data_re03[-1]
    data_TYN = data_re04[-1]
    data_HSZ0 = data_re05[-1]
    data_HSZ1 = data_re06[-1]
    data_ZMI = data_re07[-1]
    data_TXG = data_re08[-1]
    data_CHW = data_re09[-1]
    data_NTC = data_re10[-1]
    data_YUN = data_re11[-1]
    data_CYI0 = data_re12[-1]
    data_CYI1 = data_re13[-1]
    data_TNN = data_re14[-1]
    data_KHH = data_re15[-1]
    data_PIF = data_re16[-1]
    data_ILA = data_re17[-1]
    data_HUN = data_re18[-1]
    data_TTT = data_re19[-1]
    data_PEH = data_re20[-1]
    data_KNH = data_re21[-1]
    data_LNN = data_re22[-1]
    
    # 合併list，全部日期 + 全國確診人數
    list_all = dict(zip(date_all, data_all))
    
    print("user_input：", user_input, type(user_input)) #選擇幾天
    print("user_date：", user_date, type(user_date)) #選擇的日期
    print("user_date_：", user_date_, type(user_date_)) #相加後的日期
    print("data_all_TPE：", data_all_TPE, type(data_all_TPE)) #執行sql指令後的data
    print("data_re03：", data_re03, type(data_re03)) #list轉string後，取re數字(list)
    print("data_all：", data_all, type(data_all)) #全國人數加總list
    print("today_data：", today_data, type(today_data)) #日期最後一天的全國確診人數
    print("data_TPE：", data_TPE, type(data_TPE)) #日期最後一天的TPE確診人數
    print("list_all：", list_all, type(list_all)) #合併list
    
    #return redirect(second_url, **locals())
    return render_template("second_web.html", **locals())

if __name__ == '__main__':
    print('####  Flask Start... ####')
    #app.debug = True
    #app.use_reloader=False
    app.run('0.0.0.0')
    #app.run()
    #db.close() #關閉連線


# In[ ]:




