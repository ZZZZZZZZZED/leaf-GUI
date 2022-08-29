import csv_handler as ch
import streamlit as st
import pandas as pd
import numpy as np
import time
import UIsupport as ui
from PIL import Image
from streamlit_ace import st_ace
from decimal import Decimal


st.set_page_config(
     page_title="LEAF - Simulator User Interface",
     page_icon=Image.open(ui.LOGO),
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "What is LEAF: https://leaf.readthedocs.io/en/latest/"
     }
)

#title
st.title('LEAF')

#describing
st.write("This application is developed for the MSc Development Project for IT+ project at the University of Glasgow.")
st.write("Try Examples, Python Input, and Import Results input methods are provided for you to use LEAF in different stages.") 
st.markdown("**Try Examples**: Two examples provide here, both adopted by original LEAF examples.")
st.write("**Python Input**:  This is the primary input method of this program; providing a Python compiler, users can imitate the case code to get the custom result.")
st.write("**Import Results**: This option is mainly used to render complex simulations. Users need to use LEAF to get the results locally and import the result file into the system to get the corresponding graph.")

if 'loadinggif' not in st.session_state:
     st.session_state['loadinggif'] = st.empty()

tab1, tab2, tab3 = st.tabs(["⏱️ Try Examples","📈 Python Input" ,"📁 Import Results"])
with tab2.container():
     st.write('Before running your script, don\'t forget to clean up uploaded files and choose example to defaut.')
     Input = st_ace(language = 'python', theme='xcode', key="code input", auto_update=True, max_lines=20, font_size=22)

with tab1.container():
     st.write('You can try some LEAF examples here!')
     st.write('If you want to type python codes in, please choose empty example and clean up updated files.')
     choosed_example = st.selectbox(
     'Choose a example to check the results.',
     ('-', 'LEAF - Single Node', 'LEAF - Application Placement'))

with tab3.container():
     uploaded_files = st.file_uploader("Choose csv files output from LEAF simulator.", help='Choose \'infrustructure.csv\' or \'infrustructure.csv\' and \'application.csv\'',accept_multiple_files=True)




#chart layout spaceholder
infrastructure, application = st.columns(2)
infrastructure.empty()
application.empty()


col1, col2 , col3= st.columns([1, 2, 3])

agree = col1.checkbox('Live Chart')
if agree:
     if 'live' not in st.session_state:
          live = True
     st.session_state['live'] = True
     st.session_state['delay'] = col2.select_slider('Set animation speed(sec)', options=np.arange(Decimal('0.01'), Decimal('1'), Decimal('0.01')))
else:
     if 'live' not in st.session_state:
          live = False
     st.session_state['live'] = False

def draw_condition():
     if ch.check_exists(ch.INFRASTRUCTURE, ch.APPLICATION) == 2:
          if st.session_state.live == False:
               draw_inf_app()
          else:
               draw_live_inf_app()
          st.success('Done!')
     elif ch.check_exists(ch.INFRASTRUCTURE, ch.APPLICATION) == 1:
          if st.session_state.live == False:
               draw_inf()
          else:
               draw_live_inf()
          st.success('Done!')
     else:
          st.error('''Please input valid code so that the LEAF simulator can output results.
               Check About for more detail.''')
          st.empty()

def draw_inf():
     inf_df = pd.read_csv(ch.CACHE+ch.INFRASTRUCTURE, index_col=0)
     st.line_chart(data=inf_df)

def draw_live_inf():
     inf_df = ch.read_first_line(ch.INFRASTRUCTURE)
     inf_chart = st.line_chart(data=inf_df, width=500, height=500)
     for i in range(1, ch.get_row_length(ch.INFRASTRUCTURE)):
          inf_chart.add_rows(ch.read_row_by_sequence(ch.INFRASTRUCTURE, nrows=i))
          time.sleep(float(st.session_state.delay))

def draw_inf_app():
     inf_df = pd.read_csv(ch.CACHE+ch.INFRASTRUCTURE, index_col=0)
     infrastructure.line_chart(data=inf_df, width=500, height=500)
     app_df = pd.read_csv(ch.CACHE+ch.APPLICATION, index_col=0)
     application.line_chart(data=app_df, width=500, height=500)

