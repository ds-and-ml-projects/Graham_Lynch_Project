# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk
from PIL import ImageTk, Image
import os.path, time, datetime
#import Draft_StockProject
#from Draft_StockProject import main
import sqlite3
import numpy as np
from Tkinter import *
import webbrowser
import requests
import pandas as pd


'''#### ADD:include popups for incorrect inputs, links of all the data so they can check it for themselves'''
basic = {
        "LARGE_Font": ("Cambria", 17),
        "MED_Font": ("Camrbia", 15),
        "SMALL_Font": ("Cambria", 13),
        "Nxt_bttn": "Next",
        "Rtv_bttn": "Retrieve",
        "StdColor": "#a1dbcd"
        }

last_modified = time.ctime(os.path.getmtime("stocks.db"))

R_Ttls = {
    'risk_totals_scores_2': [],
    'risk_totals_scores_4': [],
    'risk_totals_scores_5': [],
    'risk_totals_scores_6': [],
    'risk_totals_scores_7': [],
    'risk_totals_scores_8': [],
    'risk_totals_scores_9': []
}

Graham_Stocks = []
Lynch_Stocks = []
#------------------------------------------------------------------------------------------
# Class: Created the framework for every additional class
#------------------------------------------------------------------------------------------
class STOCK_GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        width = tk.Tk.winfo_screenwidth(self)
        height = tk.Tk.winfo_screenheight(self)
        gui_style = ttk.Style()
        gui_style.configure('My.TFrame', background='red')

        tk.Tk.title(self, "Stock Screener")
        tk.Tk.geometry(self, str(width/2) + "x" + str(height/2))

        # what the entire GUI will be placed within
        self.container = ttk.Frame(self, style="My.TFrame")
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.configure()

        self.frames= {}

        #------------------------------------------------------------------------------------------
        # The framework for every page, we aren't yet displaying it but only creating it
        #------------------------------------------------------------------------------------------

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive,
                        PageSix, PageSeven, PageEight, PageNine, PageTen, PageEleven):
            if (F != PageEleven): # Don't create Page 11, we first want the information on risk tolerance
                frame = F(self.container, self)

            self.frames[F] = frame # a dictionary: The Page Title is the value and the frame is the key
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage) # Will intialize the startpage

    #------------------------------------------------------------------------------------------
    # Function: Will display the page, once we hit to page 10, we move into the Check_Page function
    #------------------------------------------------------------------------------------------
    def show_frame(self, *args):
        current_pg = args[0]
        frame = self.frames[current_pg]
        frame.tkraise()
        if ((args[0]) == PageTen):
            self.Check_Page(args[0], args[1], args[2])

    #------------------------------------------------------------------------------------------
    # Function: Calcualtion of risk and will create page 11. We also call the info of the database that has's lower than
    #           the risk tolerance
    #------------------------------------------------------------------------------------------
    def Check_Page(self, current_page, container, parent):
        MeasuringRisk.Calculate_Risk()
        RETRIEVE_SQL.KEY_RATIOS() # We get the GRAHAM SCORES

        frame = PageEleven(self.container, parent)
        self.frames[PageEleven] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

#------------------------------------------------------------------------------------------
# Class: Two Functions: One gives each class a weighted value depedning on answers
#                       Other creates a list with all the values the user inputs
#------------------------------------------------------------------------------------------
class MeasuringRisk(object):
    """
    Risk_Tolerance: Used for


    """

    @classmethod
    def Risk_Tolerance(self, *args):
        num_of_questions = args[1] #  MeasuringRisk.Risk_Tolerance(var, 3, R_Ttls['risk_totals_scores_2']
        interval = args[1] - 1
        button_clicked = args[0]
        LIST_OF_CHOICES = args[2]

        risk_scale = np.linspace(0, 1, interval) # creating a numpy array that increments depending on the number of answers, EX: Starts from 0 until 1, with the interval
        for click_value in range(1, num_of_questions): # the get function provides answers from 1 to the number of questions
            if button_clicked.get() == click_value:
                print button_clicked.get()
                print click_value

                risk_score = risk_scale[click_value-1] # Because our list start from 0, we subract 1. Thus, if the user clicked on the second button, the point given to risk is the in position 0 of the list
                (LIST_OF_CHOICES.append(risk_score)) # append everything to the dict. to the specific list of the page

    @classmethod
    def Calculate_Risk(self): # This will get the last button that's being pressed. ADD ALL THE SCORES
        global total_score
        R_Agregate = 0.0 # The initial start is 0, we will keep adding all the choices

        # Will be adding all the choices from every single position
        for R_Scores in R_Ttls.iterkeys():
            try:
                R_Agregate = R_Agregate + R_Ttls[R_Scores][-1] # this is the last item in the list of each information in the page
            except IndexError:
                pass
        total_score = R_Agregate

