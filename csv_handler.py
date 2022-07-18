from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import os
import shutil
from typing import Optional

CACHE = "./results_cache/"
INFRASTRUCTURE = 'infrastructure.csv'
APPLICATION = 'application.csv'
FILE = 'run.py'


def clean_cache(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)  
        os.mkdir(path)

def check_exists(inf,app):
    filelist = os.listdir(CACHE)
    print(filelist)
    if inf and app in filelist:
        print('2')
        return 2
    elif inf in filelist:
        print('1')
        print(inf)
        print(app)
        return 1
    else:
        print('False')
        return False

def read_first_line(csv):
    df = pd.read_csv(CACHE + csv,nrows = 1,index_col=0)
    return df

def get_row_length(csv):
    df = pd.read_csv(CACHE + csv,index_col=0)
    return df.shape[0]

def read_row_by_sequence(csv,nrows):
    df = pd.read_csv(CACHE + csv,nrows=nrows,index_col=0)
    return df

def merge_results():
    path = CACHE
    files = os.listdir(path)
    temp_inf = pd.read_csv('temp.csv',index_col=0)
    temp_app = pd.read_csv('temp.csv',index_col=0)
    for f in files:
        if '1_' in f and f.endswith('.csv'):
            df = pd.read_csv(path + f, index_col=0) 
            temp_inf = pd.merge(temp_inf,df,on='time',how='outer', sort=True) 
            temp_inf.fillna(method = 'ffill',inplace=True, axis = 0)
            temp_inf.to_csv(path + 'infrastructure.csv')
        elif '2_' in f and f.endswith('.csv'):
            df = pd.read_csv(path + f, index_col=0) 
            temp_app = pd.merge(temp_app,df,on='time',how='outer', sort=True) 
            temp_app.fillna(method = 'ffill',inplace=True, axis = 0)
            temp_app.to_csv(path + 'application.csv')


def output_csv(PM, rename, type: Optional[int] = 1, delay: Optional[float] = 0):
    result_dir = f"results_cache/"
    if rename:
        csv_content = "time,"+ rename +"\n"
    else:
        csv_content = "time,"+ PM.name +"\n"
    os.makedirs(result_dir, exist_ok=True)
    for i, powermeter in enumerate(PM.measurements):
        sum = powermeter.static + powermeter.dynamic
        j = i
        j*=PM.measurement_interval
        csv_content += f"{j + delay},{sum}\n"
    with open(f"{result_dir}/{type}_{rename}.csv", 'w') as csvfile:
        csvfile.write(csv_content)