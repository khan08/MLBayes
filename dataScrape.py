from BeautifulSoup import BeautifulSoup
import requests
import re
from datetime import date,timedelta
def getStat(date,writeDate):
    f=open('BA.csv','a')
    BASE_URL = "https://www.teamrankings.com/ajax/league/v3/stats_controller.php"
    data = {'type':'team-detail',
            'league':'mlb',
            'stat_id':'6024',
            'season_id':'635',
            'cat_type':'4',
            'view':'stats_v1',
            'is_previous':'0',
            'date':date}
    r = requests.post(BASE_URL,data=data)
    s = BeautifulSoup(r.text)
    regex = re.compile("div_(.)")
    for row in s.findAll(attrs={'class':regex}):
        list=row.findAll("td")
        team = list[1].text
        winPercent = list[2].text
        f.write(team+","+writeDate+","+winPercent+'\n')
    f.close()

def getAllStat(start,end):
    while start<end:
        onDate = start.strftime("%m/%d/%y")
        writeDate = start.strftime('%Y%m%d')
        print onDate
        getStat(onDate,writeDate)
        start = start + timedelta(days=1)













getAllStat(date(2014,4,10),date(2014,9,28))
