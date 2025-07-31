#Alexander Crespo
import datetime
import csv
# Sets current time when called
#def set_current_year():
    #time = str(datetime.date.today()).split('-')
    #time[0] = time[0][2:]
    #time[0] = 24
    #return time[0]

#print(set_current_year())
#print(set_current_date())
'''''
    Categories is a 2d-array. Below is the categories information
    categories[0] = Date
    categories[1] = Amount
    categories[2] = Transaction Type
    categories[3] = Balance
'''''

#CustomerError class was made in order to throw customer exceptions in the program.
class CustomError(Exception):
    pass

class ExpenseTrackerFile:
    def __init__(self, file = 'NA'):
        self.csv_file = file
        self.cat_trans_date = []
        self.cat_trans_amt = []
        self.cat_trans_type = []
        self.cat_trans_bal = []
        self.cat_trans_desc = []
        #self.time = self.choose_date_by_month_year()
        #self.year = int(set_current_year())
        #self.month = month
        if file != 'NA':
            self.data_list = self.read_file_to_list()
        self.length_of_ind = 0

    @staticmethod
    def print_category_choice():
        print('Categories'
              'Housing, Transportation, Food'
              '\nUtilities, Entertainment, Income'
              '\nSubscriptions, Savings, Misc')

    def read_file_to_list(self):
        with open(self.csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            data_list = []
            for row in csv_reader:
                data_list.append(row)
        return data_list
        #self.check_date_of_data(data_list)

    def choose_date_by_month_year(self):
        while True:
            year = input("Enter the year (YY): ")
            month = input("Enter the month (MM): ")

            # Validate input
            if not year.isdigit() or not month.isdigit():
                print("Invalid input. Year and month must be numeric.")
                continue

            year = int(year)
            month = int(month)

            if not 1 <= month <= 12:
                print("Invalid month. Please enter a number between 1 and 12.")
                continue

            return year, month

    def create_category_list(self):
        categories = [[], [], [], [], []]
        for data in data_list:
            print(data)
            temp_date = data['Transaction Date'].split('/')
            temp_year = temp_date[2]
            temp_month = temp_date[0]


    def check_date_of_data(self, data_list,month,year):
        categories = [[], [], [], [],[]]
        for data in data_list:
            print(data)
            temp_date = data['Transaction Date'].split('/')
            temp_year = temp_date[2]
            temp_month = temp_date[0]
            #print(temp_date)
            print(f"The month is {month} and temp month is {temp_month}")
            print(f"The year is {year} and temp year is {temp_year}")
            if int(temp_year) == year and int(temp_month) == month:
                categories[0].append(data['Transaction Date'])
                categories[1].append(float(data['Transaction Amount']))
                categories[2].append(data['Transaction Type'])
                categories[3].append(float(data['Balance']))
                categories[4].append(data['Transaction Description'])
        self.create_categories(categories)
        self.length_of_ind = len(self.cat_trans_desc)



    def create_categories(self, cats):
        self.cat_trans_date = cats[0]
        self.cat_trans_amt = cats[1]
        self.cat_trans_type = cats[2]
        self.cat_trans_bal = cats[3]
        self.cat_trans_desc = cats[4]

    def get_curr_bal(self):
        return self.cat_trans_bal[0]

    def get_desc(self, ind):
        return self.cat_trans_desc[ind]

    def get_date(self,ind):
        return self.cat_trans_date[ind]

    def get_amt(self, ind):
        if(self.cat_trans_amt[ind] < 0):
            return self.cat_trans_amt[ind] * -1
        return self.cat_trans_amt[ind]

    def get_type(self, ind):
        return self.cat_trans_type[ind]

    def print_trans(self,ind):
        return f'{self.get_date(ind)} | {self.get_desc(ind)} | ${self.get_amt(ind)}'

    def print_trans_user(self):
        for ind in range(self.length_of_ind):
            print(f'Transaction #{ind}:\t{self.get_date(ind)}:{self.get_desc(ind)}')
