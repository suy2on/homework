import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta    # 'dbsparta'라는 이름의 db를 사용합니다. 'dbsparta' db가 없다면 새로 만듭니다.

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

musics=soup.select("#body-content > div.newest-list > div > table > tbody > tr") #여러개 음악 가져오기



for music in musics:
    music.select_one("td.number").span.decompose()  # 랭크부분의 자식태그 span을 없애준다

    music_singer = music.select_one("td.info > a.artist").text.strip()
    music_rank = music.select_one("td.number").text.strip()
    music_name = music.select_one("td.info > a.title.ellipsis").text.strip()
    print(music_rank,music_name,music_singer) #출력
    #db에저장
    db.music_rank.insert_one({
        'rank':music_rank,
        'name':music_name,
        'singer':music_singer
    })
