import logging
import os
import re
import time
import pandas as pd
import streamlit as st
import base64
import psutil





inf_tuples = ('pm_cloud','pm_fog','pm_wan_up','pm_wan_down','pm_wifi')
app_tuples = ('pm_v2i','pm_cctv')

def read_logs_update_chart_test():
    fo = open("logfile.log", "rb") # 'rb for bites'
    line = fo.readline()
    for line in fo.readlines():
        logs = str(line.decode())
        if logs[0].isdigit():
            temp_list = logs.split(": ")
            pattern = re.compile(r'[\d.\d]{1,}')
            power_sum = pattern.findall(temp_list[2])
            power = float(power_sum[0]) + float(power_sum[1])
            element = []
            element.append(power)
            columns = temp_list[1]
            i = temp_list[0]
            df = pd.DataFrame(element,index=[i],columns=[columns])
            # if '' in df.columns:
            #     print('drop')
            #     df.drop(columns='')
            df.index = df.index.map(str)
            df.index = df.index.astype('float64')
            
            st.session_state.inf_chart.add_rows(df)
            time.sleep(0.1)
            # if str(temp_list[1]) in inf_tuples:
            #     st.session_state.inf_chart.add_rows(df)
            # if str(temp_list[1]) in app_tuples:
            #     st.session_state.app_chart.add_rows(df)
        else:
            continue
    loading('static/loading.gif')


def loading(path):
    if st.session_state.loading == False:
        st.session_state['loading'] = True
        file_ = open(path, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.session_state['loadinggif'] = st.markdown(f'<div style="text-align: center"> <img src="data:image/gif;base64,{data_url}" alt="loading gif"> </div>',unsafe_allow_html=True,)
    elif st.session_state.loading == True:
        st.session_state['loading'] = False
        st.session_state['loadinggif'].empty()


def storeStrintoPy(string,filename):
    copy_to_py = open(filename, 'w')
    copy_to_py.write(string)
    copy_to_py.close()
    fo = open(filename, "rb") # 'rb for bites'
    line = fo.readline()
    for line in fo.readlines():
        logs = str(line.decode())
        logs = logs.lstrip()
        if logs == 'if measure_infrastructure:':
            print(logs)
        
        # else:
        #     continue



    # os.system('python %s'%filename)




    