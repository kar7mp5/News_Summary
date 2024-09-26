# app.py
from ArticleTools import get_req, summarize_article

import streamlit as st
import pandas as pd
import os


# Define variable to track the tasks
if 'keep_running' not in st.session_state:
    st.session_state.keep_running = False


# Any asyncronous task
def run_task():
    while st.session_state.keep_running:
        print('Background Task running...')
        df = pd.DataFrame(get_req())

        for idx in range(len(df['link'])):
            st.markdown(f"""{summarize_article(df['link'][idx])}""")


# Streamlit
def main():
    st.title('2024 Google MLB - Gemma Sprint')
    st.session_state.keep_running = st.toggle('Activate Background Tasks', key='toggle_bot')

    if st.session_state.keep_running:
        st.toast('Running background Tasks', icon='🤖')
        # THE CODE IS STUCK HERE
        run_task()

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        st.write('Stop background Tasks.')


if __name__ == "__main__":
    main()
