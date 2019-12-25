import bs4
import os
import pandas as pd
import output


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

    remine_cols = ["Year Standing" , "Course ID" , "Course Title" , "Credit" , "Credit type" , "Day/Period" , "Remarks(Might contain Chinese due to course remarks which cannot be translated afterwards)"]
    for i in source_lst : 
        df = pd.read_html(i)
        df = df[0]
        df = df[remine_cols]
        df.columns = ["Year Standing" , "Course ID" , "Course Title" , "Credit" , "Credit type" , "Day/Period" , "Remarks"]
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

#將由其他系支援的課程併入原本的系所課表內
def hard_insert() : 
    path = os.getcwd()
    financial_df , mis_df , ie_df , accounting_df = read_file()
    
    source_lst_1 = []
    source_lst_2 = []

    #數學系
    with open(path + "/1081/2104_e.html" , 'r' , encoding = 'utf-8') as file :
        source_lst_1.append(file.read())

    with open(path + "/1082/2104_e.html" , 'r' , encoding = 'utf-8') as file :
        source_lst_2.append(file.read())

    #企管系
    with open(path + "/1081/5204_e.html" , 'r' , encoding = 'utf-8') as file :
        source_lst_1.append(file.read())

    with open(path + "/1082/5204_e.html" , 'r' , encoding = 'utf-8') as file :
        source_lst_2.append(file.read())

    #經濟系
    with open(path + "/1081/5104_e.html" , 'r' , encoding = 'utf-8') as file :
        source_lst_1.append(file.read())
    
    with open(path + "/1082/5104_e.html" , 'r' , encoding = 'utf-8') as file :
        source_lst_2.append(file.read())


    df_lst_1 = []
    df_lst_2 = []

    remine_cols = ["Year Standing" , "Course ID" , "Course Title" , "Credit" , "Credit type" , "Day/Period" , "Remarks(Might contain Chinese due to course remarks which cannot be translated afterwards)"]
    for i in source_lst_1 : 
        df = pd.read_html(i)
        df = df[0]
        df = df[remine_cols]
        df.columns = ["Year Standing" , "Course ID" , "Course Title" , "Credit" , "Credit type" , "Day/Period" , "Remarks"]
        df['semester'] = 1
        df_lst_1.append(df)

    for i in source_lst_2 : 
        df = pd.read_html(i)
        df = df[0]
        df = df[remine_cols]
        df.columns = ["Year Standing" , "Course ID" , "Course Title" , "Credit" , "Credit type" , "Day/Period" , "Remarks"]
        df['semester'] = 2
        df_lst_2.append(df)

    df_lst = concat(df_lst_1 , df_lst_2)

    math_df = df_lst[0]
    manage_df = df_lst[1]
    eco_df = df_lst[2]

    math_df.reset_index(inplace = True)
    manage_df.reset_index(inplace = True)
    eco_df.reset_index(inplace = True)

    #新增數學系支援的課程
    mis_insert_df = math_df.loc[math_df["Course Title"].str.contains("Calculus") & math_df["Remarks"].str.contains("Information Management")]
    ie_insert_df = math_df.loc[math_df["Course Title"].str.contains("Calculus") & math_df["Remarks"].str.contains("Computer Science")]
    financial_insert_df = math_df.loc[math_df["Course Title"].str.contains("Calculus") & math_df["Remarks"].str.contains("Finance and Banking")]
    accounting_insert_df = math_df.loc[math_df["Course Title"].str.contains("Calculus") & math_df["Remarks"].str.contains("Accounting and Information Technology")]


    #新增企管系支援的課程
    financial_insert_df = pd.concat([financial_insert_df , manage_df.loc[manage_df["Course Title"].str.contains("Introduction to Business") & manage_df["Remarks"].str.contains("Finance and Banking")]] , axis = 0 , ignore_index = True)
    accounting_insert_df = pd.concat([accounting_insert_df , manage_df.loc[manage_df["Course Title"].str.contains("Seminar on Humanistic and Business Ethics") & manage_df["Remarks"].str.contains("Accounting and Information Technology")]] , axis = 0 , ignore_index = True)
    mis_insert_df = pd.concat([mis_insert_df , manage_df.loc[manage_df["Course Title"].str.contains("Introduction to Business") & manage_df["Remarks"].str.contains("Information Management")]] , axis = 0 , ignore_index = True)
    mis_insert_df = pd.concat([mis_insert_df , manage_df.loc[manage_df["Course Title"].str.contains("Business Ethics") & manage_df["Remarks"].str.contains("Information Management")]] , axis = 0 , ignore_index = True)

    #新增經濟學系支援的課程
    financial_insert_df = pd.concat([financial_insert_df , eco_df.loc[eco_df["Course Title"].str.contains("Principle of Economics") & eco_df["Remarks"].str.contains("Finance and Banking")]] , axis = 0 , ignore_index = True)
    financial_insert_df = pd.concat([financial_insert_df , eco_df.loc[eco_df["Course Title"].str.contains("Microeconomics") & eco_df["Remarks"].str.contains("Finance and Banking")]] , axis = 0 , ignore_index = True)
    accounting_insert_df = pd.concat([accounting_insert_df , eco_df.loc[eco_df["Course Title"].str.contains("Principle of Economics") & eco_df["Remarks"].str.contains("Accounting and Information Technology")]] , axis = 0 , ignore_index = True)
    mis_insert_df = pd.concat([mis_insert_df , eco_df.loc[eco_df["Course Title"].str.contains("Principle of Economics") & eco_df["Remarks"].str.contains("Information Management")]] , axis = 0 , ignore_index = True)

    #新增資管系支援的課程
    accounting_insert_df = pd.concat([accounting_insert_df , mis_df.loc[mis_df["Course Title"].str.contains("Introduction to Computer") & mis_df["Remarks"].str.contains("Accounting and Information Technology")]] , axis = 0 , ignore_index = True)

    #新增財金系的支援課程
    accounting_insert_df = pd.concat([accounting_insert_df , financial_df.loc[financial_df["Course Title"].str.contains("Statistics") & financial_df["Remarks"].str.contains("Accounting and Information Technology")]] , axis = 0 , ignore_index = True)
    mis_insert_df = pd.concat([mis_insert_df , financial_df.loc[financial_df["Course Title"].str.contains("Statistics") & financial_df["Remarks"].str.contains("Information Management")]] , axis = 0 , ignore_index = True)
    
    #新增會資系支援的課程
    mis_insert_df = pd.concat([mis_insert_df , accounting_df.loc[accounting_df["Course Title"].str.contains("Accounting") & accounting_df["Remarks"].str.contains("Information Management")]] , axis = 0 , ignore_index = True)

    financial_insert_df.drop(['Remarks' , "index"] , axis = 1 , inplace = True)
    financial_df.drop("Remarks" , axis = 1 , inplace = True)
    financial_df = pd.concat([financial_df , financial_insert_df] , axis = 0 , ignore_index = True)

    mis_insert_df.drop(['Remarks' , 'index'] , axis = 1 , inplace = True)
    mis_df.drop("Remarks" , axis = 1 , inplace = True)
    mis_df = pd.concat([mis_df , mis_insert_df] , axis = 0 , ignore_index = True)
    
    ie_insert_df.drop(['Remarks' , 'index'] , axis = 1 , inplace = True)
    ie_df.drop("Remarks" , axis = 1 , inplace = True)
    ie_df = pd.concat([ie_df , ie_insert_df] , axis = 0 , ignore_index = True)

    accounting_insert_df.drop(['Remarks' , 'index'] , axis = 1 , inplace = True)

    #手動刪除會資系的 Principle of Economics(II)
    accounting_insert_df.drop(accounting_insert_df[accounting_insert_df["Course ID"] == 5101002].index , axis = 0 , inplace = True)
    accounting_df.drop("Remarks" , axis = 1 , inplace = True)
    accounting_df = pd.concat([accounting_df , accounting_insert_df] , axis = 0 , ignore_index = True ,  sort = True)

    #按照年級和學期排列
    financial_df.sort_values(by = ["Year Standing" , "semester"] , ascending = True , inplace = True)
    mis_df.sort_values(by = ["Year Standing" , "semester"] , ascending = True , inplace = True)
    ie_df.sort_values(by = ["Year Standing" , "semester"] , ascending = True , inplace = True)
    accounting_df.sort_values(by = ["Year Standing" , "semester"] , ascending = True , inplace = True)




    #對個別可以抵免的課程進行特殊處理
    #會資系的微積分先暫定變成微積分(微積分(一) -> 微積分) (取消)
    #會資系的統計學先暫定變成統計學(一) (方便比對)
    #accounting_df.loc[accounting_df["Course Title"] == "Calculus (I)" , "Course Title"] = "Calculus"
    
    accounting_df.loc[accounting_df["Course Title"] == "Statistics" , "Course Title"] = "Statistics (I)"

    new_df_lst = [ie_df , financial_df , accounting_df , mis_df]
    output.write_csv(new_df_lst)

