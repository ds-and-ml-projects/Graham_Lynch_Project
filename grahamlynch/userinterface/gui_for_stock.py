# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk
import sqlite3
import numpy as np
import webbrowser
import requests
import pandas as pd

from .typical_features import dict_features
from .typical_features import dict_bttns
from .typical_features import dict_answ_choices
from .typical_features import dict_questions

from .generated_stock_picks import key_ratios

from .popups import retrieve_db
from .popups import info_on_metrics

list_of_recommend_graham = []
list_of_recommend_lynch = []

risk_tol_per_qs = {
    'risk_pg_2': [],
    'risk_pg_4': [],
    'risk_pg_5': [],
    'risk_pg_6': [],
    'risk_pg_7': [],
    'risk_pg_8': [],
    'risk_pg_9': []
}

class interface_template(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        width = tk.Tk.winfo_screenwidth(self)
        height = tk.Tk.winfo_screenheight(self)
        gui_style = ttk.Style()
        gui_style.configure('My.TFrame', background='red')

        tk.Tk.title(self, "Stock Screener")
        tk.Tk.geometry(self, str(width/2) + "x" + str(height/2))

        self.container = ttk.Frame(self, style="My.TFrame")
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.configure()

        self.frames= {}

        # Creating the framework all the pages. Not using it yet.
        for Page in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive,
                    PageSix, PageSeven, PageEight, PageNine, PageTen, PageEleven):

            if (Page != PageEleven): # Don't create Page 11, we first want the information on risk tolerance
                frame = Page(self.container, self)

            self.frames[Page] = frame # a dictionary: The Page Title is the value and the frame is the key
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage) # Will intialize the startpage

    def show_frame(self, *args):
        """
        The template for each page will be shown once the next button is clicked. Once we reach page 10,
        all computatios are calculated
        """
        current_pg = args[0]
        frame = self.frames[current_pg]
        frame.tkraise()

        if current_pg == PageTen:
            graham_picks, lynch_picks = Complete_Interface.completing_evalution()
            self.last_pg_results(graham_picks, lynch_picks, *args)

    def last_pg_results(self, graham_picks, lynch_picks, *args):
        """
        Creates the last page, with all the calculations completed
        """
        crrnt_pg, container, parent = args

        frame = PageEleven(self.container, parent, graham_picks, lynch_picks)
        self.frames[PageEleven] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        tkvar = tk.StringVar()

        label = tk.Label(self, text=dict_questions["question_pstart"], font=dict_features["large_font"]).place(relx=0.1, rely=0.1)
        popupMenu = ttk.OptionMenu(self, tkvar, "Options", *dict_answ_choices["choice_startpg"]).place(relx=0.1, rely=0.8)
        self.button0 = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageOne)).place(relx=0.8, rely=0.8)

        def change_dropdown(*args):
            if (tkvar.get() == 'Retrieve'):
                retrieve_db()
            elif (tkvar.get() == 'Additional information'):
                info_on_metrics()

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttl_qs = dict_questions['question_p1']

        for i in range(len(ttl_qs)):
            label = tk.Label(self, text=ttl_qs[i], font=dict_features["large_font"], bg=dict_features['std_color'])
            i = i * 2
            label.grid(row=i, column=1)
            entry = ttk.Entry(self).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageTwo)).place(relx=0.8, rely=0.8)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        var = tk.IntVar()
        tk.Frame.__init__(self, parent)

        ttl_qs = dict_questions['question_p2']
        ttl_ans = dict_answ_choices['choice_pg2']

        label1 = tk.Label(self, text=ttl_qs, font=dict_features["small_font"], bg=dict_features['std_color']).grid(row=0, column=1)

        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1,
                            command=lambda: Complete_Interface.per_risk_tol(var, 3, risk_tol_per_qs['risk_pg_2'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageThree)).place(relx=0.8, rely=0.8)

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        ttl_qs = dict_questions['question_p3']
        ttl_ans = dict_answ_choices['choice_pg3']

        label = tk.Label(self, text=ttl_qs, font=dict_features['large_font'], bg=dict_features['std_color']).grid(row=0, column=1)

        var = tk.IntVar()
        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageFour)).place(relx=0.8, rely=0.8)

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        var = tk.IntVar()
        tk.Frame.__init__(self, parent)

        ttl_qs = dict_questions['question_p4']
        ttl_ans = dict_answ_choices['choice_pg4']

        label = tk.Label(self, text=ttl_qs, font=dict_features['large_font'], bg=dict_features['std_color']).grid(row=0, column=1)

        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1,
                            command=lambda: Complete_Interface.per_risk_tol(var, 6, risk_tol_per_qs['risk_pg_4'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageFive)).place(relx=0.8, rely=0.8)

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        ttl_qs = dict_questions['question_p5']
        ttl_ans = dict_answ_choices['choice_pg5']

        label = tk.Label(self, text=ttl_qs, font=dict_features['medium_font'], bg=dict_features['std_color']).grid(row=0, column=1)

        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1,
                            command=lambda: Complete_Interface.per_risk_tol(var, 5, risk_tol_per_qs['risk_pg_5'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageSix)).place(relx=0.8, rely=0.8)

