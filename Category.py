#Alexander Crespo
import ExpenseTracker
import matplotlib.pyplot as plt

'''
Category is a class used in order to create different Category options and turn them into their own instances.
Category accepts an instance of the ExpenseTracker class which takes a file in a certain format as a parameter
for creating the class and separates all the information in the file to necessary subcategories such as date, balance,
description etc..

Category Class Variables
categorys_selected (List) - A list of strings, that will contain the category's selected for that run of the program
category_options (List) - This will hold all possible category options

Category Instance Variables
bill_indexs - list of index's representing the bills from the file
amount - amount is the total of all bills
category_type - it holds the category type
file - is the a class instance of ExpenseTracker

add_bill_amt_to_selected
select_category ask the user to enter category type, and checks to see if it exist, if it does it adds the category 
to categorys_selected list in the Category class 
'''


class Category():
    categorys_selected = {}
    category_options = ["Housing", "Transportation", "Food",
                        "Utilities", "Entertainment", "Income", "Subscriptions", "Savings", "Misc"]
    def __init__(self,file,type = ''):
        self.bill_indexs = []
        self.amount = 0
        self.category_type = type
        self.file = file

    @classmethod
    def add_bill_amt_to_selected(cls, category_type, amount):
        if category_type in cls.categorys_selected:
            cls.categorys_selected[category_type] += amount
        else:
            cls.categorys_selected[category_type] = amount

    def add_bill_index(self,ind):
        self.bill_indexs.append(ind)

    def add_bill_amt(self,ind):
        self.amount += self.file.get_amt(ind)


    def select_bill(self):
        self.file.print_trans_user()
        flag = ''
        while(flag!='q'):
            try:
                trans_num = int(input("Enter transaction number: "))
                self.validate_bill(trans_num)
                self.add_bill_index(trans_num)
                self.add_bill_amt(trans_num)
                flag = 'q'
            except ExpenseTracker.CustomError as outOfRange:
                print(outOfRange)
            except ValueError as incorrecttype:
                print(f"{incorrecttype} \nTry Again")


    def validate_bill(self, trans_num):
        if -1 < trans_num < self.file.length_of_ind:
            return
        else:
            raise ExpenseTracker.CustomError(f"The transaction selected is out of range [0-{self.file.length_of_ind-1}]")

    @staticmethod
    def format_labels(label_lower):
        return [label.capitalize() for label in label_lower]

    @staticmethod
    def print_category_choice():
        print('Categories\nHousing, Transportation, Food\nUtilities, Entertainment, Income\nSubscriptions, Savings, Misc')

    @classmethod
    def select_category(cls):
        flag = ''
        while (flag != 'q'):
            try:
                category_name = input("Enter category Type: ").lower()
                cls.category_validation(category_name)
                if category_name in Category.categorys_selected:
                    break
                else:
                    cls.categorys_selected[category_name] = 0
                    flag = 'q'
            except ExpenseTracker.CustomError as e:
                print(e)
        return category_name

    @classmethod
    def category_validation(cls,category_name):
        category_options_lower = [string.lower() for string in cls.category_options]
        if category_name not in category_options_lower:
            raise ExpenseTracker.CustomError("No category with that name exist, enter name again: ")

    @classmethod
    def plot_pie_chart(cls, ax,month):
        if cls.categorys_selected:
            labels, amounts = zip(*cls.categorys_selected.items())
            labels = [label.capitalize() for label in labels]
            sizes = [abs(amount) for amount in amounts]
            total = sum(sizes)
            sizes = [abs(amount) / total * 100 for amount in amounts]
            ax.clear()
            ax.pie(sizes,labels=labels, autopct='%1.1f%%', )
            labels = [f'{type} {percentage:0.1f}%' for type, percentage in zip(labels,sizes)]
            ax.legend(labels, loc='center left', bbox_to_anchor=(-.3, 0.5))
            ax.set_title(f'Expenses {month}', fontsize=20)
            ax.figure.canvas.draw()
        else:
            ax.clear()
            ax.text(0.5, 0.5, "No data", horizontalalignment='center', verticalalignment='center')
            ax.figure.canvas.draw()








