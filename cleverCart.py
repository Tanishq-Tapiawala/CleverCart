import csv
from recipe_scrapers import scrape_me
import re

### Create a CSV file
csv_file = open('test_recipes.csv', 'w')
csv_writer = csv.writer(csv_file)

### Write the column names to the CSV file
csv_writer.writerow(['Recipe Name', 'Description', 'Instructions', 'Grocery Item Names', 'Grocery Item Quantity', 'Cook Time', 'Serving Size'])

### Can add as many specific URLS you want to add
urls = ['https://www.allrecipes.com/recipe/14385/pasta-salad/', 'https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/', 'https://www.allrecipes.com/clams-casino-stuffed-pasta-shells-recipe-7376480',
        'https://www.allrecipes.com/recipe/13824/deep-fried-turkey/', 'https://www.allrecipes.com/recipe/8543753/creamy-chicken-and-mushroom-stroganoff/', 'https://www.allrecipes.com/recipe/8486301/sour-cream-mashed-potatoes/',
        'https://www.allrecipes.com/recipe/8525647/teriyaki-shrimp-noodles/', 'https://www.allrecipes.com/recipe/12720/grilled-salmon-i/']

### Uncomment this to take websites as an input from the user
# Taking the URLS as an input from the user
# urls = []
# Take the number of websites to scrape as an input from the user
# n = int(input('Enter number of websites to scrape: '))
# for i in range(n):
#     url = input('Enter the URL: ')
#     urls.append(url)

### Iterate over the URLs
for url in urls:
    scraper = scrape_me(url)
    ingredients = scraper.ingredients()
    quantity, name = [], []

    for ingredient in ingredients:
        ### Extract the quantity and name using regular expressions
        match = re.match(r'([\d/ ]+)(\w*)(.*)', ingredient)
        if match:

            ### Decimal serviving size (0.5 or 0.25) were not being extracted properly
            ### So we use this regex to extract them
            pattern = r"([.\d]+\s+\w+)+\s+(.*)"
            text = match.group(3)
            matches = re.search(pattern, text)

            if matches:
                quantity.append(matches.group(1))
                name.append(matches.group(2))
            
            else:
                quantity.append(match.group(1).strip() + ' ' + match.group(2).strip())
                name.append(match.group(3).strip())

    ### Convert the lists to strings            
    name = '\n'.join(name)
    quantity ='\n'.join(quantity)

    ### Extract the instructions and add numbering to them
    lines = scraper.instructions().split('\n')
    instructions = ''
    for i, line in enumerate(lines):
        instructions += f'{i+1}. {line}'
        instructions += '\n'

    ### Convert it to minutes
    total_time =str(scraper.total_time()) + ' minutes'
    
    ### Write the data to the CSV file
    csv_writer.writerow([scraper.title(), scraper.description(), instructions, name, quantity, total_time, scraper.yields()])

### Close the CSV file
csv_file.close()