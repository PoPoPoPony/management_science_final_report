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

	plt.xlabel("department")
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
		plt.pie([course_len_lst[i] - overlap_lst[i] - mis_course_len , mis_course_len - overlap_lst[i] , overlap_lst[i]] , 
		autopct = "%1.1f%%" , pctdistance = 0.6 , colors = ["green" , "orange" , "blue"] ,            
		textprops = {"fontsize" : 12})
		
	for i , j in enumerate([x for x in range(1 , 7) if x % 2 == 1]) : 
		plt.subplot(2 , 4 , j)
		plt.title("MIS and " + df.columns.to_list()[i] + " Course Overlap barplot")
		plt.bar("overlap" , df.iloc[1 , i])
		plt.bar("total course" , mis_course_len - df.iloc[1 , i] , label = "MIS Course")
		plt.bar("total course" , df.iloc[0 , i] - mis_course_len , bottom = mis_course_len - df.iloc[1 , i] , label = df.columns.to_list()[i] + " Course")
		plt.legend()

	plt.subplot(2 , 2 , 4)
	plt.title("Overlap Ratio Compare")
	for i in range(3) : 
		plt.bar(df.columns.to_list()[i] , ratio_lst[i] * 100)

	plt.show()
	
#def time_conflict_chart() : 












#time_conflict_chart()