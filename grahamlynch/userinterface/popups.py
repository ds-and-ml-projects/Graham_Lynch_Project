import Tkinter as tk
import ttk

from ..Storing_Stock_Statistics import StockInformation

init_prompt = """
We will be updating information for over 2,500 stocks. This take approximately one hour.
If you would like to continue, click 'Yes'.
Sidenote: You can still continue with the current database in the meantime.
If you want to return, click 'No'.
"""

def retrieve_db():
    '''
    Either destroys or creates an updated database of the stock metrics
    '''

    def close_window():
        db_window.destroy()

    def make_new_database():
        StockInformation()
        db_window.destroy()

    db_window = tk.Toplevel()
    db_window.title("About this application...")

    labels = tk.Label(db_window, text=init_prompt, height=50, width=100).pack()

    if_clicked_Y = ttk.Button(db_window, text='Yes', command=make_new_database).place(relx=0.8, rely=0.8)
    if_clicked_N = ttk.Button(db_window, text='No', command=close_window).place(relx=0.1, rely=0.8)

def info_on_metrics():
    metrics_window = tk.Toplevel()
    metrics_window.title("About this application...")

    text = tk.Text(metrics_window, height=75, width=200)
    text.pack()
    with open('StockMetricFile.txt', 'r') as stock_file:
        info_used = stock_file.read()
    text.insert(tk.END, info_used)
