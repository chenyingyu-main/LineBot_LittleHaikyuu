import requests
from bs4 import BeautifulSoup

url = 'https://zh.m.wikipedia.org/zh-tw/排球'

html = requests.get(url)
soup = BeautifulSoup(html.text, "html.parser")
rules = soup.find('section', class_='mf-section-2')

def get_foul_rule():
    foul_rule = []
    list_foul = rules.select('ul')[0].select('li')
    title_foul = rules.find_all('span', class_='mw-headline')[0]

    foul_rule.append(title_foul.getText())
    for i in list_foul:
        foul_rule.append(i.getText())

    return foul_rule

def change_and_timeout():
    change_rule = []
    title_change = rules.find_all('span', class_='mw-headline')[1]
    l1 = rules.select('p')[0]
    l2 = rules.select('p')[1]

    change_rule.append(title_change.getText())
    change_rule.append(l1.getText())
    change_rule.append(l2.getText())
    return change_rule

def score():
    score_rule = []
    title_score = rules.find_all('span', class_='mw-headline')[2]
    score_rule.append(title_score.getText())

    list_p = rules.select('p')
    for i in range(len(list_p)):
        if i > 1:
            score_rule.append(list_p[i].getText())
    return score_rule





