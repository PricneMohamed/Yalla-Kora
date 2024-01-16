import requests
from bs4 import BeautifulSoup
import sqlite3

match_date = input("Enter Match Date Please And Follow This DD/MM/YYYY: ")

src = requests.get(f"https://www.yallakora.com/match-center?date={match_date}#days")

file_name = input("""
            Enter File Name Please:  
                    """)

def func_one(src , file_name):
    code_one = src.content
    code_two = BeautifulSoup(code_one,'lxml')

    code_3 = code_two.find_all('div',{'class','matchCard'})

    def func_sql(file_name ,code_3):
        try:
            name =code_3.contents[1].find('h2').text.strip()
            ul =code_3.contents[3].find_all('div',{'class':'liItem'})
            for i in range(len(ul)):
                teamA = ul[i].find_all('div', {'class': 'teamA'})[0].text.strip()
                teamB = ul[i].find_all('div', {'class': 'teamB'})[0].text.strip()
                score = ul[i].find('div', {'class': 'MResult'}).find_all('span',{'class':'score'})
                time = ul[i].find('div', {'class': 'MResult'}).find('span',{'class':'time'}).text.strip()
                result = f"{score[0].text.strip()} - {score[1].text.strip()}"
                db = sqlite3.connect(f"{file_name}.db")
                cr = db.cursor()
                cr.execute(f"CREATE TABLE IF NOT EXISTS {file_name}(Championship TEXT,Team_A TEXT , Team_B TEXT , Score_team_A INTEGER ,Score_TeamB INTEGER , Time TEXT )")
                cr.execute(f"INSERT INTO {file_name}(Championship ,Team_A , Team_B, Score_team_A ,Score_TeamB, Time) VALUES('{name}','{teamA}' ,'{teamB}','{score[0].text.strip()}' , '{score[1].text.strip()}','{time}')")
                db.commit()
                db.close()
            else:
                print("The procces is done")
        except:
            raise Exception(ValueError("An error has occurred"))

    for x in range(len(code_3)):
        func_sql(file_name,code_3[x])


        
func_one(src,file_name)
