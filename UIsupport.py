
import os
import streamlit as st
import base64

 

LOADING_GIF = 'static/loading.gif'
LOGO = 'static/logo.png'

#toggle loading animation
def loading(path):
    if st.session_state.loading == False:
        st.session_state['loading'] = True
        file_ = open(path, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.session_state['loadinggif'] = st.markdown(f'<div style="text-align: center"> <img src="data:image/gif;base64, {data_url}" alt="loading gif"> </div>', unsafe_allow_html=True,)
    elif st.session_state.loading == True:
        st.session_state['loading'] = False
        st.session_state['loadinggif'].empty()

def storeStrintoPy(string, filename):
    copy_to_py = open(filename, 'w')
    copy_to_py.write(string)
    copy_to_py.close()
    os.system('python %s' %filename)

def run_example(filename):
    copy_to_py = open('run.py', 'w')
    f = open("./leaf_examples/" + filename)
    string = f.read()
    copy_to_py.write(string)
    copy_to_py.close()
    os.system('python run.py')
