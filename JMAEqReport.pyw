# -*- coding: utf-8 -*-
from asyncore import write
from calendar import month
from dis import code_info
from encodings import utf_8
import time
import requests
import urllib3
import xmltodict
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
urllib3.disable_warnings()

xml = requests.get("https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml")
xml = requests.get("https://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml") #測試用 最新1周資料
xml.encoding = "utf-8"
#取得気象庁XML(地震/火山相關)

sp = BeautifulSoup(xml.text, 'xml')

if xml.status_code == 200:
    print("資料取得正常")
else:
    print("資料取得失敗，請檢查網路或氣象廳網站是否正常")
    exit()
#判定資料是否取得正常


logfile = open("JMAlog.txt", encoding="utf8")
logid1 = logfile.read()
logfile.close
#讀取上次情報ID

print(sp.title.text)
z = ""
for i in sp.select("entry"): #搜尋地震相關的XML
    if "VXSE51" in i.id.text or "VXSE52" in i.id.text or "VXSE53" in i.id.text or "VXSE61" in i.id.text:
        url = i.id.text
        z = "a"
        break

if z == "":
    print("未取得地震資訊")
    exit()

def log():
    logfile = open('JMAlog.txt', encoding="utf8")
    log3 = logfile.read()
    logfile.close
    if log3 != log2:
        exit()

def file(y=5):
    print(output)
    f = open("JMAoutput.txt", "w",encoding="utf8")
    f.write(output)
    f.close()
    time.sleep(y)

def num(y):
    y = y.replace("1","１").replace("2","２").replace("3","３").replace("4","４").replace("5","５").replace("6","６").replace("7","７").replace("8","８").replace("9","９").replace("0","０")
    return y

url = "http://www.yoyo0901.byethost16.com/%e5%9c%b0%e9%9c%87%e6%83%85%e5%a0%b1/%e9%9c%87%e6%ba%90%e3%83%bb%e9%9c%87%e5%ba%a6%e3%81%ab%e9%96%a2%e3%81%99%e3%82%8b%e6%83%85%e5%a0%b1%20VXSE53/32-39_11_05_120615_VXSE53.xml" #test
url = "http://www.yoyo0901.byethost16.com/%e5%9c%b0%e9%9c%87%e6%83%85%e5%a0%b1/%e9%9c%87%e6%ba%90%e3%81%ab%e9%96%a2%e3%81%99%e3%82%8b%e6%83%85%e5%a0%b1%20VXSE52/32-35_08_06_100915_VXSE52.xml" #test
url = "http://www.yoyo0901.byethost16.com/%e5%9c%b0%e9%9c%87%e6%83%85%e5%a0%b1/%e9%9c%87%e6%ba%90%e3%83%bb%e9%9c%87%e5%ba%a6%e3%81%ab%e9%96%a2%e3%81%99%e3%82%8b%e6%83%85%e5%a0%b1%20VXSE53/32-39_05_05_100831_VXSE53.xml" #test
url = "http://www.yoyo0901.byethost16.com/%e5%9c%b0%e9%9c%87%e6%83%85%e5%a0%b1/%e9%a1%95%e8%91%97%e3%81%aa%e5%9c%b0%e9%9c%87%e3%81%ae%e9%9c%87%e6%ba%90%e8%a6%81%e7%b4%a0%e6%9b%b4%e6%96%b0%e3%81%ae%e3%81%8a%e7%9f%a5%e3%82%89%e3%81%9b%20VXSE61/32-35_07_09_100915_VXSE61.xml" #test


#xml2 = requests.get(url) #取得資料

headers1 = dict() #test
headers1["Cookie"]="__test=eb3f55df3488e2eb5ad76e961a3d8e90; _test=6c0c461aa22234658c3ed583b610179e" #test

xml2 = requests.get(url,headers=headers1) #test

xml2.encoding = "utf-8"
xml2=xmltodict.parse(xml2.text) #XML轉JSON