#------------------------------------------------------------------------------------------
# Class from StartPage to PageEleven: Framworks to the specific class
#------------------------------------------------------------------------------------------
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def callback(event):
            webbrowser.open_new(r"http://www.google.com")
        tk.Frame.__init__(self, parent)
        tkvar = tk.StringVar()

        EntryPrompt = '''Please be as accurate as possible with the following questions\n
        This information is currently a a version of %r\n
        if we want a current database, click "Retrieve" ''' % (last_modified)

        label = tk.Label(self, text=EntryPrompt, font=basic["LARGE_Font"]).place(relx=0.1, rely=0.1)
        choices = { 'Retrieve','Additional information'}
        popupMenu = ttk.OptionMenu(self, tkvar, "Options", *choices).place(relx=0.1, rely=0.8)
        self.button0 = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageOne)).place(relx=0.8, rely=0.8)

        def change_dropdown(*args):
            if (tkvar.get() == 'Retrieve'):
                Popups.Retrieve()
            elif (tkvar.get() == 'Additional information'):
                Popups.Add_Info()

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        '''with open('RiskToleranceQs.txt', 'r') as Risk_File:
            page_per_question = Risk_File.readlines()
            list_of_questions.append(page_per_question)

        page_per_question = [x.strip() for x in page_per_question]

        '''
        questions = ["How old are you?","When do you expect to start drawing income?"]

        for i in range(len(questions)):
            label = tk.Label(self, text=questions[i], font=basic['LARGE_Font'], bg=basic['StdColor'])
            i = i * 2
            label.grid(row=i, column=1)
            entry = ttk.Entry(self).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageTwo)).place(relx=0.8, rely=0.8)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        var = tk.IntVar()
        tk.Frame.__init__(self, parent)

        question1 = '''Suppose that you bought a lottery ticket a week ago. You are now informed that\n
                            you have won and have been given two options of how to receive the money. Either...\n'''
        label1 = tk.Label(self, text=question1, font=basic['SMALL_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["A sure gain of $500", "A 50 percent chance to gain $1,000 and a 50 percent chance to gain nothing"]

        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1,
                        command=lambda: MeasuringRisk.Risk_Tolerance(var, 3, R_Ttls['risk_totals_scores_2'])).grid(row=i+1, column=1)


        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageThree)).place(relx=0.8, rely=0.8)

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        question = "Which of the following best characterizes your purpose to invest?"
        label = tk.Label(self, text=question, font=basic['LARGE_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["College", "Retirement", "Savings"]
        var = tk.IntVar()
        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageFour)).place(relx=0.8, rely=0.8)

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        var = tk.IntVar()
        tk.Frame.__init__(self, parent)

        question = '''Which of these statements would best describe your attitudes\n
                    about the next three months' performance of this investment?\n'''
        label = tk.Label(self, text=question, font=basic['LARGE_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["Who cares? One calendar quarter means nothing.", "I wouldn't worry about losses in that time frame",
                    "If I suffered a loss of greater than 10%, I'd get concerned", "I can only tolerate small short-term losses",
                    "I would have a hard time accepting any losses"]

        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1,
                            command=lambda: MeasuringRisk.Risk_Tolerance(var, 6, R_Ttls['risk_totals_scores_4'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageFive)).place(relx=0.8, rely=0.8)

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        question = '''Imagine that in the past three months, the overall stock market lost 25 percent of its value.\n
                    An individual stock investment you own also lost 25 percent of its value.\n
                    What would you do?\n'''
        label = tk.Label(self, text=question, font=basic['MED_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["Sell all of my shares", "Sell some of my shares", "Do nothing", "Buy more shares"]

        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1,
                            command=lambda: MeasuringRisk.Risk_Tolerance(var, 5, R_Ttls['risk_totals_scores_5'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageSix)).place(relx=0.8, rely=0.8)

class PageSix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        question = '''Suppose that you are about to retire, and have two choices for a pension:\n
        Pension A gives you an income equal to your pre- retirement income.\n
        Pension B has a 50 chance your income will be double your pre-retirement income, and a 50 percent\n
        chance that your income will be 20 percent less than your pre-retirement income.\n
        You will have no other source of income during retirement, no chance of employment,\n
        and no other family income ever in the future. All incomes are after tax. Which pension would you choose?\n'''
        label = tk.Label(self, text=question, font=basic['SMALL_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["Pension A", "Pension B"]
        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1,
                            command=lambda: MeasuringRisk.Risk_Tolerance(var, 3, R_Ttls['risk_totals_scores_6'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageSeven)).place(relx=0.8, rely=0.8)

class PageSeven(tk.Frame):
    def __init__(self, parent, controller):
        var = tk.IntVar()
        tk.Frame.__init__(self, parent)

        question = '''What percent of your funds are you willing to place in investments\n
                    that are of above average risk?\n'''
        label = tk.Label(self, text=question, font=basic['LARGE_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["0 percent", "1-9 percent", "10-19 percent", "20-29 percent", "30-39 percent",
                    "40-49 percent", "50-59 percent", "60-69 percent", "70-79 percent", "80-89 percent",
                    "90-99 percent"]
        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1,
                            command=lambda: MeasuringRisk.Risk_Tolerance(var, 12, R_Ttls['risk_totals_scores_7'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageEight)).place(relx=0.8, rely=0.8)

class PageEight(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        question = "What degree of risk have you assumed on your investments in the past?"
        label = tk.Label(self, text=question, font=basic['LARGE_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["1 = very small", "2 = small", "3 = medium", "4 = large", "5 = very large"]
        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1,
                            command=lambda: MeasuringRisk.Risk_Tolerance(var, 6, R_Ttls['risk_totals_scores_8'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageNine)).place(relx=0.8, rely=0.8)

class PageNine(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        question = '''Suppose that you violated a traffic rule and hurt somebody a week ago.\n
                    You are now informed that you will be fined and\n
                have been given two options of how to pay the fine\n'''
        label1 = tk.Label(self, text=question, font=basic['MED_Font'], bg=basic['StdColor']).grid(row=0, column=1)

        answers = ["A sure loss of $500", "A 50 percent chance to lose $1,000 and a 50 percent chance to lose nothing"]
        for i in range(len(answers)):
            checkbutton = tk.Radiobutton(self, text=answers[i], variable=var, value=i+1,
                            command=lambda: MeasuringRisk.Risk_Tolerance(var, 3, R_Ttls['risk_totals_scores_9'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageTen, parent, controller)).place(relx=0.8, rely=0.8)

class PageTen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(1, weight=1)
        prompt = '''GREAT YOU ARE DONE.\n
                    CLICK NEXT TO SEE WHAT STOCKS ARE APPROPRIATE\n
                    FOR YOU BASED ON YOUR RISK TOLERANCE\n'''
        label1 = tk.Label(self, text=prompt, font=basic['LARGE_Font'], bg=basic['StdColor']).grid(row=0, column=1)
        button = ttk.Button(self, text=basic['Nxt_bttn'], command=lambda: controller.show_frame(PageEleven)).place(relx=0.8, rely=0.8)

class PageEleven(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        df = pd.read_csv('secwiki_tickers.csv')

        listbox = tk.Listbox(self)
        listbox.pack(fill='y', side=LEFT)
        listbox.config(height=100, width=35)

        listbox2 = tk.Listbox(self)
        listbox2.pack(fill='y', side=RIGHT)
        listbox2.config(height=100, width=35)

        listbox.insert(END, "GRAHAM RECOMMENDATIONS")
        listbox2.insert(END, "LYNCH RECOMMENDATIONS")
        for Per_GrahamS in range(len(Graham_Stocks)):
            test = df[df.Ticker==Graham_Stocks[Per_GrahamS][0]]
            if not (test.empty):
                company_name = list(test.Name.values)[0]
                listbox.insert(END, company_name)

        for Per_LynchS in range(len(Lynch_Stocks)):
            test = df[df.Ticker==Lynch_Stocks[Per_LynchS][0]]
            if not (test.empty):
                company_name = list(test.Name.values)[0]
                listbox2.insert(END, company_name)

#------------------------------------------------------------------------------------------
# Class: We use the database that's already uploaded with the information from GRAHAM and LYNCH depedning on the total score
#------------------------------------------------------------------------------------------
class RETRIEVE_SQL(object):
    @classmethod
    def KEY_RATIOS(self):
        global Graham_Stocks
        global Lynch_Stocks

        sqlite_file = '/Users/alexguanga/All_Projects/Project_Stock/stocks.db'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute("SELECT STOCK FROM Stock_STAT WHERE %s < ? " % ("GrahamScore"), (total_score,))
        Graham_Stocks = c.fetchall()
        c.execute("SELECT STOCK FROM Stock_STAT WHERE %s < ? " % ("LynchScore"), (total_score,))
        Lynch_Stocks = c.fetchall()

        c.close()
        conn.close()

#------------------------------------------------------------------------------------------
# Class: We have informatin for the additional chpices the user clicks on the start page
#------------------------------------------------------------------------------------------
class Popups(object):
    @classmethod
    def Retrieve(self):

        def close_window():
            top.destroy()
        def new_database():
            Draft_StockProject.main()
            top.destroy()

        top = tk.Toplevel()
        top.title("About this application...")
        prompt = """
We will be updating information for over 2,500 stocks. This take approximately one hour
If you would like to continue, click 'Yes'
Sidenote: You can still continue with the current database in the meantime.
If you want to return, click 'No'
        """
        labellls = tk.Label(top, text=prompt, height=50, width=100).pack()
        Y_bttn = ttk.Button(top, text='Yes', command=new_database).place(relx=0.8, rely=0.8)
        N_bttn = ttk.Button(top, text='No', command=close_window).place(relx=0.1, rely=0.8)

    @classmethod
    def Add_Info(self):
        top = tk.Toplevel()
        top.title("About this application...")
        T = tk.Text(top, height=75, width=200)
        T.pack()
        '''with open('StockMetricFile.txt', 'r') as Stock_File:
            info_on_metrics_used = Stock_File.read()'''
        T.insert(END, info_on_metrics_used)

def main():
    gui = STOCK_GUI()
    gui.mainloop()

if __name__ == "__main__":
    main()