class PageSix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        ttl_qs = dict_questions['question_p6']
        ttl_ans = dict_answ_choices['choice_pg6']

        label = tk.Label(self, text=ttl_qs, font=dict_features['small_font'], bg=dict_features['std_color']).grid(row=0, column=1)

        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1,
                            command=lambda: Complete_Interface.per_risk_tol(var, 3, risk_tol_per_qs['risk_pg_6'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageSeven)).place(relx=0.8, rely=0.8)

class PageSeven(tk.Frame):
    def __init__(self, parent, controller):
        var = tk.IntVar()
        tk.Frame.__init__(self, parent)

        ttl_qs = dict_questions['question_p7']
        ttl_ans = dict_answ_choices['choice_pg7']

        label = tk.Label(self, text=ttl_qs, font=dict_features['large_font'], bg=dict_features['std_color']).grid(row=0, column=1)

        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1,
                            command=lambda: Complete_Interface.per_risk_tol(var, 12, risk_tol_per_qs['risk_pg_7'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageEight)).place(relx=0.8, rely=0.8)

class PageEight(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        ttl_qs = dict_questions['question_p8']
        ttl_ans = dict_answ_choices['choice_pg8']

        label = tk.Label(self, text=ttl_qs, font=dict_features['large_font'], bg=dict_features['std_color']).grid(row=0, column=1)

        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1,
                            command=lambda: Complete_Interface.per_risk_tol(var, 6, risk_tol_per_qs['risk_pg_8'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageNine)).place(relx=0.8, rely=0.8)

class PageNine(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        var = tk.IntVar()

        ttl_qs = dict_questions['question_p9']
        ttl_ans = dict_answ_choices['choice_pg9']

        label = tk.Label(self, text=ttl_qs, font=dict_features['medium_font'], bg=dict_features['std_color']).grid(row=0, column=1)

        for i in range(len(ttl_ans)):
            checkbutton = tk.Radiobutton(self, text=ttl_ans[i], variable=var, value=i+1,
                            command=lambda: Complete_Interface.per_risk_tol(var, 3, risk_tol_per_qs['risk_pg_9'])).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageTen, parent, controller)).place(relx=0.8, rely=0.8)

class PageTen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(1, weight=1)

        prompt = dict_questions['question_p10']

        label1 = tk.Label(self, text=prompt, font=dict_features['medium_font'], bg=dict_features['std_color']).grid(row=0, column=1)
        button = ttk.Button(self, text=dict_bttns['next_bttn'], command=lambda: controller.show_frame(PageEleven)).place(relx=0.8, rely=0.8)

class PageEleven(tk.Frame):
    def __init__(self, parent, controller, graham_picks, lynch_picks):
        tk.Frame.__init__(self, parent)
        df = pd.read_csv('secwiki_tickers.csv')

        listbox = tk.Listbox(self)
        listbox.pack(fill='y', side=tk.LEFT)
        listbox.config(height=100, width=35)

        listbox2 = tk.Listbox(self)
        listbox2.pack(fill='y', side=tk.RIGHT)
        listbox2.config(height=100, width=35)

        listbox.insert(tk.END, "GRAHAM RECOMMENDATIONS")
        listbox2.insert(tk.END, "LYNCH RECOMMENDATIONS")

        Complete_Interface.display_final_results(graham_picks, listbox, df)
        Complete_Interface.display_final_results(lynch_picks, listbox2, df)

class Complete_Interface:
    @classmethod
    def completing_evalution(self, *args):
        """
        After risk tolerance is figured out, will return the values from the database from each investors
        that are lower than the risk tolerance
        """
        self.calculate_risk_tol(*args)
        graham_picks = key_ratios("GrahamScore", total_score)
        lynch_picks = key_ratios("LynchScore", total_score)
        return (graham_picks, lynch_picks)

    @classmethod
    def per_risk_tol(*args):
        """
        Because some buttons can be clicked, to assure that the risk tolerance is done to the last item
        clicked, this function makes sure that the risk of each page is done, is on the last button clicked
        """
        num_of_qs_plus_1 = args[2]
        interval_btw_ttl_qs = args[2] - 1
        button_click = args[1]
        dict_temp_risk = args[3]
        risk_tol_scale = np.linspace(0, 1, interval_btw_ttl_qs)

        for possible_ans in range(1, num_of_qs_plus_1):
            if button_click.get() == possible_ans:
                risk_score = risk_tol_scale[possible_ans-1] # Because our list start from 0, we subract 1. Thus, if the user clicked on the second button, the point given to risk is the in position 0 of the list
                dict_temp_risk.append(risk_score) # append everything to the dict. to the specific list of the page

    @classmethod
    def calculate_risk_tol(*args):
        """
        Adds all the risk tolerance of each page
        """
        global total_score
        risk_tol_start = 0.0

        for risk_per_pg in risk_tol_per_qs.iterkeys():
            try:
                risk_tol_start = risk_tol_start + risk_tol_per_qs[risk_per_pg][-1] # this is the last item in the list of each information in the page
            except IndexError:
                pass
        total_score = risk_tol_start

    @classmethod
    def display_final_results(*args):
        """
        Using an Excel sheet with ticker, will display the result of each company by its name
        """
        class_interface, investor_picks, listbox, tckr_file = args

        for each_pick in range(len(investor_picks)):
            test = tckr_file[tckr_file.Ticker==investor_picks[each_pick][0]]
            if not (test.empty):
                company_name = list(test.Name.values)[0]
                listbox.insert(tk.END, company_name)