#丟棄選修課，只留必修課，回傳課程df的list
def drop_elective() : 
    dpt_df_lst = read_file()
    for i in range(len(dpt_df_lst)) : 
        dpt_df_lst[i] = dpt_df_lst[i].loc[dpt_df_lst[i]["Credit type"] == "Required"]
    return dpt_df_lst

#讀取前面做好的csv，讀取順序 : 財金系 -> 資管系 -> 資工系 -> 會資系，回傳課程df的list
def read_file() : 
    path = os.getcwd()
    financial = pd.read_csv(path + "/data/Finance and Banking.csv" , encoding = "big5")
    mis = pd.read_csv(path + "/data/Information Management.csv" , encoding = "big5")
    ie = pd.read_csv(path + "/data/Information Engineering.csv" , encoding = "big5")
    accounting = pd.read_csv(path + "/data/Accounting and Information Technology.csv" , encoding = "big5")

    dpt_df_lst = [financial , mis , ie , accounting]

    return dpt_df_lst

#計算資管系與其他系所的課程重疊率
def course_overlap() : 
    dpt_df_lst = drop_elective()
    #dpt_name = ["financial" , "mis" , "ie" , "accounting"]
    course_lst = course_title_procedure(dpt_df_lst)

    
    for i in range(len(dpt_df_lst)) : 
        dpt_df_lst[i] = dpt_df_lst[i][['Course ID' , 'Course Title']]
        dpt_df_lst[i]['Course Title'] = course_lst[i]
        dpt_df_lst[i].drop_duplicates("Course ID", inplace = True)
        dpt_df_lst[i].drop_duplicates("Course Title", inplace = True)
        


    financial_course = dpt_df_lst[0]['Course Title'].to_list()
    mis_course = dpt_df_lst[1]['Course Title'].to_list()
    ie_course = dpt_df_lst[2]['Course Title'].to_list()
    accounting_course = dpt_df_lst[3]['Course Title'].to_list()

    mis_financial_overlap = 0
    mis_ie_overlap = 0
    mis_accounting_overlap = 0

    for i in mis_course : 
        if i in financial_course : 
            mis_financial_overlap += 1
        if i in ie_course : 
            mis_ie_overlap += 1
        if i in accounting_course : 
            mis_accounting_overlap += 1
    
    mis_financial_ratio = mis_financial_overlap / (len(mis_course) + len(financial_course) - mis_financial_overlap)
    mis_ie_ratio = mis_ie_overlap / (len(mis_course) + len(ie_course) - mis_ie_overlap)
    mis_accounting_ratio = mis_accounting_overlap / (len(mis_course) + len(accounting_course) - mis_accounting_overlap)

    print(mis_financial_ratio)
    print(mis_ie_ratio)
    print(mis_accounting_ratio)
    
    return mis_financial_ratio , mis_ie_ratio , mis_accounting_ratio
    

#處理課程名稱，將其盡量統一格式
def course_title_procedure(dpt_df_lst) : 
    course_lst = []

    for i in dpt_df_lst : 
        course_lst.append(i['Course Title'].to_list())

    #統一處理的部分
    for i in range(len(course_lst)) : 
        for j in range(len(course_lst[i])) : 
            course_lst[i][j] = course_lst[i][j].replace(" " , "")
            course_lst[i][j] = course_lst[i][j].lower()
            course_lst[i][j] = course_lst[i][j].replace("." , "")
            if "(programmingrelated)" in course_lst[i][j] : 
                course_lst[i][j] = course_lst[i][j][ : -20]
            if "(english-taught)" in course_lst[i][j] : 
                course_lst[i][j] = course_lst[i][j][ : -16]
            if "ⅱ" in course_lst[i][j] : 
                course_lst[i][j] = course_lst[i][j].replace("ⅱ" , "ii")
            if "（" in course_lst[i][j] : 
                course_lst[i][j] = course_lst[i][j].replace("（" , "(")
                course_lst[i][j] = course_lst[i][j].replace("）" , ")")
            if "&" in course_lst[i][j] : 
                course_lst[i][j] = course_lst[i][j].replace("&" , "and")

    return course_lst