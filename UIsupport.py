import logging
import os
import re
import time
import pandas as pd
import streamlit as st
import base64
import psutil




def testing():
    print('into  test')
    loading('static/loading.gif')
    




def read_logs_update_chart_test():
    fo = open("logfile.log", "rb") # 'rb for bites'
    line = fo.readline()
    for line in fo.readlines():
        logs = str(line.decode())
        if logs[0].isdigit():
            temp_list = logs.split(":")
            pattern = re.compile(r'[\d.\d]{1,}')
            power_sum = pattern.findall(temp_list[2])
            power = float(power_sum[0]) + float(power_sum[1])
            element = []
            element.append(power)
            columns = temp_list[1]
            i = temp_list[0]
            df = pd.DataFrame(element,index=[i],columns=[columns])
            if '' in df.columns:
                print('drop')
                df.drop(columns='')
            df.index = df.index.map(str)
            df.index = df.index.astype('float64')
            st.session_state.inf_chart.add_rows(df)
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
        print('loading false')


def storeStrintoPy(str,filename):
    copy_to_py = open(filename, 'w')
    copy_to_py.write(str)
    copy_to_py.close()
    os.system('python %s'%filename)

def is_process_running(process_name):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == process_name:
            return True
    else:
        return False


    