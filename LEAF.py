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
          print('have file')
          if len(uploaded_files) > 1:
               if st.session_state.live == False:
                    for uploaded_file in uploaded_files:
                         if uploaded_file.name == ch.INFRASTRUCTURE:
                              inf_df = pd.read_csv(uploaded_file, index_col=0)
                              infrastructure.line_chart(data=inf_df, width=500, height=500)
                         elif uploaded_file.name == ch.APPLICATION:
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
          print('code')
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
     </style>''', unsafe_allow_html=True)