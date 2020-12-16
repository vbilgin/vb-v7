# This is a simple Python script
# for me to add expenses to my spending.yml file
# via the command line.

from datetime import date

expense_file = open('spending.yml', 'a')

def get_date():
    purchase_date = input('What is the date of the purchase? (Hit Enter if today) ')
    if purchase_date == '':
        today = date.today()
        purchase_date = today.strftime("%Y-%m-%d")
    return purchase_date

def get_name():
    purchase_name = input('What is the name of the purchase? ')
    return purchase_name

def get_amt():
    purchase_amt = input('What was the amount? ')
    return purchase_amt

while (True):
    purchase_date = get_date()
    purchase_name = get_name()
    purchase_amt = get_amt()

    expense_file.write(f'\n- date: {purchase_date}\n  name: "{purchase_name}"\n  amount: {purchase_amt}')

    print('Purchase added!')
    trigger = input('Add another? (Y or N): ')
    if trigger.lower() == 'y':
        continue
    elif trigger.lower() == 'n':
        expense_file.close()
        break