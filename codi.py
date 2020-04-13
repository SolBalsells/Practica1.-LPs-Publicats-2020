import requests
import pandas as pd  
from bs4 import BeautifulSoup

i = 1
stop = False
Artist = []
Title = []
Date = []
Genre = []
Label = []
CriticScore = []
CriticNum = []
UserScore = []
UserNum = []

while stop == False:
    url = 'https://www.albumoftheyear.org/2020/releases/?s=release&page=' +  str(i)
    page = requests.get(url)
    content = BeautifulSoup(page.content, features="html.parser")
    albums = content.find_all("div", {"class": "albumBlock five"})
    if len(albums) == 0:
        stop = True
    for j in range(len(albums)):
        date = albums[j].find("div", {"class": "date"})
        if 'unknown-artist-you-are-supposed-to-pay-for-this-release-you-are-supposed-to-pay-copious' in albums[j].find("a").get('href'):
            print('NO')
        else: 
            if date.get_text() not in ("2020", "Jan", "Feb", "Mar", "Apr", 
                                   "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"):
                link = 'https://www.albumoftheyear.org' + albums[j].find("a").get('href')
                page_album = requests.get(link)
                pAsoup = BeautifulSoup(page_album.content, features="html.parser")
                detailRow = pAsoup.find_all("div", {"class": "detailRow"})
                FormatProject = detailRow[1].get_text()[0:2]
                if FormatProject == 'LP':
                    title = pAsoup.find("div", {"class": "albumTitle"})
                    artist = pAsoup.find("div", {"class": "artist"})
                    critic = pAsoup.find("div", {"class": "albumCriticScore"})
                    critic_num = pAsoup.find("span", {"itemprop": "reviewCount"})
                    user = pAsoup.find("div", {"class": "albumUserScore"})
                    user_num = pAsoup.find("div", {"class": "text numReviews"})
                    day = detailRow[0].contents[1][1:3]
                    month = detailRow[0].a.get_text()
                    date = str(month + " " + day)
                    label = detailRow[2].get_text()[:-8]
                    genre = detailRow[3].get_text()[:-9]
                    criticscore = critic.get_text()
                    if (criticscore != 'NR'): criticnum = critic_num.get_text()
                    else: criticnum = 0
                    userscore = user.get_text()
                    if (userscore != 'NR'): usernum = user_num.strong.get_text()
                    else: usernum = 0
                    Artist.append(artist.get_text())
                    Title.append(title.get_text())
                    Date.append(date)
                    Genre.append(genre)
                    Label.append(label)
                    CriticScore.append(criticscore)
                    CriticNum.append(criticnum)
                    UserScore.append(userscore)
                    UserNum.append(usernum)
    print(i)
    i = i + 1

df = pd.DataFrame({'Artist': Artist, 'Title': Title, 'Date': Date, 'Genre': Genre, 'Label': Label,
                  'CriticScore': CriticScore, 'CriticNum': CriticNum, 'UserScore': UserScore,
                  'UserNum': UserNum}) 
df.to_csv('ep.csv', index=True, sep=';')