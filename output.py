import pandas as pd
import os

def write_csv(df_lst) : 
	dpt_lst = ["Information Engineering" , "Finance and Banking" , "Accounting and Information Technology" , "Information Management"]

	for i in range(len(df_lst)) : 
		df_lst[i].to_csv(os.getcwd() + "/data/" + dpt_lst[i] + ".csv" , encoding = 'big5' , index = False)

def write_time_conflict_csv(df_lst) : 
	dpt_lst = ["Finance and Banking" , "Information Management" , "Information Engineering" , "Accounting and Information Technology"]
	for i in range(len(dpt_lst)) : 
		dpt_lst[i] += " time conflict"
		df_lst[i].to_csv(os.getcwd() + "/data/" + dpt_lst[i] + ".csv" , encoding = 'big5' , index = False)