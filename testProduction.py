from os import error
from os import system
import requests
import json
import time
import csv 
import smtplib, ssl
from email.mime.text import MIMEText


def basicsCostElement(element):
    with open('basicElementsCost.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            if row[0] == element:
                return row

def basicsCostRecipe(recipe):
    airs = 0
    earths = 0
    waters = 0
    fires = 0 
    for el in recipe:
        temp = basicsCostElement(el)
        airs = airs + int(temp[1])
        earths = earths + int(temp[2])
        waters = waters + int(temp[3])
        fires = fires + int(temp[4])
    basicsCost = [airs, earths, waters, fires]
    return basicsCost


#find the recipe cost 
def cost(element):
    basic = ['EARTH', 'WATER', 'AIR', 'FIRE']
    if element in basic:
        return 10000
    with open('recipes.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            if row[7] == element:
                return row[9]
              
def totalCost(recipe):
    total = 0
    costs = []
    for element in recipe:
        temp = int(cost(element))
        total = total + temp
        costs.append(temp)
    costs.append(total)
    return costs

def send_email(invention, recipe, totalCost, inventor_name, basicsCost):
    port = 465  # For SSL

    receiver_email = getEmails()
    
    message = MIMEText(invention+ " was INVENTED by " + inventor_name + "\n\n" +
        "TOTAL Aether: "+ str(totalCost)[0:-3]+","+str(totalCost)[-3:] + "\n\n" +
        "RECIPE: \n" +
        recipe[0][0] + " - " + str(recipe[0][1]) + "\n" +
        recipe[1][0] + " - " + str(recipe[1][1]) + "\n" +
        recipe[2][0] + " - " + str(recipe[2][1]) + "\n" +
        recipe[3][0] + " - " + str(recipe[3][1]) + "\n\n" +
        "Rplanet Generator" + " https://rplanet.io/generator" + "\n" +
        "Tools Generator" + " https://rplanet.tools/generator" + "\n" +
        "Alchemy Generator" + " https://prospectors.online/alchemy/create/create.html" + "\n\n" +
        recipe[0][0] + " https://wax.simplemarket.io/trading/ft/a.rplanet/"+recipe[0][0] + "\n" +
        recipe[1][0] + " https://wax.simplemarket.io/trading/ft/a.rplanet/"+recipe[1][0] + "\n" +
        recipe[2][0] + " https://wax.simplemarket.io/trading/ft/a.rplanet/"+recipe[2][0] + "\n" +
        recipe[3][0] + " https://wax.simplemarket.io/trading/ft/a.rplanet/"+recipe[3][0] + "\n\n" +
        "BASICS\n" + 
        "AIRs:       " + str(basicsCost[0]) + "\n" +
        "EARTHs: " + str(basicsCost[1]) + "\n" +
        "WATERs: " + str(basicsCost[2]) + "\n" +
        "FIREs:     " + str(basicsCost[3]) + "\n\n\n" +
        "To See how many are left from the a.rplanet nftelement Table on wax.bloks.io (scroll table to right):" + "\n" +
        "https://wax.bloks.io/account/a.rplanet?loadContract=true&tab=Tables&table=nftelements&account=a.rplanet&scope=a.rplanet&limit=100&lower_bound="
        + invention + "\n\n" +"DONATIONS:  lv5b.wam"
        )
        
    message['Subject'] = invention + " was DISCOVERED!!"
    message['From'] = sender_email
    message['To'] = ", ".join(receiver_email)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", port)
        server.login(sender_email, password)
        print("Login Succesfull")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email was Sent")
        server.quit()
    except:
        print("Error Logging in")


def recipeWithCosts(recipe, totalCosts):
    return [[recipe[0], totalCosts[0]],[recipe[1], totalCosts[1]],[recipe[2], totalCosts[2]],[recipe[3], totalCosts[3]]]


# txid = input("enter the txid: ")
# txid = '598659cd3e899476a00256a9a29e24d5054dddd848ac9626bac9ad43b95050e1'
def fetch_txid():
    #
    #print(invented_elements)
    #
    url = 'https://api.waxsweden.org/v2/history/get_actions?account=w.rplanet&filter=a.rplanet:discover&skip=0&limit=50'
    response = requests.get(url)
    raw_data = json.loads(response.content)
    # txs_ids = [ raw_data['actions'][0]['trx_id'] ]
    
    # raw_data['actions'][0]['trx_id']
    print(raw_data['actions'][0]['timestamp'])
    for i in range(50):
        #print(str(i)+".  "+ raw_data['actions'][i]['act']['data']['str_symbol'] + " - " + raw_data['actions'][i]['time$
        fetch_discovery(raw_data['actions'][i], i)
        try:
            #fetch_discovery(raw_data['actions'][i], i)
            pass
        except:
            pass
            #print(raw_data['actions'][i])
        #time.sleep(0.1)


def fetch_discovery(action, i):
    #url = 'https://api.waxsweden.org/v2/history/get_transaction?id=' + txid

    #response = requests.get(url)
    #raw_data = json.loads(response.content)

    #print("- "+ action['act']['data']['str_symbol'])
    
    element_name  = action['act']['data']['str_symbol']
    #memo = raw_data['actions'][1]['act']['data']['memo']

    if element_name not in invented_elements and element_name != "": #in uninvented_elements: #invented_elements: #memo$
        recipe = []
        elements = action['act']['data']['elements']
        inventor_name = action['act']['data']['user']
        print('Element discovered is: ' + element_name)
        print('Inventor is:' + inventor_name)
        print('trx_id: '+action['trx_id'])
        for i in elements:
            recipe.append(i[2:])
        print("the recipe is")
        print(recipe)
        print("YOOYOYOYOYOYOY "+action['timestamp']+" OYOYOOYOYOYOY")
        basicsCost = basicsCostRecipe(recipe)
        #print(basicsCost)

        send_email(element_name, recipeWithCosts(recipe, totalCost(recipe)) ,totalCost(recipe)[4], inventor_name, basicsCost)

        #append the new element in the csv
        fields=['serialNo','Date','inventor_name', recipe[0], recipe[1], recipe[2], recipe[3], element_name, 1, totalCost(recipe)[4]]
        with open('recipes.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        invented_elements.append(element_name)
        #uninvented_elements.remove(element_name)
        with open('basicElementsCost.csv', 'a') as f2:
            writer2 = csv.writer(f2)
            basicsCost.insert(0, element_name)
            writer2.writerow(basicsCost)
        
        time.sleep(5)
    else:
        #print(str(i)+".    - "+ element_name + " has already been discovered " + action['timestamp'])
        pass

# downloads latest csv and creates a table with the name of the already invented elements
def find_invented():
    invented_elements = []
    system('curl -o recipes.csv https://prospectors.online/alchemy/alchemy-recipes.csv')

    with open('recipes.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            invented_elements.append(row[7])
    return invented_elements

def getEmails():
    receiver_email = []
    with open('testEmails.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            #print(row[0])
            receiver_email.append(row[0])
    return receiver_email



def main():

    print("The script is succesfully running , keep me on")

    while True:
        fetch_txid()
        try:
            #fetch_txid()
            pass
        except:
            pass
        time.sleep(1)


#download latest csv with invented recipes
invented_elements = find_invented()
#find_invented()

#uninvented_elements = ['GAS', 'NFT', 'SODA', 'OZONE', 'UPLIFT', 'BACTERI', 'BUBBLES']

#define the email accounts to send and receive the aler
sender_email = "email" #input("sender email: ")
password = "pass" #input("sender password: ")

# start the script
main()


#req_memo = "Win!!! New element has been opened."
# fetch_txid()

