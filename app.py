#Nixon & Laith
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ExpenseTracker
from Category import Category
from ExpenseTracker import ExpenseTrackerFile, CustomError
years = {2020 : 20,2021: 21,2022: 22,2023: 23,2024: 24,2025: 25}
months = {"January": 1, "February": 2, "March": 3, "April": 4, "June": 5, "July": 6, "August": 8, "September": 9 , "October": 10, "November": 11, "December": 12}
class ExpenseTrackerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Expense Tracker - Categorize and Visualize")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        screen_resolution = f"{window_width}x{window_height}"
        master.geometry(screen_resolution)

        #Initializing the backend
        self.expense_tracker = ExpenseTracker.ExpenseTrackerFile()

        #Creating main frames
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(pady=10)
        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(pady=10)

        #Setting up file loading
        self.load_button = tk.Button(self.top_frame, text="Load CSV File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.top_frame, text="Clear Current Data", command=self.reset_application)
        self.reset_button.pack(side=tk.LEFT)

        #Define date selection
        self.month_date = tk.Label(self.top_frame,text = "Select month")
        self.month_date.pack(side = tk.LEFT)
        self.combobox_date = ttk.Combobox(self.top_frame, values=list(months))
        self.combobox_date.pack(side=tk.LEFT)

        # Define year selection
        self.year_date = tk.Label(self.top_frame, text="Enter year")
        self.year_date.pack(side=tk.LEFT)
        self.combobox_year = ttk.Combobox(self.top_frame, values=list(years))
        self.combobox_year.pack(side=tk.LEFT)


        #Setting up the category selection and action buttons
        self.category_label = tk.Label(self.top_frame, text="Select Category:")
        self.category_label.pack(side=tk.LEFT)
        self.category_combobox = ttk.Combobox(self.top_frame, values=Category.category_options)
        self.category_combobox.pack(side=tk.LEFT)
        self.categorize_button = tk.Button(self.bottom_frame, text="Categorize Selected", command=self.categorize_transaction)
        self.categorize_button.pack(side=tk.BOTTOM)

        #Pie chart display button
        self.chart_button = tk.Button(self.bottom_frame, text="Show Pie Chart", command=self.plot_chart)
        self.chart_button.pack(side=tk.BOTTOM)

        #Plot area
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.sub_plot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.bottom_frame)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM)

        # Transaction list display
        plot_width, plot_height = self.sub_plot.get_figure().get_size_inches()
        plot_width_scaled = int(plot_width * 100)//10
        plot_height_scaled = int(plot_height * 100)//20

        #Status label
        self.status_label = tk.Label(master, text="Status: Ready")
        self.status_label.pack(side=tk.TOP)

    def auto_category_creation(self):
        file = self.expense_tracker.csv_file
        categories_dict = self.create_category_dictionary()
        for index, data in enumerate(self.expense_tracker.cat_trans_desc):
            category_name = data.lower()
            current_category = categories_dict[category_name]
            amount = self.expense_tracker.get_amt(index)
            if category_name in current_category.categorys_selected:
                current_category.categorys_selected[category_name] += amount
            else:
                current_category.categorys_selected[category_name] = amount
            current_category.add_bill_index(index)
            print(current_category.file)
            current_category.add_bill_amt(index)

    def create_category_dictionary(self):
        file = self.expense_tracker
        category_dict = {
            'income': Category(file, 'Income'),
            'housing': Category(file, 'Housing'),
            'transportation': Category(file, 'Transportation'),
            'food': Category(file, 'Food'),
            'utilities': Category(file, 'Utilities'),
            'entertainment': Category(file, 'Entertainment'),
            'subscriptions': Category(file, 'Subscriptions'),
            'savings': Category(file, 'Savings'),
            'misc': Category(file, 'Misc')
        }
        return category_dict

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.expense_tracker = ExpenseTrackerFile(file_path)
            self.expense_tracker.read_file_to_list()
            self.status_label.config(text="File loaded successfully.")

    def category_error(self,category_name):
        if category_name not in Category.categorys_selected and self.expense_tracker.length_of_ind > 0:
            if category_name == "":
                messagebox.showerror("No Category Error", "Must enter category")
                return False
            if category_name.isdigit():
                messagebox.showerror("Number Error", "Category is not a number")
                return False
            else:
                messagebox.showerror("Incorrect Category Error", "Incorrect category enter again")
                return False
        if self.expense_tracker.length_of_ind == 0 and category_name == "":
            messagebox.showerror("Null Data Error","Try again")
            return False
        if self.expense_tracker.length_of_ind == 0 and len(category_name) > 1:
            messagebox.showerror("Incorrect Category Error", "Incorrect category enter again")
            return False
        if self.expense_tracker.length_of_ind == 0 and category_name.isdigit():
            messagebox.showerror("Number Error", "Category is not a number")
            return False
        return True

    def categorize_transaction(self):
        category_name = self.category_combobox.get().lower()
        if(not self.category_error(category_name)):
            return
        selected_categories = []
        num_of_trans = self.expense_tracker.length_of_ind
        for i in range(num_of_trans):
            if self.expense_tracker.cat_trans_desc[i].lower() == category_name:
                trans = self.expense_tracker.print_trans(i)
                selected_categories.append(trans)
        if selected_categories:
            category_window = tk.Toplevel(self.master)
            category_window.title(f'Transaction of {category_name.capitalize()}')

            category_label = tk.Label(category_window, text="\n".join(selected_categories))
            category_label.pack()

            self.status_label.config(text=f"Transactions of {category_name} displayed.")
        else:
            self.status_label.config(text=f"No transactions found for {category_name}.")


    def plot_chart(self):
        try:
            month_str = self.combobox_date.get()
            month = months[month_str]
            year_int = int(self.combobox_year.get())
            year = years[year_int]
            self.expense_tracker.check_date_of_data(self.expense_tracker.data_list,month,year)
            self.auto_category_creation()
            Category.plot_pie_chart(self.sub_plot,month_str)  #Using the adapted method
            self.canvas.draw()  #Redrawing the canvas to show the updated plot
            self.status_label.config(text="Chart updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Failed to update chart.")


    def reset_application(self):
        #Clearing the category selections and their accumulated amounts
        Category.categorys_selected.clear()

        #Optional reset of the plot area if necessary
        self.sub_plot.clear()
        self.sub_plot.text(0.5, 0.5, 'No data', horizontalalignment='center', verticalalignment='center')
        self.canvas.draw()

        #Clearing any other GUI components or class attributes that store data
        if self.expense_tracker:
            self.expense_tracker.cat_trans_date.clear()
            self.expense_tracker.cat_trans_amt.clear()
            self.expense_tracker.cat_trans_type.clear()
            self.expense_tracker.cat_trans_desc.clear()

        #Updating status label
        self.status_label.config(text="Ready to load a new file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)

    root.mainloop()
