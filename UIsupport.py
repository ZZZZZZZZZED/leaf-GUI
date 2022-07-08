import logging
import os
import re
import time
import pandas as pd
import streamlit as st


def testing():
    print('into  test')
    print(type(['columns']))
    # print(st.session_state.inf_chart)
    df = pd.DataFrame([5],index=[3],columns=['columns'])
    if 'inf_chart' not in st.session_state:
        st.session_state['inf_chart'] = st.line_chart(data=df,width=500)
    df1 = pd.DataFrame([4],index=[4],columns=['columns'])
    st.dataframe(df1)
    st.session_state.inf_chart.add_rows(df1)


def reading(env):
    while 1:
        yield env.timeout(0.5)
        read_logs_update_chart_test()

start_point=0
def read_logs_update_chart_test():
    fo = open("logfile.log", "rb") # 'rb for bites'
    global start_point 
    fo.seek(start_point, 1)
    line = fo.readline()
    for line in fo.readlines():
        if line is not None:
            logs = str(line.decode())
            if logs[0].isdigit():
                temp_list = logs.split(":")
                pattern = re.compile(r'[0-9]*\.?[0-9]\w')
                power_sum = pattern.findall(temp_list[2])
                power = float(power_sum[0]) + float(power_sum[1])
                element = []
                element.append(power)
                columns = temp_list[1]
                i = temp_list[0]
                df = pd.DataFrame(element,index=[i],columns=[columns])
                # df.index = df.index.map(str)
                df.index = df.index.astype('float64')
                st.session_state.inf_chart.add_rows(df)
                time.sleep(0.5)
            else:
                continue
    start_point=fo.tell() # move pointer to last bite
    fo.close()

# start_point=0
def read_logs_update_chart():
    fo = open("logfile.log", "rb") # 'rb for bites'
    global start_point 
    fo.seek(start_point, 1)
    line = fo.readline()
    if line is not None:
        logs = str(line.decode())
        if logs[0].isdigit():
            temp_list = logs.split(":")
            pattern = re.compile(r'[0-9]*\.?[0-9]\w')
            power_sum = pattern.findall(temp_list[2])
            power = float(power_sum[0]) + float(power_sum[1])
            element = []
            element.append(power)
            columns = temp_list[1]
            i = temp_list[0]
            df = pd.DataFrame(element,index=[i],columns=[columns])
            # df.index = df.index.map(str)
            df.index = df.index.astype('float64')
            st.session_state.inf_chart.add_rows(df)
    start_point=fo.tell() # move pointer to last bite
    fo.close()


def draw_infrastructure(element,i,columns):
    df = pd.DataFrame(element,index=[i],columns=[columns])
    st.session_state.inf_chart.add_rows(df)

# def get_dataframe_from_logs(element,i,columns):
#     df = pd.DataFrame(element,index=[i],columns=[columns])
#     return df

def storeStrintoPy(str,filename):
    copy_to_py = open(filename, 'w')
    copy_to_py.write(str)
    copy_to_py.close()

# def live_chart(chart,filename):
#     for i in range(12):
#         chart.add_rows(UIsupport.pop_log(filename,i))
#         time.sleep(0.05)


# def pop_log(filename,i,columns):
#     f = open(filename,'r')
#     list = re.compile(r'[0-9]*\.?[0-9]\w').findall(f.read())
#     f.close()
#     one_element = []
#     print(list[i])
#     one_element.append(float(list[i]))
#     df = pd.DataFrame(one_element,index=[i],columns=[columns])
#     return df

# element = st.empty()
# element.line_chart(...)

# powermeters = ()
# def get_sorted_columns(full_list):
#     global powermeters
#     if full_list[1] not in powermeters:
#         temp = list(powermeters)
#         temp.append(full_list[1])
#         powermeters = tuple(temp)
#     return powermeters

# def getlist(filename,output_type):
#      f = open(filename,'r')
#      readpower = re.compile(r'[0-9]*\.?[0-9]\w').findall(f.read())
#      f.close()
#      for i in range(len(readpower)):
#           readpower[i] = float(readpower[i])
#      txtpower = []
#      txtpower+=readpower
#      if output_type == 'list':
#           return txtpower
#      elif output_type == 'DataFrame':
#           df = pd.DataFrame (txtpower,columns=['asf'])
#           return df


    