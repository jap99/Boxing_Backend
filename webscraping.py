import requests
import re
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from bs4 import BeautifulSoup
from csv import writer

firebase = firebase.FirebaseApplication('https://boxingyeah-e5d30.firebaseio.com/')
# GET
# result = firebase.GET('/user',None)

# POST
result = firebase.POST('/user',{'Three':'Bye'})
print(result)


response = requests.get('http://www.espn.com/boxing/story/_/id/12508267/boxing-schedule')

# the way it showed in Firebase docs - https://console.firebase.google.com/u/0/project/cleandev-ios/settings/serviceaccounts/adminsdk
cred = credentials.Certificate('cleandev-ios-firebase-adminsdk-a8et7-822c83eaca.json')
firebase_admin.initialize_app(cred)

soup = BeautifulSoup(response.text, 'html.parser')

count = 0
# GET DATES, LOCATIONS, TV PROVIDERS
for item in soup.find('div', class_='article-body').find_all('h2'):
    print() 
    print() 
    print() 
    text = item.get_text() 
    print(text)
    if text.find("(") == -1:
        print("BROADCAST INFORMATION CURRENTLY UNAVAILABLE") 
    else: 
        channels = text[text.find("(")+1:text.find(")")].replace('/', ', ') 
        if channels:
            print(channels)  
    array_date_Venue_Location = item.get_text().split(':') 
    date = array_date_Venue_Location[0] 
    print(date) 
    print()
    # GET DATA FOR ALL FIGHTS ON THAT DATE
    for fight in item.find_next_sibling('ul').select('li'): 
        fightArray = fight.select('p')   
        for fightElement in fightArray:
            fightProperties = fightElement.get_text().split(',') 
            # print(fightProperties)
            for x in fightProperties:
                # print(x)  
                if "vs." in x:
                    if "TBA" in x:
                        print("TBA - SEEKS OPPONENT")
                    else:
                        theFighters = x 
                        # isolate each fighter name into its own object
                        fighter1 = theFighters.split('vs.')[0]
                        fighter2 = theFighters.split('vs.')[1]
                        print(fighter1)
                        print(fighter2)
                        if "Title fight:" in x:
                            isTitleFight = True
                            print('TITLE FIGHT') 
                            titleFightFighters = []   
                            titleFightFighters.append(fighter1) 
                            titleFightFighters.append(fighter2) 
                            # only display the name of the weightclass the fight is re:; don't mention who own the belt; ensure it doesn't look exactly like the espn example/text
                        else:
                            isTitleFight = False
                            print('NOT A TITLE FIGHT') 
                            if "weight" in x:
                                weightClass = x[:-1].title()
                                print(weightClass)
                else:
                    if "rounds" in x:
                        
                        l = []
                        for t in x.split():
                            try: 
                                l.append(int(t))
                                numberOfRounds = str(l[0])
                                print('Rounds: ' + numberOfRounds)
                            except ValueError:
                                pass 
                    else:
                        print()
                        continue
                        

                    # if fightArray.count > 3:
                    #     isTitleFight = True
                    #     print(isTitleFight)
                    # else:
                    #     isTitleFight = False
                    #     print(isTitleFight)  
        else:
            continue
            # print("NO OPPONENTS HAVE BEEN SELECTED FOR THIS DATE.")   
    titleFightDates = []
    titleFightDates.append(date) 

        # still need to:
            # 1 - LATER ---------- save the location of the fight to an instance variable
            # 2 - create endpoint & pass data as json
            # 3 - LATER ---------- somehow find out the time of the events
            # 4 - convert date so it has this format: "Friday, December 14, 2019" 
            # 5 - LATER ---------- put a green checkmark next to any title fight - don't say who's belt it is
            # 6 - LATER ---------- don't show fights that are less than 8 rounds
        

# VALIDATE DATA IS VALID
    # ENSURE THERE ARE AT LEAST TWO FIGHTERS (ENSURE NO TBA)
        # THEN CHECK IF MORE THAN 8 ROUNDS
            # IF >8 ROUNDS, CHECK IF FIGHT EXISTS IN FIREBASE YET
# // NOW EITHER WRITE AS JSON FILE AND SAVE TO FIREBASE OR JUST SAVE/DELETE DIRECTLY TO FIREBASE FROM THIS FILE
# DONT INCLUDE A FIGHT IF THE VS. SAYS TBA - OR GO AHEAD BUT DONT SHOW IT TO USER YET; KEEP TRACK OF IT

# OBJECTS - 
#   FIGHTER NAMES 
#   DATE 
#   LOCATION 
#   VENUE 
#   CHANNELS
#   IS_TITLE_FIGHT 
#   WEIGHT CLASS
#   NUM_OF_ROUNDS
#   TRY TO FIND OUT THE TIME IT WILL BE TELEVISED

# ERROR HANDLING
    # BE ABLE TO MANAGE IF DATES CHANGE - FIRST CHECK IF THE FIGHTERS ARE IN THE DATE, IF NOT, CHECK IF THEY'RE ANYWHERE ELSE; IF NOT THEN IT MUST MEAN THE FIGHT HAS BEEN CANCELLED
        # IF IT APPEARS A FIGHT WAS CANCELLED THEN LET USERS WITH NOTIF.S ON KNOW IT APPEARS A FIGHT WAS CANCELLED
        # IF CHANGE OF DATE THEN LET USER KNOW VIA NOTIF.S
    # NEED TO ALSO CHECK EVERY MATCH IN FIREBASE STILL EXISTS IN SCRAPED DATA, MAKE SURE WE DONT SCREW OURSELVES OVER AND ACCIDENTALLY DELETE EVERYTHING SOMEHOW
# Don't print out channels if it says PPV only in between the ( )


# fightArray = fight.find_all('p')
# fightArray = str(fight.get_text()).split(',')

# el = soup.body.contents[1].contents[1].next_sibling.next_sibling
# el = soup.find_all('div')[1]
# el = soup.find(id='section-1')
# el = soup.find(class_='article-body').next_sibling
# el = soup.find(class_='article-body').find_previous_sibling()
# el = soup.find(class_='article-body').find_all('h2')
# el = soup.find(attrs={"href":"#APR"})
# el = soup.select('.article-body')[0].get_text()

# for item in soup.select('.article-body'):
#     title = item.find(class_='post-title').get_text().replace('\n', '')
#     print(item.get_text())
#     print()


# print(el)



