import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def free_score_bar() : 
    mis_financial_free_score , mis_ie_free_score , mis_accounting_free_score = preprocessing.free_score()

    print(mis_financial_free_score)
    print(mis_ie_free_score)
    print(mis_accounting_free_score)

    score = pd.DataFrame([mis_financial_free_score , mis_ie_free_score , mis_accounting_free_score] , columns = ["free_score"])

    plt.figure(figsize = (100 , 80))
    plt.title(u"Free Score between mis and other departments" , fontsize = 32)

    sns.set(font_scale = 30)
    x = ["financial" , "ie" , "accounting"]
    #y1 = 


    sns.barplot(x = x , y = score["free_score"] , data = score)

    plt.xlabel("department")
    plt.text(-0.05 , 10 , score.iloc[0 , 0] , fontsize = 20)
    plt.text(0.70 , 11.5 , score.iloc[1 , 0] , fontsize = 20)
    plt.text(1.95 , 14.8 , score.iloc[2 , 0] , fontsize = 20)
    plt.show()


free_score_bar()