# # app.py
# import streamlit as st

import pandas as pd
from ArticleTools import get_req, summarize_article

# df = pd.DataFrame(get_req())

# st.markdown(f"""
# # 2024 Google MLB - Gemma Sprint
# {summarize_article(df['link'][0])}
# """)

import os
import streamlit as st
import asyncio

# Define variable to track the tasks
if 'keep_running' not in st.session_state:
    st.session_state.keep_running = False

# Any asyncronous task
async def run_task():
    while st.session_state.keep_running:
        print('Background Task running...')

        df = pd.DataFrame(get_req())

        st.markdown(f"""
# 2024 Google MLB - Gemma Sprint
{summarize_article(df['link'][13])}
        """)

        await asyncio.sleep(1)

# Streamlit
def main():
    st.title('Background Task with streamlit')

    st.session_state.keep_running = st.toggle('Activate Background Tasks', key='toggle_bot')

    nome = st.text_input('Enter your name', key='name')

    st.write(f'Hello {nome}!')

    if st.session_state.keep_running:
        st.toast('Running background Tasks', icon='🤖')
        # THE CODE IS STUCK HERE
        asyncio.run(run_task())
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        st.write('Stop background Tasks.')

# Execute Streamlit
if __name__ == "__main__":
    main()
