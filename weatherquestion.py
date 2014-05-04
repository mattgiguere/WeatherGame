import json
import urllib2
import random
from datetime import datetime, timedelta

class Question(object):
    """Store question and relavent historical data"""

    def __init__(self, qid):
        self.qid = qid
        self.country, self.city = GetCity()
        self.printableCity = self.city.replace("_", " ")
        self.guessDate = datetime.now()
        dt = timedelta(days=random.randint(1, 6),
                       hours=random.randint(0, 24))
        self.guessDate = self.guessDate + dt
        self.month = self.guessDate.strftime("%m")
        self.day = self.guessDate.strftime("%d")
        self.year = self.guessDate.strftime("%Y")
        self.hour = self.guessDate.strftime("%H")
        self.history, self.hourlyTemp = self.GetHistory()
        self.questionType, self.question = self.GetQuestion()
        if self.questionType == 4:
            self.questionTypeCode = 2
        else:
            self.questionTypeCode = 1

    def GetHistory(self):
        history = {"maxTemp":[], "minTemp":[], "meanTemp":[], "precip":[]}
        year = int(self.year)
        hourlyTemps = []
        for i in range(24):
            hourlyTemps.append([])
        while year >= 1970:
            dateString = str(year) + self.month + self.day
            oneYearData = QueryWundergroundHistory(self.country, self.city, dateString)
            try:
                history["maxTemp"].append(oneYearData["history"]["dailysummary"][0]["maxtempi"])
                history["minTemp"].append(oneYearData["history"]["dailysummary"][0]["mintempi"])
                history["meanTemp"].append(oneYearData["history"]["dailysummary"][0]["meantempi"])
                history["precip"].append(oneYearData["history"]["dailysummary"][0]["precipi"])
                for i in range(24):
                    try:
                        hourlyTemps[i].append(oneYearData["history"]["observations"][i]["tempi"])
                    except IndexError:
                        hourlyTemps[i].append(-99999)
                yearInRecord = int(oneYearData["history"]["date"]["year"])
                monthInRecord = oneYearData["history"]["date"]["mon"]
                dayInRecord = oneYearData["history"]["date"]["mday"]
                if (yearInRecord != year or monthInRecord != self.month or
                    dayInRecord != self.day):
                    year = 1900
            except IndexError:
                year = 1900
            year -= 1
        return history, hourlyTemps

    def GetAnswer(self):
        dateString = str(self.year) + self.month + self.day
        answerData = QueryWundergroundHistory(self.country, self.city, dateString)
        if len(answerData["history"]["dailysummary"]) == 0:
            return -99999
        if self.questionType == 1:
            return int(answerData["history"]["observations"][int(self.guessDate)]["tempi"])
        elif self.questionType == 2:
            return int(answerData["history"]["dailysummary"][0]["maxtempi"])
        elif self.questionType == 3:
            return int(answerData["history"]["dailysummary"][0]["mintempi"])
        elif self.questionType == 4:
            rainFall = float(answerData["history"]["dailysummary"][0]["precipi"])
            if rainFall < 0.1:
                return False
            else:
                return True


    def GetQuestion(self):
        qid = random.randint(1,4)
        if qid == 1:
            q = "What will the temperature in {:s} be on ".format(self.printableCity)+\
                self.guessDate.strftime('%a %b %d')+" at "+self.guessDate.strftime("%I %p")+ "?"
        elif qid == 2:
            q = "What will the maximum temperature in {:s} be on ".format(self.printableCity)+\
                self.guessDate.strftime('%a %b %d')+"?"
        elif qid == 3:
            q = "What will the minimum temperature in {:s} be on ".format(self.printableCity)+\
                self.guessDate.strftime('%a %b %d')+"?"
        elif qid == 4:
            q = "Will it rain in {:s} on ".format(self.printableCity)+\
                self.guessDate.strftime('%a %b %d')+"?"
        return qid, q


def QueryWundergroundHistory(country, city, date):
    f = urllib2.urlopen("http://api.wunderground.com/api/2c63603de70b6a76/history_"+
                         date+"/q/"+country+"/"+city+".json")
    jsonString = f.read()
    return json.loads(jsonString)


def URLtoJSON(url):
    f = urllib2.urlopen(url)
    string = f.read()
    return json.loads(string)


def GetCity():
    cities = {"Paris":"FR",
              "London":"UK",
              "Bangkok":"TH",
              "New_York":"NY",
              "Dubai":"AE",
              "Istanbul":"TR",
              "Rome":"IT",
              "Los_Angeles":"CA",
              "Toronto":"Canada",
              "Barcelona":"ES",
              "San_Francisco":"CA",
              "Vancouver":"Canada",
              "Budapest":"HU",
              "Tokyo":"JP",
              "Mexico_City":"MX",
              "Lima":"PE",
              "Santiago":"CL"}

    key = cities.keys()[random.randint(0, len(cities)-1)]
    return cities[key], key

def main():
    for i in range(50):
        q = Question(1)
        print q.question
