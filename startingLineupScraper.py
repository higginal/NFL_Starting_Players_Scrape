import requests
from lxml import html
from bs4 import BeautifulSoup as Soup
from bs4 import Comment
import sys
from multiprocessing import Pool, TimeoutError
from functools import reduce

output = "Week,Team,QB,RB,WR,WR,WR,TE,LT,LG,C,RG,RT,DE,DE,DT,DT,OLB,MLB,CB,CB,S,S,S"
output += "\n"

def scrapeGame(game):

    currentRow = ""

    game = Soup(game, 'lxml')

    if game.has_attr("class"):
        return ""
    try :
        week = game.find('th').text
        score = game.find('td', {'data-stat': 'boxscore_word'}).find('a')
    
        if(score == None):
            return ""

        scoreUrl = score.get('href')
        cbsUrl = 'https://www.pro-football-reference.com' + scoreUrl

 
        req = requests.get(cbsUrl)
        soup = Soup(req.text, 'lxml')
        count = 0

        scorebox = soup.find('div', {'class': 'scorebox'})

        home, away = [x.text for x in scorebox.find_all('a', {'itemprop': 'name'})]

        home_div = soup.find('div', {'id' : 'all_home_starters'})

        homePlayerTable= home_div.find_all(text=lambda text:isinstance(text, Comment))

        positionMap = {
            'QB': " ",
            'LT': " ",
            'LG': " ",
            'C': " ",
            "RG": " ",
            "RT": " "
        }
        set = False

        rbs = []
        wrs = []
        tes = []
        lbs = []
        des = []
        dts = []
        cbs = []
        s = []

        currentRow += str(week) + "," + home + ","

        for elem in homePlayerTable:
            elms = Soup(elem, 'lxml').find('table', {'id': 'home_starters'})
            if elms != None:
                players  = elms.find_all('tr')
                for guy in players:
            
                    name = guy.find('th')
                    pos = guy.find('td')

                    if pos != None and name != None:
                        if('RB' in pos.text or 'HB' in pos.text or 'FB' in pos.text):
                            rbs.append(name.text)
                        elif('LB' in pos.text or 'WILL' in pos.text or 'MIKE' in pos.text):
                            lbs.append(name.text)
                        elif('WR' in pos.text):
                            wrs.append(name.text)
                        elif('TE' in pos.text):
                            tes.append(name.text)
                        elif('DE' in pos.text or 'DL' in pos.text):
                            des.append(name.text)
                        elif('DT' in pos.text or 'NT' in pos.text):
                            dts.append(name.text)
                        elif('CB' in pos.text or 'DB' in pos.text):
                            cbs.append(name.text)
                        elif('S' in pos.text):
                            s.append(name.text)
                        else:
                            positionMap[pos.text] = name.text
                        set = True

        if(set):
            currentRow += positionMap['QB'] + ","
            if(len(rbs) > 0):
                currentRow += ",".join(rbs) + ","
            if(len(wrs) > 0):
                currentRow +=  ",".join(wrs) + "," 
            if(len(tes) > 0):
                currentRow += ",".join(tes) + ","
            currentRow +=  positionMap['LT'] + "," +  positionMap['LG'] + "," + positionMap['C'] + "," + positionMap['RG'] + "," + positionMap['RT'] + ","
            if(len(des ) > 0):
                currentRow += ",".join(des) + ","
            if(len(dts) > 0):
                currentRow += ",".join(dts) + ","
            if(len(lbs) > 0):
                currentRow += ",".join(lbs) + ","
            if(len(cbs) > 0):
                currentRow += ",".join(cbs) + ","
            currentRow += ",".join(s)
            currentRow += '\n'

        vis_div = soup.find('div', {'id' : 'all_vis_starters'})

        visPlayerTable= vis_div.find_all(text=lambda text:isinstance(text, Comment))

        currentRow += str(week) + "," + away + ","

        positionMap = {
            'QB': " ",
            'LT': " ",
            'LG': " ",
            'C': " ",
            "RG": " ",
            "RT": " "
        }
        set = False
        rbs = []
        tes = []
        lbs = []
        wrs = []
        des = []
        dts = []
        cbs = []
        s = []

        for elem in visPlayerTable:
            elms = Soup(elem, 'lxml').find('table', {'id': 'vis_starters'})
            if elms != None:
                players  = elms.find_all('tr')
                for guy in players:
            
                    name = guy.find('th')
                    pos = guy.find('td')
            
                    if pos != None and name != None:
                        if('RB' in pos.text or 'HB' in pos.text or 'FB' in pos.text):
                            rbs.append(name.text)
                        elif('LB' in pos.text or 'WILL' in pos.text or 'MIKE' in pos.text):
                            lbs.append(name.text)
                        elif('WR' in pos.text):
                            wrs.append(name.text)
                        elif('TE' in pos.text):
                            tes.append(name.text)
                        elif('DE' in pos.text or 'DL' in pos.text):
                            des.append(name.text)
                        elif('DT' in pos.text or 'NT' in pos.text):
                            dts.append(name.text)
                        elif('CB' in pos.text or 'DB' in pos.text):
                            cbs.append(name.text)
                        elif('S' in pos.text):
                            s.append(name.text)
                        else:
                            positionMap[pos.text] = name.text                            
                        set = True
                            
        if(set):
            currentRow += positionMap['QB'] + ","
            if(len(rbs) > 0):
                currentRow += ",".join(rbs) + ","
            if(len(wrs) > 0):
                currentRow +=  ",".join(wrs) + "," 
            if(len(tes) > 0):
                currentRow += ",".join(tes) + ","
            currentRow +=  positionMap['LT'] + "," +  positionMap['LG'] + "," + positionMap['C'] + "," + positionMap['RG'] + "," + positionMap['RT'] + ","
            if(len(des ) > 0):
                currentRow += ",".join(des) + ","
            if(len(dts) > 0):
                currentRow += ",".join(dts) + ","
            if(len(lbs) > 0):
                currentRow += ",".join(lbs) + ","
            if(len(cbs) > 0):
                currentRow += ",".join(cbs) + ","
            currentRow += ",".join(s)
            currentRow += '\n' 

        return currentRow
    except AttributeError:
        return ""


year = input("Enter a season year: ")

threads = int(input("Enter number of threads (more is faster): "))

#For grabbing the entire season page
fullSeasonUrl = 'https://www.pro-football-reference.com/years/' + year + '/games.htm'
reqFull = requests.get(fullSeasonUrl)
soupFull = Soup(reqFull.text, 'lxml')
allGamesTable = soupFull.find('table', {'id': 'games'}).find('tbody')

#parallel processing - to run faster
pool = Pool(processes=threads)
allGames = [str(val) for val in allGamesTable.find_all('tr')]
returnVals = pool.map(scrapeGame, allGames)
bottomString = reduce(lambda x, y: x + y, returnVals)
output += bottomString

#write's file
f = open(year + "_positions.csv", "w")
f.write(output)
f.close()

