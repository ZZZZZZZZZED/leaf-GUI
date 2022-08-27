import pandas as pd
import os
import shutil
from typing import Optional

CACHE = "./results_cache/"
INFRASTRUCTURE = 'infrastructure.csv'
APPLICATION = 'application.csv'
FILE = 'run.py'
STATIC = "./static/"


#copy results into cache file
def into_cache(UploadedFile):
    df = pd.read_csv(UploadedFile,index_col=0)
    temp = pd.read_csv(STATIC+'temp.csv',index_col=0)
    temp = pd.merge(temp,df,on='time',how='outer', sort=True) 
    temp.fillna(method='ffill',inplace=True,axis=0)
    temp.to_csv(CACHE+UploadedFile.name)

#clean cache file before new simulation
def clean_cache(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)  
        os.mkdir(path)

#check if inf and app exists to modify spaceholder
def check_exists(inf,app):
    filelist = os.listdir(CACHE)
    if inf and app in filelist:
        return 2
    elif inf in filelist:
        return 1
    else:
        return False

#read first line to be a base of addrows
def read_first_line(csv):
    df = pd.read_csv(CACHE + csv,nrows = 1,index_col=0)
    return df

def get_row_length(csv):
    df = pd.read_csv(CACHE + csv,index_col=0)
    return df.shape[0]

#optimize performance
def read_row_by_sequence(csv,nrows):
    df = pd.read_csv(CACHE + csv,nrows=nrows,index_col=0)
    return df

def merge_results():
    files = os.listdir(CACHE)
    temp_inf = pd.read_csv(STATIC+'temp.csv',index_col=0)
    temp_app = pd.read_csv(STATIC+'temp.csv',index_col=0)
    for f in files:
        if '1_' in f and f.endswith('.csv'):
            df = pd.read_csv(CACHE + f, index_col=0) 
            temp_inf = pd.merge(temp_inf,df,on='time',how='outer', sort=True) 
            temp_inf.fillna(method = 'ffill',inplace=True, axis = 0)
            temp_inf.to_csv(CACHE + 'infrastructure.csv')
        elif '2_' in f and f.endswith('.csv'):
            df = pd.read_csv(CACHE + f, index_col=0) 
            temp_app = pd.merge(temp_app,df,on='time',how='outer', sort=True) 
            temp_app.fillna(method = 'ffill',inplace=True, axis = 0)
            temp_app.to_csv(CACHE + 'application.csv')

#core function to make the base of lines then front-end can draw it.
def output_csv(PM, rename, filter:Optional[str] = 'sum',type: Optional[int] = 1, delay: Optional[float] = 0):
    result_dir = f"results_cache/"
    sum_contect = "time,"+ rename +"\n"
    dynamic_content = "time,"+ rename+' dynamic' +"\n"
    static_content = "time,"+ rename+' static' +"\n"
    full_content = "time,"+ rename+' static,' + rename+' dynamic'+"\n"
    os.makedirs(result_dir, exist_ok=True)
    for i, powermeter in enumerate(PM.measurements):
        sum = powermeter.static + powermeter.dynamic
        j = i
        j *= PM.measurement_interval
        if filter == 'sum':
            sum_contect += f"{j + delay},{sum}\n"
        elif filter == 'dynamic':
            dynamic_content += f"{j + delay},{powermeter.dynamic}\n"
        elif filter == 'static':
            static_content += f"{j + delay},{powermeter.static}\n"
        elif filter == 'all':
            full_content += f"{j + delay},{powermeter.static},{powermeter.dynamic}\n"
    with open(f"{result_dir}/{type}_{rename}.csv", 'w') as csvfile:
        if filter == 'sum':
            csvfile.write(sum_contect)
        elif filter == 'dynamic':
            csvfile.write(dynamic_content)
        elif filter == 'static':
            csvfile.write(static_content)
        elif filter == 'all':
            csvfile.write(full_content)

def from_filechooser_to_cache(file):
    shutil.move(file,CACHE+file)

