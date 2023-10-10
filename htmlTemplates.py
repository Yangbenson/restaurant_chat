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
            <img src="https://i.ibb.co/dknS9xP/book.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>
        <div class="message">{{MSG}}</div>
    </div>
    '''

    user_template = '''
    <div class="chat-message user">
        <div class="avatar">
            <img src="https://i.ibb.co/022Lh8Q/user.jpg">
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


