import logging
import os
import re
import time
import pandas as pd
import streamlit as st




def reading(env):
    while 1:
        yield env.timeout(0.5)
        read_logs_update_chart()

start_point=0
def read_logs_update_chart():
    fo = open("logfile.log", "rb") # 'rb for bites'
    global start_point 
    fo.seek(start_point, 1)
    for line in fo.readlines():
        logs = str(line.decode())
        if logs[0].isdigit():
            temp_list = logs.split(":")
            pattern = re.compile(r'[0-9]*\.?[0-9]\w')
            power_sum = pattern.findall(temp_list[2])
            power = float(power_sum[0]) + float(power_sum[1])
            element = []
            element.append(power)
            columns = temp_list[1] #columns name
            i = temp_list[0] # 
            draw_infrastructure(element,i,columns)

        else:
            continue
    start_point=fo.tell() # move pointer to last bite
    fo.close()


def draw_infrastructure(element,i,columns):
    df = pd.DataFrame(element,index=[i],columns=[columns])
    st.dataframe(df)
    print(st.session_state.inf_chart)
    st.session_state['inf_chart'].add_rows(df)

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


    