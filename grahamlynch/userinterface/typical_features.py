import sys, time, datetime

"""
The following are some features that will be typically used throughout the GUI interface
"""
#db_time_modify = time.ctime(os.path.getmtime("stocks.db"))

dict_features = {
        "large_font": ("Cambria", 17),
        "medium_font": ("Camrbia", 15),
        "small_font": ("Cambria", 13),
        "std_color": "#a1dbcd"
}

dict_bttns = {
        "next_bttn": "Next",
        "retrieve_bttn": "Retrieve"
}


dict_answ_choices = {
    "choice_startpg": ["Retrieve","Additional information"],

    "choice_pg2": ["A sure gain of $500", "A 50 percent chance to gain $1,000 and a 50 percent chance to gain nothing"],

    "choice_pg3": ["College", "Retirement", "Savings"],

    "choice_pg4": ["I would have a hard time accepting any losses.", "I wouldn't worry about losses in that time frame",
                    "If I suffered a loss of greater than 10%, I'd get concerned", "I can only tolerate small short-term losses",
                    "Who cares? One calendar quarter means nothing."],

    "choice_pg5": ["Sell all of my shares", "Sell some of my shares", "Do nothing", "Buy more shares"],

    "choice_pg6": ["Pension A", "Pension B"],

    "choice_pg7": ["0 percent", "1-9 percent", "10-19 percent", "20-29 percent", "30-39 percent", "40-49 percent",
                    "50-59 percent", "60-69 percent", "70-79 percent", "80-89 percent", "90-99 percent"],

    "choice_pg8": ["1 = very small", "2 = small", "3 = medium", "4 = large", "5 = very large"],

    "choice_pg9": ["A sure loss of $500", "A 50 percent chance to lose $1,000 and a 50 percent chance to lose nothing"]


}


dict_questions = {
    "question_pstart": '''Please be as accurate as possible with the following questions.\n
                        \bIf you want a current database, click "Retrieve"\n''',

    "question_p1": ["How old are you?","When do you expect to start drawing income?"],

    "question_p2": '''Suppose that you bought a lottery ticket a week ago. You are now informed that\n
                    you have won and have been given two options of how to receive the money. Either...\n''',

    "question_p3": "Which of the following best characterizes your purpose to invest?",

    "question_p4": '''Which of these statements would best describe your attitudes\n
                    about the next three months' performance of this investment?\n''',

    "question_p5": '''Imagine that in the past three months, the overall stock market lost 25 percent of its value.\n
                    An individual stock investment you own also lost 25 percent of its value.\n
                    What would you do?\n''',

    "question_p6": '''Suppose that you are about to retire, and have two choices for a pension:\n
                    Pension A gives you an income equal to your pre-retirement income.\n
                    Pension B has a 50 chance your income will be double your pre-retirement income, and a 50 percent\n
                    chance that your income will be 20 percent less than your pre-retirement income.\n
                    You will have no other source of income during retirement, no chance of employment,\n
                    and no other family income ever in the future. All incomes are after tax. Which pension would you choose?\n''',

    "question_p7":  '''What percent of your funds are you willing to place in investments\n
                    that are of above average risk?\n''',

    "question_p8": "What degree of risk have you assumed on your investments in the past?",

    "question_p9": '''Suppose that you violated a traffic rule and hurt somebody a week ago.\n
                    You are now informed that you will be fined and\n
                    have been given two options of how to pay the fine\n''',

    "question_p10": '''GREAT YOU ARE DONE.\n
                    CLICK NEXT TO SEE WHAT STOCKS ARE APPROPRIATE\n
                    FOR YOU BASED ON YOUR RISK TOLERANCE\n'''

}