commentcode = {"0211":"津波警報等を発表中です",
"0212":"日本の沿岸で多少の潮位変動があるかもしれませんが　被害の心配はありません",
"0215":"この地震による津波の心配はありません",
"0221":"太平洋の広域に津波発生の可能性があります",
"0222":"太平洋で津波発生の可能性があります",
"0223":"北西太平洋で津波発生の可能性があります",
"0224":"インド洋の広域に津波発生の可能性があります",
"0225":"インド洋で津波発生の可能性があります",
"0226":"震源の近傍で津波発生の可能性があります",
"0227":"震源の近傍で小さな津波発生の可能性がありますが　被害の心配はありません",
"0229":"日本への津波の有無については現在調査中です",
"0230":"この地震による日本への津波の影響はありません",
"0242":"この地震で緊急地震速報を発表しましたが　観測された最大震度は２です",
"0243":"この地震で緊急地震速報を発表しましたが　観測された最大震度は１です",
"0244":"この地震で緊急地震速報を発表しましたが　震度１以上は観測されていません",
"0245":"この地震で緊急地震速報を発表しましたが　強い揺れは観測されません"}

data = xml2["Report"] #資料主體

title = data["Head"]["Title"] #標題
headline = data["Head"]["Headline"]["Text"] #註解文
try:
    earthquake = data["Body"]["Earthquake"] #震源資訊
    loc = earthquake["Hypocenter"]["Area"]["Name"] #震源地
    try:
        if "深さ" in earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"]["@description"]: #深度
            dep = earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"]["@description"].split("深さ")[1].replace("　","").replace("ｋｍ","キロ").replace("は","")
        elif "ごく浅い" in earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"]["@description"]:
            dep = "ごく浅い"
        elif "震源要素不明" in earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"]["@description"]:
            dep = "不明"
    except:
        if "深さ" in earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"][1]["@description"]: #深度
            dep = earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"][1]["@description"].split("深さ")[1].replace("　","").replace("ｋｍ","キロ").replace("は","")
        elif "ごく浅い" in earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"][1]["@description"]:
            dep = "ごく浅い"
        elif "震源要素不明" in earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"][1]["@description"]:
            dep = "不明"
    mag = earthquake["jmx_eb:Magnitude"]["@description"].replace("Ｍ","") #規模
    if "巨大地震" in mag:
        mag = "８以上"

except:
    earthquake = ""
    loc = ""
    dep = ""
    mag = ""
    print("未取得震源資訊")

try:
    intensity = data["Body"]["Intensity"]["Observation"] #震度資訊
    pref = intensity["Pref"] 
    maxint = intensity["MaxInt"] #最大震度
except:
    intensity = ""
    pref = ""
    maxint = ""
    print("未取得震度資訊")

try: #固定付加文
    comment = data["Body"]["Comments"]["ForecastComment"]
    comtext = comment["Text"].split(" ")
    comcode = comment["Code"].split(" ")
except:
    comment = ""
    comtext = ""
    comcode = ""

try: #地震發生時間
    eventtime = earthquake["ArrivalTime"]
    mon = eventtime[5:7]
    day = eventtime[8:10]
    hou = int(eventtime[11:13])
    min = eventtime[14:16]
except:
    eventtime = data["Head"]["EventID"]
    mon = eventtime[4:6]
    day = eventtime[6:8]
    hou = int(eventtime[8:10])
    min = eventtime[10:12]

if hou > 11:
    hou -= 12
    ampm = "午後"
else:
    ampm = "午前"
hou = str(hou)

if mon[:1] == "0":
    mon = mon.replace("0","")
if day[:1] == "0":
    day = day.replace("0","")
if hou[:1] == "0":
    hou = hou.replace("0","")
if min[:1] == "0":
    min = min.replace("0","")    

if "震源要素更新" in title:
    eventtime = f"{mon}月{day}日{ampm}{hou}時{min}分頃"
else:
    eventtime = f"{ampm}{hou}時{min}分頃"

eventtime = num(eventtime)


a = 0
b = 0
c = 0
cityint = {}
areaint = {}

for i in pref: #將震度及名稱存到字典
    if type(i) == str:
        i = pref
        a = 1
    for j in i["Area"]:
        if type(j) == str:
            j = i["Area"]
            b = 1
        try:
            for k in j["City"]:
                if type(k) == str:
                    k = j["City"]
                    c = 1
                try:
                    cityint[k["Name"]] = k["MaxInt"]
                except:
                    cityint[k["Name"]] = k["Condition"]
                if c == 1:
                    break
        except:
            pass
        
        try:
            areaint[j["Name"]] = j["MaxInt"]
        except:
            areaint[j["Name"]] = j["Condition"]

        if b == 1:
            break
    if a == 1:
        break

a = 0
for i in commentcode:
    if i in comcode:
        print(commentcode[i])
    a += 1


print(eventtime)
print(loc)
print(dep)
print(mag)
print(maxint)
print(comcode)