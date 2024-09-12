import streamlit as st
import streamlit.components.v1 as components
from constant import *


# page config ----------------------------------------------------------------
st.set_page_config(page_title="Portofolio", page_icon="🎨", layout="wide",initial_sidebar_state="collapsed")
margin_r,body,margin_l = st.columns([0.4, 3, 0.4])

with body:
   menu()

   st.header("🎨 Portfolio",divider='rainbow')

   # page functions ----------------------------------------------------------------
   def Portfolio_component(header, content):
      st.subheader(header, divider='grey')
      st.write(content)

   # RAG  ----------------------------------------------------------------
   Portfolio_component(Portfolio[1][0], Portfolio[1][1])
   st.link_button("Go to :blue[Source Code]", "https://github.com/likhitjha/RestaurantReccomendationSystem")

   # Deis Evaluation ----------------------------------------------------------------
   Portfolio_component(Portfolio[2][0], Portfolio[2][1])

   tab1, tab2 = st.tabs(["View Article", "View Website"])
   with tab1:  
      st.link_button("Go to Website", "https://viterbischool.usc.edu/news/2023/11/too-close-for-comfort-usc-viterbi-students-use-ai-to-prevent-aircraft-collisions")
      components.iframe("https://viterbischool.usc.edu/news/2023/11/too-close-for-comfort-usc-viterbi-students-use-ai-to-prevent-aircraft-collisions/", width=800, height=600, scrolling=True)
   with tab2:
      st.link_button("Go to Website", "https://ckids-datafirst.github.io/2023-fall-aviation-safety")
      components.iframe("https://ckids-datafirst.github.io/2023-fall-aviation-safety", width=800, height=600, scrolling=True)

   # Data VIS in D3.js --------------------------------------------------------------
   Portfolio_component(Portfolio[3][0], Portfolio[3][1])

   st.link_button("Go to Github", "https://github.com/Rsirp0c/D3-practice")
   st.image("src/Custom_Database_System.jpg")

   # Desktop ChatApp -------------------------------------------------------------- 
   Portfolio_component(Portfolio[4][0], Portfolio[4][1])


   st.link_button("Go to Website", "https://leekith-newsclassifier.herokuapp.com")
   components.iframe("https://leekith-newsclassifier.herokuapp.com", width=800, height=600, scrolling=True)

   st.link_button("Go to :blue[Source Code]", "https://github.com/Rsirp0c/desktop_chatapp")

   #  -----------------------------------------------------------


   # Add Anti Chess project -----------------------------------------------------------
   Portfolio_component("Anti Chess", "A unique twist on traditional chess where the goal is to lose all your pieces. Developed using [your technology stack].")
   
   tabs = st.tabs(["Game Play"])

   with tabs[0]:
      st.video("src/AntiChess.mp4")  # Replace with your video path
      if st.button("Go to :blue[Game Website]"):
         st.write("[Click here](https://likhitjha.itch.io/anti-chess-beta-version)")
      if st.button("Go to :blue[Source Code]"):
         st.write("[Click here](https://github.com/likhitjha/AntiChess)")

   # Add Brick Breaker project -----------------------------------------------------------
   Portfolio_component("Brick Breaker", "A classic arcade game where you control a paddle to break bricks. Developed using Unity2D.")
   
   tabs = st.tabs(["Game Play"])
   with tabs[0]:
      st.video("src/BrickBreaker.mp4")  # Replace with your video path
      st.link_button("Go to :blue[Game Website]", "https://likhitjha.itch.io/brick-breaker-corona-edition")
      st.link_button("Go to :blue[Source Code]", "https://github.com/likhitjha/BrickBreaker")


with st.sidebar:
    messages = st.container(height=300)
    if prompt := st.chat_input("Say something"):
        messages.chat_message("user").write(prompt)
        messages.chat_message("assistant").write(f"Echo: {prompt}")
