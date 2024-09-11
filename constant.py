import streamlit as st  

skill_col_size = 5

def menu():
    bar0, bar1, bar2, bar3, bar4= st.columns([0.1,1,1,1,1])
    bar1.page_link("🏠_Mainpage.py", label="Introduction", icon="🏠")
    bar2.page_link("pages/1_📚_Experience.py", label= "Experience", icon="📚")
    bar3.page_link("pages/2_🎨_Portofolio.py", label="Portofolio", icon="🎨")
    bar4.page_link("pages/3_🌏_Contacts.py", label="Contacts", icon="🌏")
    st.write("")

#publication_url --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
linkedin_logo = '''                                                                                                                                          
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
  <i class="fa-brands fa-linkedin" style="font-size: 28px;"></i>                                                                           
'''

github_logo = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
  <i class="fa-brands fa-github" style="font-size: 28px;"></i>                                                                           
'''

# personal info (for main page) --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
info = {'brief':
              """    
                 I'm on a journey to explore the fascinating world of data and code. Currently, I'm pursuing my Master's in Applied Data Science at the University of Southern California. I'm a coding enthusiast with a love for data, coffee, and open-source projects.
                **I believe in the intersectionality of quantitative and qualitative subjects, that neither approach alone can lead one to the absolute truth.**
              """,
        'name':'Likhit Jha', 
        'study':'University of Southern California',
        'location':'Los Angeles, CA',
        'interest':'Data Science, Machine Learning',
        'skills' : ['Python', 'R', 'C++', 'C#', 'MATLAB', 'Hadoop', 'SQL', 'NoSQL (Firebase)', 'Spark', 'scikit-learn', 'pandas', 'TensorFlow', 'PyTorch', 'LangChain', 'matplotlib', 'Data science pipeline', 'Statistics', 'Time series', 'Hypothesis testing', 'Excel', 'Tableau', 'Git', 'Vertex AI']
,
        }

# Experience --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#[[header, subheader, date, location, content, link, link_url], [...], etc.]

Experience = [
              [":orange[WNS Global]", "Data Science Intern", 
              "May 2024 – August 2024", "New York, USA", 
              """
              - Utilized Python to implement supervised machine learning techniques for time series forecasting and compared them with large models, which reduced processing time by 90%. Primarily focused on Xgboost, Prophet, TimeGPT, Chronos, LagLlama.
              - Delivered thorough results to the global head, authoring an executive summary that outlined a strategic value proposition.
              - Engineered enhancements to the “Trust bridge” tool, specifically focusing on fairness in model governance and interpretation, resulting in production deployment of the optimal model that met all quality assurance checkpoints. 
              - Enhanced Trust bridge’s capabilities by integrating an architecture of LLM agents and resulting in a 30% increase in model interpretability and transparency.
              """, 
              "Company website", "https://www.wns.com/capabilities/analytics",
              "**Skills:** Python, Time Series Forecasting, Xgboost, Prophet, TimeGPT, Chronos, LagLlama, LLM, Model Governance"],


              [":blue[Laminaar Aviation Infotech]", "Machine Learning Intern", 
              "June 2022 – September 2022", "Mumbai, India", 
              """
              - Performed exploratory data analysis to interpret patterns in time series, and shared insights with an industry mentor.
              - Conducted in-depth research on standby crew operations in the airline industry to accurately forecast no-show rates; findings led to a 20% reduction in operational costs associated with crew scheduling inefficiencies.
              - Improved accuracy of Prophet model by 6% through feature selection and reduced training time by 17%.
              """,
              "Company website", "https://www.laminaar.com",
              "**Skills:** Python, Time Series Forecasting, Prophet, Feature Selection"],

              [":red[AUR Consultant]", "Machine Learning & Artificial Intelligence Intern", 
              "May 2022 – June 2022", "Nagpur, India", 
              """
              - Led the development of an AI recruitment chatbot using Rasa and Python
              - Accelerated candidate screening time by 40% and streamlined the hiring process for over 200 applicants per month. Integrated features included resume parsing, interview scheduling, and reminder notifications.
              - Trained a SpaCy NER model with a dataset of over 2000 resumes, facilitating text summarization.
              """,
              "Company website", "https://aurconsultant.com",
              "**Skills:** Python, Rasa, AI, SpaCy, NER, Chatbots"]

]

# Portfolio --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#     {'project1':[HEADER, CONTENT]
#      'project2':[HEADER, CONTENT]
#      ...}

Portfolio = {  
    1: [':blue[Big Data] Restaurant Recommendation System',
        """
        - Utilized **NLP** to analyze and categorize reviews, combined with Association Rules and Graph algorithms to enhance restaurant recommendations based on user preferences and social connections.
        - Developed a hybrid restaurant recommendation system on Yelp dataset using collaborative filtering and **XGBoost** with **Apache Spark**.
        """],
    2: [':orange[NLP] in Mitigating Runway Incursions',
        """
        - Collaborated with leading professors in Aviation and NLP to analyze insights from 47,000+ NASA Aviation Safety reports
        - Identified human factors in 87.1% of incidents
        - Applied **BERTopic** and **LDA** to classify human factors into ten distinct categories, presenting key vulnerabilities to in the FAA Data challenge, with us securing a spot in the top 10 position in the copetition.
        """],
    3: [':blue[Custom] Database System',
        """
        - Designed and implemented a relational database system that streamlined the manipulation of large CSV datasets through chunk-based processing, enabling execution of 100+ Data Definition and Data Manipulation Language operations.
        - Developed advanced functionalities, including custom query language parsing and lexer rules using **Ply**.
        """],
    4: [':green[News] Classifier',
    """
    - Leveraged **Beautiful Soup** for web scraping to gather a comprehensive dataset from the Inshorts news website.
    - Developed and compared multiple classification models, including **Multinomial Naïve Bayes**, **Random Forest**, and **Decision Tree**, to identify the most accurate approach.
    - Achieved a high classification accuracy of 96.37% using the **Multinomial Naïve Bayes** model, outperforming other models in the process.
    - Successfully deployed the classifier on **Heroku**, ensuring seamless scalability and enabling real-time news categorization.
    """],
    5: [':pink[Anti-Chess] 2D Game',
    """
    - Developed and designed an online multiplayer variant of chess using **C#**, **Unity2D**, and **Firebase**.
    - Implemented custom rules and logic for Anti-Chess, where the objective is to lose all pieces, adding a unique twist to traditional gameplay.
    - Integrated **local multiplayer functionality** and used Firebase for player login and saving game data, ensuring a seamless and interactive experience for players.
    - Designed intuitive UI/UX for the chessboard and piece movements, enhancing user engagement with smooth animations and responsive controls.
    - Deployed the game on multiple platforms, allowing players to compete across different devices, and included user authentication and data storage for tracking player progress and statistics.
    """]


}
              
# Contacts --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
phone = "323-620-3822"
email = "ljha@usc.edu"
linkedin_link = "https://www.linkedin.com/in/likhit-jha"
github_link = "https://github.com/likhitjha"


# iframes --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
figma_iframe = '<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FlMYyNOptCmZb5JlYXmKkif%2FCourseEvaluation%3Ftype%3Ddesign%26node-id%3D160%253A1249%26mode%3Ddesign%26t%3DEj6BVdYEZCLgxthB-1" allowfullscreen></iframe>'

figma_link = "https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FlMYyNOptCmZb5JlYXmKkif%2FCourseEvaluation%3Ftype%3Ddesign%26node-id%3D160%253A1249%26mode%3Ddesign%26t%3DEj6BVdYEZCLgxthB-1"

StoryMap_iframe = "https://storymaps.arcgis.com/stories/dfb9689618e343cf9f6ef36d9a8329a7?header"

Evaluation_html = '''
                <div class="github-card" data-github="Rsirp0c/deis-course-evaluation" data-width="400" data-height="" data-theme="default"></div>
                <script src="https://cdn.jsdelivr.net/github-cards/latest/widget.js"></script>                
                '''
