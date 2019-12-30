import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def free_score_barplot() : 
    mis_financial_free_score , mis_ie_free_score , mis_accounting_free_score = preprocessing.free_score()

    print(mis_financial_free_score)
    print(mis_ie_free_score)
    print(mis_accounting_free_score)

    score = pd.DataFrame([mis_financial_free_score , mis_ie_free_score , mis_accounting_free_score] , columns = ["Y1" , "Y2" , "Y3" , "Y4"])
    score["dpt"] = ["financial" , "ie" , "accounting"]



    plt.figure(figsize = (100 , 80))
    plt.title(u"Free Score between mis and other departments" , fontsize = 32)

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
    

free_score_barplot()