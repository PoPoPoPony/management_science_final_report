import bs4
import os
import pandas as pd


def get_source(semester) : 
    semester = str(semester)
    path = os.getcwd() + "/" + semester + "/"
    dir = os.listdir(path)
    source_lst = []
    dpt_lst = ["Information Engineering" , "Finance and Banking" , "Accounting and Information Technology" , "Information Management"]
    for i in dir : 
        if "_e"  in i : 
            with open(path + "/" + i , 'r' , encoding = 'utf-8') as file :
                source = file.read()
                soup = bs4.BeautifulSoup(source , 'html.parser')
                title = soup.select_one("head > title")
                
                for j in dpt_lst : 
                    if j in title.string and "Department" in title.string : 
                        source_lst.append(source)
            
    return source_lst



# 順序 : 資工、財金、會資、資管

def get_table(source_lst , semester) :
    
    df_lst = []

    remine_cols = ["Year Standing" , "Course Title" , "Credit" , "Credit type" , "Day/Period"]
    for i in source_lst : 
        df = pd.read_html(i)
        df = df[0]
        df = df[remine_cols]
        df['semester'] = semester
        df_lst.append(df)

    return df_lst


def concat(df_lst1 , df_lst2) : 
    df_lst = []
    for i in range(len(df_lst1)) : 
        df = pd.concat([df_lst1[i] , df_lst2[i]] , axis = 0)
        df.reset_index()
        df_lst.append(df)

    return df_lst

def read_file() : 
    path = os.getcwd()
    financial = pd.read_csv(path + "/data/Finance and Banking.csv" , encoding = "big5")
    mis = pd.read_csv(path + "/data/Information Management.csv" , encoding = "big5")
    ie = pd.read_csv(path + "/data/Information Engineering.csv" , encoding = "big5")
    accounting = pd.read_csv(path + "/data/Accounting and Information Technology.csv" , encoding = "big5")

    return financial , mis , ie , accounting

def course_overlap() : 
    dpt_df = list(read_file())
    dpt_name = ["financial" , "mis" , "ie" , "accounting"]
    
    for i in dpt_df : 
        i.drop_duplicates("Course Title", inplace = True)
        print(i)
        print()

    financail_course = dpt_df[0]['Course Title'].to_list()
    mis_course = dpt_df[1]['Course Title'].to_list()
    ie_course = dpt_df[2]['Course Title'].to_list()
    accounting_course = dpt_df[3]['Course Title'].to_list()

    mis_financial_overlap = 0
    mis_ie_overlap = 0
    mis_accounting_overlap = 0

    for i in mis_course : 
        if i in financail_course : 
            mis_financial_overlap += 1
        if i in ie_course : 
            mis_ie_overlap += 1
        if i in accounting_course : 
            mis_accounting_overlap += 1
    
    mis_financial_ratio = mis_financial_overlap / (len(mis_course) + len(financail_course) - mis_financial_overlap)
    mis_ie_ratio = mis_ie_overlap / (len(mis_course) + len(ie_course) - mis_ie_overlap)
    mis_accounting_ratio = mis_accounting_overlap / (len(mis_course) + len(accounting_course) - mis_accounting_overlap)

    print(mis_financial_overlap)
    print(mis_ie_overlap)
    print(mis_accounting_overlap)


    print(mis_financial_ratio)
    print(mis_ie_ratio)
    print(mis_accounting_ratio)
    
    return mis_financial_ratio , mis_ie_ratio , mis_accounting_ratio
    

