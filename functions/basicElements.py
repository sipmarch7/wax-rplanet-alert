import requests
import lxml.html as lh
import pandas as pd
import csv

def main():
    url='https://prospectors.online/alchemy/recipes.html'
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    [len(T) for T in tr_elements[:5]]

    #Create empty list
    list=[]
   
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]

        i=0

        #If row is not of size 10, the //tr data is not from our table 
        element = []

        for t in T.iterchildren():
           data=t.text_content()
           
           i+=1
           if i==8 or i==11 or i==12 or i==13 or i==14 or i==15:
               element.append(data)
        
        list.append(element)

    #print(list)

    with open('basicElementsCost.csv', 'w') as f:
        writer = csv.writer(f)
        for element in list:
            writer.writerow(element)
        
        
        #i is the index of our column


main()