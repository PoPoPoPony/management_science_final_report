import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def free_score_barplot() : 
	mis_financial_free_score , mis_ie_free_score , mis_accounting_free_score , free_score_lst = preprocessing.free_score()

	print(mis_financial_free_score)
	print(mis_ie_free_score)
	print(mis_accounting_free_score)

	score = pd.DataFrame([mis_financial_free_score , mis_ie_free_score , mis_accounting_free_score] , columns = ["Y1" , "Y2" , "Y3" , "Y4"])
	score["dpt"] = ["financial" , "ie" , "accounting"]

	plt.figure(figsize = (100 , 80))
	plt.title(u"Free Score between MIS and other departments" , fontsize = 32)

	print(score)

	plt.bar(score["dpt"] , score["Y1"] , data = score , label = "Yl")
	plt.bar(score["dpt"] , score["Y2"] , bottom = score["Y1"] , data = score , label = "Y2")
	plt.bar(score["dpt"] , score["Y3"] , bottom = score["Y1"] + score["Y2"] , data = score , label = "Y3")
	plt.bar(score["dpt"] , score["Y4"] , bottom = score["Y1"] + score["Y2"] + score["Y3"] , data = score , label = "Y4")

	plt.xlabel("department" , fontsize = 25)
	plt.ylabel("Free Score" , fontsize = 25)
	plt.xticks(fontsize = 25)
	plt.yticks(fontsize = 25)
	plt.text(-0.05 , 9.9 , sum(mis_financial_free_score) , fontsize = 20)
	plt.text(0.78 , 11.4 , sum(mis_ie_free_score) , fontsize = 20)
	plt.text(1.92 , 14.9 , sum(mis_accounting_free_score) , fontsize = 20)
	plt.legend()
	plt.show()

def course_overlap_chart() : 
	course_len_lst , overlap_lst , ratio_lst , mis_course_len = preprocessing.course_overlap()

	df = pd.DataFrame([course_len_lst , overlap_lst , ratio_lst] , columns = ["financial" , "ie" , "accounting"])

	plt.figure(figsize = (100 , 80))
	plt.title(u"Course Overlap Score between MIS and other departments" , fontsize = 32)

	for i , j in enumerate([x for x in range(1 , 7) if x % 2 == 0]) : 
		plt.subplot(2 , 4 , j)
		plt.title("MIS and " + df.columns.to_list()[i] + " Course Overlap piechart")
		plt.pie([course_len_lst[i] - mis_course_len , mis_course_len - overlap_lst[i] , overlap_lst[i]] , 
		autopct = "%1.1f%%" , pctdistance = 0.6 , colors = ["green" , "orange" , "blue"] ,            
		textprops = {"fontsize" : 12} , labels = [df.columns.to_list()[i] + " Course(%)" , "MIS Course(%)" , "overlap Course(%)"])
		
	for i , j in enumerate([x for x in range(1 , 7) if x % 2 == 1]) : 
		plt.subplot(2 , 4 , j)
		plt.title("MIS and " + df.columns.to_list()[i] + " Course Overlap barplot")
		plt.bar("overlap" , df.iloc[1 , i])
		plt.bar("total course" , mis_course_len - df.iloc[1 , i] , label = "MIS Course")
		plt.bar("total course" , df.iloc[0 , i] - mis_course_len , bottom = mis_course_len - df.iloc[1 , i] , label = df.columns.to_list()[i] + " Course")
		plt.xlabel("department" , fontsize = 15)
		plt.ylabel("amount of course" , fontsize = 15)
		plt.xticks(fontsize = 15)
		plt.yticks(fontsize = 15)
		plt.legend()

	plt.subplot(2 , 2 , 4)
	plt.title("Overlap Ratio Compare")
	for i in range(3) : 
		plt.bar(df.columns.to_list()[i] , ratio_lst[i] * 100)
	
	plt.xlabel("department" , fontsize = 15)
	plt.xticks(fontsize = 15)
	plt.show()
	
