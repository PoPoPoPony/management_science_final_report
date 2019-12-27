import preprocessing
import output
import web_clawer

#df_lst1 = preprocessing.get_table(preprocessing.get_source(1081) , 1)
#df_lst2 = preprocessing.get_table(preprocessing.get_source(1082) , 2)
#df_lst = preprocessing.concat_df_lst(df_lst1 , df_lst2)

#output.write_csv(df_lst)

#preprocessing.hard_insert()
#preprocessing.course_overlap()


#preprocessing.delicate_time_conflict()
#preprocessing.free_score()

options = web_clawer.driver_settings()
driver , home = web_clawer.CCU_login(options)
driver , dpt_page_url = web_clawer.CCU_get_dpt_page(driver , home)
web_clawer.CCU_get_mis_df(driver , dpt_page_url)

