import streamlit as st
from googlesearch import search
from time import sleep, time
from _datetime import datetime
import sys
import subprocess
from smtp import AnalysisEmail

# Title of the app
st.title("Web Scrapper 1.0")

# Navigation management
if 'view' not in st.session_state:
    st.session_state.view = 'main'

#Button setting


# Function to navigate to the 'main' view
def go_to_main():
    st.session_state.view = 'main'


# Function to navigate to the 'another' view
def go_to_another():
    st.session_state.view = 'another'

def send_email():
    st.session_state.view = 'email'

# Main view
if st.session_state.view == 'main':
    st.subheader("Stage 1")
    st.subheader("Google Search")
    query = st.text_input("Please enter for SERP results: ")
    CurrentTime = datetime.today()
    Seconds = CurrentTime.timestamp()
    if query != "":

        st.write("Executing your results for ", query)
        st.write("Please wait...!!!")

        Links = open(str(Seconds), 'a')
        Links.write(query + "\n")
        links = []
        i = 0
        TotalTimeTaken = 0
        TimeInMin = 0
        Start = time()

        for j in search(query, tld="com.tw", num=10, stop=6, pause=14,
                        user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"):
            st.write(j)
            i += 1
            sleep(1)
            links.append(j)

            Links.write(str(i) + ',' + str(j))
            Links.write('\n')

        End = time()
        TotalTimeTaken = End - Start
        Links.close()

        st.write(str(i), "Results Found!!!!!")
        st.write(f"Time Taken: {int(TotalTimeTaken)} sec")
        Links = open(str(Seconds), 'r')
        btn = st.download_button(
            label="Download File",
            data=Links,
            file_name=str(Seconds) + ".csv",
            mime="text/csv"
        )
        Links.close()



        another_btn = st.button("Analyze")
        if another_btn == False:
            another_btn = True
        go_to_another()

# Another view
elif st.session_state.view == 'another':
    st.subheader("Stage 2")
    from SEO_Analyzer import Analyze

    url = st.text_input("Enter URL to analyze: ")

    if url != "":
        ProgressBar = st.progress(0)
        for progress in range(100):
            sleep(0.05)
            ProgressBar.progress(progress+1)
        Analyze(url)
        send_btn = st.button("Send analysis report")
        if send_btn == False:
            send_btn = True
        send_email()
elif st.session_state.view == 'email':
    st.subheader("Stage 3")
    SendTo = st.text_input("Enter email for analysis report: ")
    if SendTo != "":
        AnalysisEmail(SendTo)
        st.success("Email sent...!!!")


        main_btn = st.button("Search More")
        if main_btn == False:
            main_btn = True
        go_to_main()