def time_conflict_chart() : 
	mis_financial_time_conflict , mis_ie_time_conflict , mis_accounting_time_conflict , time_conflict_lst = preprocessing.delicate_time_conflict()

	df = pd.DataFrame([mis_financial_time_conflict , mis_ie_time_conflict , mis_accounting_time_conflict] , columns = ["Y1" , "Y2" , "Y3" , "Y4"])
	df["dpt"] = ["financial" , "ie" , "accounting"]

	print(df)
	for i in time_conflict_lst : 
		print(i)

	plt.figure(figsize = (100 , 80))
	plt.title(u"Course Overlap Score between MIS and other departments" , fontsize = 32)

	for i in range(1 , 4) : 
		plt.subplot(2 , 2 , i)
		plt.title("MIS and " + df['dpt'].to_list()[i - 1] + " Time Conflict piechart" , fontsize = 20)
		plt.pie([len(time_conflict_lst[i - 1]) - sum(df.iloc[i - 1 , 0 : 4].to_list()) , sum(df.iloc[i - 1 , 0 : 4].to_list())] , 
		autopct = "%1.1f%%" , pctdistance = 0.6 , colors = ["blue" , "orange"] ,            
		textprops = {"fontsize" : 15} , labels = ["unConflicted Course(%)" , "Conflicted Course(%)"])

	plt.subplot(2 , 2 , 4)
	plt.title("Compare Time Conflict")
	plt.bar(df["dpt"] , df["Y1"] , label = "Yl")
	plt.bar(df["dpt"] , df["Y2"] , bottom = df["Y1"] , label = "Y2")
	plt.bar(df["dpt"] , df["Y3"] , bottom = df["Y1"] + df["Y2"] , label = "Y3")
	plt.bar(df["dpt"] , df["Y4"] , bottom = df["Y1"] + df["Y2"] + df["Y3"] , label = "Y4")

	plt.xlabel("department" , fontsize = 15)
	plt.ylabel("Time Conflict" , fontsize = 15)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 15)
	
	plt.text(-0.05 , 13.5 , sum(mis_financial_time_conflict) , fontsize = 20)
	plt.text(0.93 , 11.4 , sum(mis_ie_time_conflict) , fontsize = 20)
	plt.text(1.95 , 10.2 , sum(mis_accounting_time_conflict) , fontsize = 20)
	plt.legend()
	plt.show()
	
def final_score_chart() : 
	financial_final_score , ie_final_score , accounting_final_score = preprocessing.final_score()

	print(financial_final_score)

	df = pd.DataFrame([financial_final_score , ie_final_score , accounting_final_score] , columns = ["Overlap Score" , "Time Conflict Score" , "Free Score"])
	df['dpt'] = ["financial" , "ie" , "accounting"]

	plt.figure(figsize = (100 , 80))
	plt.title(u"Final Score between MIS and other departments" , fontsize = 32)

	plt.bar(df["dpt"] , df["Overlap Score"] , label = "Overlap Score")
	plt.bar(df["dpt"] , df["Time Conflict Score"] , bottom = df["Overlap Score"] , label = "Time Conflict Score")
	plt.bar(df["dpt"] , df["Free Score"] , bottom = df["Overlap Score"] + df["Time Conflict Score"] , label = "Free Score")

	plt.ylim((0 , 75))
	plt.xlabel("department" , fontsize = 25)
	plt.ylabel("Final Score" , fontsize = 25)
	plt.xticks(fontsize = 25)
	plt.yticks(fontsize = 25)

	
	plt.text(-0.2 , 67.5 , sum(financial_final_score) , fontsize = 20)
	plt.text(0.78 , 20.7 , sum(ie_final_score) , fontsize = 20)
	plt.text(1.815 , 60 , sum(accounting_final_score) , fontsize = 20)
		
	plt.legend()
	plt.show()
	



free_score_barplot()
course_overlap_chart()
time_conflict_chart()
final_score_chart()