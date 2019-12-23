import pandas as pd
import os

def write_csv(df_lst) : 
    dpt_lst = ["Information Engineering" , "Finance and Banking" , "Accounting and Information Technology" , "Information Management"]

    for i in range(len(df_lst)) : 
        df_lst[i].to_csv(os.getcwd() + "/data/" + dpt_lst[i] + ".csv" , encoding = 'big5' , index = False)