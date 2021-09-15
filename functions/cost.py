import csv

recipe = ['EARTH', 'EARTH', 'EARTH', 'EXPLOSN']

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
    for element in recipe:
        total = total + int(cost(element))
    return total

print(totalCost(recipe))