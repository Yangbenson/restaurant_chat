class ChatUI:
    css = '''
    <style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .avatar img {
      max-width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
    }
    .chat-message .message {
      width: 80%;
      padding: 0 1.5rem;
      color: #fff;
    }
    </style>
    '''

    bot_template = '''
    <div class="chat-message bot">
        <div class="avatar">
            <img src="https://ibb.co/hK5zt5Y/cutlery.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>
        <div class="message">{{MSG}}</div>
    </div>
    '''

    user_template = '''
    <div class="chat-message user">
        <div class="avatar">
            <img src="https://ibb.co/hK5zt5Y/cutlery.png">
        </div>    
        <div class="message">{{MSG}}</div>
    </div>
    '''

    linkedin_link = '''
    <style>
        /* Add some basic padding and alignment */
        .fa {
            padding-right: 5px;
        }
    </style>
    <a href="https://www.linkedin.com/in/pinghsien-yang/" target="_blank" style="margin-right: 15px; text-decoration: none;">
        <i class="fab fa-linkedin-in" style="font-size:24px; color: #0077B5;"></i>

    </a>
    '''

    github_link = '''
    <style>
        /* Add some basic padding and alignment */
        .fa {
            padding-right: 5px;
        }
    </style>
    <a href="https://github.com/Yangbenson/portfolio_chat" target="_blank" style="margin-right: 15px; text-decoration: none;">
        <i class="fa-brands fa-github" style="font-size:24px; color: #0077B5;"></i>

    </a>
    '''

    email_link = '''
       <style>
           /* Add some basic padding and alignment */
           .fa {
               padding-right: 5px;
           }
       </style>
       <a href="mailto:bensonyang0326@gmail.com" target="_blank" style="text-decoration: none;">
           <i class="fa-solid fa-envelope" style="font-size:24px; color: #0077B5;"></i>

       </a>
       '''

    resume4show = """
    Benson (Ping Hsien) Yang\n

    EXPERIENCE

    Market Analyst | Python, SQL\n
    ARCADIA MOTOR CO., LTD. | Taipei, Taiwan


    June 2020 - August 2021

    •	Extracted key metrics from SQL databasesPerformed advanced analysis using Python, leading to the identification of emerging market trends and insights into user behavior, resulting in a 15% increase in marketing efficiency\n
    •	Work closely with cross-functional teams, including sales, product, and technology teams, to ensure accuracy and viability of market insights and make data-based strategic recommendations to drive business growth.

    Software Engineer | VB, Javascript, MYSQL\n
    ChainSea Information Integration Co., Ltd | Taipei, Taiwan

    September 2018 - September 2019

    •	Performed proactive and ad-hoc product analyses to identify key customer needs and create cyber security through new product features.\n
    •	Reviewed, modified, and implemented A/B tests for unit and integration assessments to enhance the Bank's software quality and reliability.

    EDUCATION

    August 2022 - May 2024

    Master of Science in Business Analytics\n
    Hofstra University | Hempstead,NY\n
    •	GPA : 4.0, Graduate Excellence Award Recipient

    August 2016 - May 2020\n

    Bachelor in Information Management\n
    National Taipei University of Business | Taipei, Taiwan

    PROJECTS

    Quantium Virtual Project from Forage| R, Tableau	August 2023 - August 2023\n
    Conducted advanced data analysis on transaction and purchase behavior data. Utilized tools Tableau and R for data visualization, statistical modeling, and data processing, producing clear and concise reports for Quantium.\n

    Slide Assistant by Open AI| Python, MySQL	June 2023 - August 2023\n
    Utilized Python programming and the latest GPT model, designed innovative and user-friendly presentation scripts that generate interfaces and help users improve their presentations.\n

    E-commercial Website Scraping and Analysis | Python, MySQL	August 2022 - November 2022\n
    Used Python to collect data on the website and inserted it into a database built on the AWS EC2 server, analyzed each dataset's correlation, and visualized it in several charts. Finally, used LSTM Neural Networks to predict the market.

    KEY SKILLS

    Software / Programming: Python, R, Matlab, Swift, EXCEL\n
    Data Stack: SQL, Tableau, GCP, AWS\n
    Python Packages: Pandas, NumPy, Matplotlib, scikit-learn, Tensorflow, GPT\n
    Machine Learning Models: Linear/Logistic Regression, Decision Trees, Random Forest, Extra Trees, k-Means Clusters, K-Nearest Neighbors, Neural Networks ( LSTM, CNNs ), NLP model\n

    """

    resume4gpt = """
    Benson (Ping Hsien) Yang\n

    Personal Link\n

    linkedin : https://www.linkedin.com/in/pinghsien-yang/
    GitHub : https://github.com/Yangbenson
    
    EXPERIENCE

    Market Analyst | Python, SQL\n
    ARCADIA MOTOR CO., LTD. | Taipei, Taiwan


    June 2020 - August 2021

    •	Extracted key metrics from SQL databasesPerformed advanced analysis using Python, leading to the identification of emerging market trends and insights into user behavior, resulting in a 15% increase in marketing efficiency\n
    •	Work closely with cross-functional teams, including sales, product, and technology teams, to ensure accuracy and viability of market insights and make data-based strategic recommendations to drive business growth.

    Software Engineer | VB, Javascript, MYSQL\n
    ChainSea Information Integration Co., Ltd | Taipei, Taiwan

    September 2018 - September 2019

    •	Performed proactive and ad-hoc product analyses to identify key customer needs and create cyber security through new product features.\n
    •	Reviewed, modified, and implemented A/B tests for unit and integration assessments to enhance the Bank's software quality and reliability.

    EDUCATION

    August 2022 - May 2024

    Master of Science in Business Analytics\n
    Hofstra University | Hempstead,NY\n
    •	GPA : 4.0, Graduate Excellence Award Recipient

    August 2016 - May 2020\n

    Bachelor in Information Management\n
    National Taipei University of Business | Taipei, Taiwan

    PROJECTS
    
    Quantium Virtual Project from Forage| R, Tableau	August 2023 - August 2023\n
    Conducted advanced data analysis on transaction and purchase behavior data. Utilized tools Tableau and R for data visualization, statistical modeling, and data processing, producing clear and concise reports for Quantium.\n

    Slide Assistant by Open AI| Python, MySQL	June 2023 - August 2023\n
    Utilized Python programming and the latest GPT model, designed innovative and user-friendly presentation scripts that generate interfaces and help users improve their presentations.\n

    E-commercial Website Scraping and Analysis | Python, MySQL	August 2022 - November 2022\n
    Used Python to collect data on the website and inserted it into a database built on the AWS EC2 server, analyzed each dataset's correlation, and visualized it in several charts. Finally, used LSTM Neural Networks to predict the market.

    

    KEY SKILLS

    Software / Programming: Python, R, Matlab, Swift, EXCEL\n
    Data Stack: SQL, Tableau, GCP, AWS\n
    Python Packages: Pandas, NumPy, Matplotlib, scikit-learn, Tensorflow, GPT\n
    Machine Learning Models: Linear/Logistic Regression, Decision Trees, Random Forest, Extra Trees, k-Means Clusters, K-Nearest Neighbors, Neural Networks ( LSTM, CNNs ), NLP model\n

    Background:
    
    As an international student majoring in Data Analytics with hands-on experience in Python, R, and SQL, I have developed a deep appreciation for leveraging data to drive business decisions. Additionally, I gained real-time finance program experience while working at a bank software development company in Taiwan.
    My passion for critical thinking and technical proficiency make me a strong candidate for this role.
    
    During my master's academic years, I have been actively involved in various data analytics projects that required technical know-how and a keen understanding of business dynamics. These experiences have sharpened my ability to translate complex data into actionable insights.
    
    I have uploaded my projects on GitHub, which is linked on my resume for everyone's review.
    """