def draw_live_inf_app():
     inf_df = ch.read_first_line(ch.INFRASTRUCTURE)
     inf_chart = infrastructure.line_chart(data=inf_df, width=500, height=500)
     app_df = ch.read_first_line(ch.APPLICATION)
     app_chart = application.line_chart(data=app_df, width=500, height=500)
     for i in range(1, ch.get_row_length(ch.INFRASTRUCTURE)):
          inf_chart.add_rows(ch.read_row_by_sequence(ch.INFRASTRUCTURE, nrows=i))
          time.sleep(float(st.session_state.delay)/2)
     for i in range(1, ch.get_row_length(ch.APPLICATION)):
          app_chart.add_rows(ch.read_row_by_sequence(ch.APPLICATION, nrows=i))
          time.sleep(float(st.session_state.delay)/2)

if st.button('Run simulator'):
     st.session_state['loading'] = False
     ch.clean_cache(ch.CACHE)
     ui.loading(ui.LOADING_GIF)
     if len(uploaded_files) != 0:
          #local file chooser
          if len(uploaded_files) > 1:
               if st.session_state.live == False:
                    print(uploaded_files)
                    for uploaded_file in uploaded_files:
                         print(uploaded_file.name)
                         if uploaded_file.name == ch.INFRASTRUCTURE:
                              print("infname = "+uploaded_file.name)
                              inf_df = pd.read_csv(uploaded_file, index_col=0)
                              infrastructure.line_chart(data=inf_df, width=500, height=500)
                         elif uploaded_file.name == ch.APPLICATION or uploaded_file.name == 'applications.csv':
                              print("appname = "+uploaded_file.name)
                              app_df = pd.read_csv(uploaded_file,index_col=0)
                              application.line_chart(data=app_df, width=500, height=500)
               else:
                    for uploaded_file in uploaded_files:
                         ch.into_cache(uploaded_file)
                    inf_df = ch.read_first_line(ch.INFRASTRUCTURE)
                    inf_chart = infrastructure.line_chart(data=inf_df, width=500, height=500)
                    app_df = ch.read_first_line(ch.APPLICATION)
                    app_chart = application.line_chart(data=app_df, width=500, height=500)
                    for i in range(1, ch.get_row_length(ch.INFRASTRUCTURE)):
                         inf_chart.add_rows(ch.read_row_by_sequence(ch.INFRASTRUCTURE, nrows=i))
                         time.sleep(float(st.session_state.delay)/2)
                    for i in range(1, ch.get_row_length(ch.APPLICATION)):
                         app_chart.add_rows(ch.read_row_by_sequence(ch.APPLICATION, nrows=i))
                         time.sleep(float(st.session_state.delay)/2)
               st.success('Done!')
          elif len(uploaded_files) == 1:
               uploaded_file = uploaded_files[0]
               if st.session_state.live == False:
                    inf_df = pd.read_csv(uploaded_file, index_col=0)
                    st.line_chart(data=inf_df)
               else:
                    ch.into_cache(uploaded_file)
                    inf_df = ch.read_first_line(ch.INFRASTRUCTURE)
                    inf_chart = st.line_chart(data=inf_df, width=500, height=500)
                    for i in range(1, ch.get_row_length(ch.INFRASTRUCTURE)):
                         inf_chart.add_rows(ch.read_row_by_sequence(ch.INFRASTRUCTURE, nrows=i))
                         time.sleep(float(st.session_state.delay))
               st.success('Done!')
          else:
               st.error('''Please choose files before start drawing.''')
     elif choosed_example=='LEAF - Single Node':
          #try examples
          print('LEAF - Single Node')
          ui.run_example('example1.py')
          draw_condition()

     elif choosed_example=='LEAF - Application Placement':
          #try examples
          print('LEAF - Application Placement') 
          ui.run_example('example2.py')
          draw_condition()

     elif len(Input) > 0:
          #run code
          ui.storeStrintoPy(string=Input, filename=ch.FILE)
          draw_condition()
     ui.loading('static/loading.gif')




#css
st.markdown('''
     <style>
     .st-cf{font-size: 20px;}
     .st-af{font-size: 20px;}
     #leaf > div > span{color: green; font-size: 80px;}
     .css-15tx938{font-size: 20px;}
     #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(2) > div > div > p{color: green;}
     #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(3) > div > div > p{font-size: 20px;}
     #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(4) > div > div > p{font-size: 20px;}
     #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(5) > div > div > p{font-size: 20px;}
     #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(6) > div > div > p{font-size: 20px;}
     </style>''', unsafe_allow_html=True)