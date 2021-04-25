# ライブラリの読み込み
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import json

# URL
url = "https://snkrdunk.com/calendars/2021-04/"
# URLにアクセス 
html = urllib.request.urlopen(url)
# HTMLをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")
# 出力
rawWebdata = soup.find_all(attrs={"class":"article-list"}) #生のdata、配列になる
print(rawWebdata)

def makePrice(rawData):
    scrapPrice=[]
    Price=[] #価格：値段の配列
    for i,rawAttr in enumerate(rawData):
        scrapPrice.append(rawAttr.find(class_= "price"))
        Price.append("".join(scrapPrice[i].find(class_="opacity-link").contents))
        Price[i] = Price[i].replace(" ","").replace("\n","")
    return Price

def makeName(rawData):
    scrapShoeName =[]
    returnShoeName =[]
    for i,rawAttr in enumerate(rawData):
        scrapShoeName.append(rawAttr.find(class_="article-en-title"))
        returnShoeName.append("".join(scrapShoeName[i].find(class_="opacity-link").contents))
        returnShoeName[i] = returnShoeName[i].replace("\t","").replace("\n","")
        print(returnShoeName[i])
    return returnShoeName
    
dt =[] #date
dtM =[] #月
dtD =[] #日
def makeDate(rawData):
    scrapDate =[]
    returnDate =[]

    for i,rawAttr in enumerate(rawData):
        returnDate.append("".join(rawAttr.find(class_="date").contents))
        returnDate[i] =returnDate[i].partition(" ")[0] # M/Dに整形
        dt.append(datetime.strptime(returnDate[i],'%m/%d')) #このへんうまくいってない
        dtM.append(dt[i].month)
        dtD.append(dt[i].day)
        print(str(dtD[i])+"日")
    return returnDate

shoePrice =makePrice(rawWebdata)
shoeName =makeName(rawWebdata)
shoeDate = makeDate(rawWebdata)

jsonData =[]

for i,Attr in enumerate(rawWebdata):
    print("発売日："+shoeDate[i]+"  "+shoeName[i]+"  "+shoePrice[i])


# ここからjsonを作る
testData =[{"month":4,"day":2,"shoes":"testJSon"}]
for i,Attr in enumerate(dt):
    testData.append({"month":dtM[i],"day":dtD[i],"shoes":shoeName[i]})
    print(testData[i])

with open("mydata.json",mode="w",encoding="utf-8") as file:
    json.dump(testData,file,ensure_ascii=False,indent=2)
print("完了")