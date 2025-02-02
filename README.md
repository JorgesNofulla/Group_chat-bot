# Group Chat-bot

A  Flask-based web application that demonstrates a multi-AI group chat using the Groq Llama API (or any future models you may integrate). Currently, two AI “personalities” interact alongside the user in one conversation. This README provides setup instructions, usage notes, and configuration tips.

### Important Preparation ⚠︎
- Obtain a Groq API Key
    1. Sign up at https://console.groq.com/ to get a free API key.
    2. Keep your key private and never commit it to version control.```https://console.groq.com/```
- Set Up Environment Variable
    1. In your virtual environment, run: ```set GROQ_API_KEY=[Your Key] ```
    2. (On Windows, use the set command; on macOS/Linux use export GROQ_API_KEY=[Your Key].) Make sure this environment variable is set each time you use or deploy the application.

## Overview
This repository presents a code design intended to create a Group Chat involving two AI agents. Currently, both agents make calls to the same model endpoint (Llama 3.3–70b–versatile via Groq). In the future, you can easily swap in different models for each agent if desired.

1. How It Works:

    - User enters a prompt in the chat interface.
    - Two AIs—currently “Joe Biden” and “Donald Trump”—each respond in turn.
    - The conversation history is preserved server-side, ensuring each AI can “see” what was said by the user and the other AI, enabling them to respond accordingly.
      
2. Disclaimer:

    This code is in a preliminary state; each AI responds only once per user message in the current version (different from the image below). Future expansions could allow multiple turns per AI, different conversation flows, or additional AIs.
    
![image](https://github.com/user-attachments/assets/c57233af-f265-4e33-be29-983f0250c0b1)

## Key Features

- Interactive Group Chat with Two AI: The system orchestrates two separate AI personalities that take turns responding to the user.
- Customizable Model & Personalities: Uses Llama 3.3–70b–versatile via Groq’s API, but can be adapted to other models or persona definitions.
- Scalable Chat History: The server tracks the entire conversation, allowing both AIs to remain contextually aware of user inputs and each other’s messages.
- Easy to Extend:
    1. Modify user names, personalities, and roles in the prompts.
    2. Adjust how many messages each AI returns per user prompt.
    3. Extend to more AI agents with minimal code changes.

## Project structure 
```
├── static/
│   ├── background.png        # Background image for the chat UI
│   ├── donald.png            # Icon for "Donald Trump" AI
│   ├── joe_biden.png         # Icon for "Joe Biden" AI
│   ├── chat_interface.js     # Client-side JS to handle UI logic
│   └── index.html            # Front-end HTML page
├── backend.py                # Main Flask application
├── requirements.txt          # Python dependencies
└── README.md                 # This documentation
```
### Installation

1. Clone the repository:
```
git clone https://github.com/JorgesNofulla/Group_chat-bot.git
cd group-chat-bot
```

2. Set up a virtual environment (recommended for Python projects):

```
python -m venv venv
venv\Scripts\activate
```  
3. Configure API Key

Ensure your GROQ_API_KEY environment variable is set. For instance:
```
set GROQ_API_KEY=[Your Key]
```
5. Run the Application
In the root directory where app.py is located, start the Flask server:

```
python backend.py
```

By default, it will run on http://0.0.0.0:5000. Open a web browser and go to http://localhost:5000 (or the appropriate IP/port if running remotely). You’ll see the chat UI with input box and conversation pane.

6. Interact with the Chat

    - Type your message and press Send.
    - You’ll receive responses sequentially from the two AIs (Joe Biden and Donald Trump).
    - The conversation logs appear in the chat window.


## Configuration & Customization

1. AI Personalities
    - The logic for each AI’s “system” prompts resides in app.py under lion_system_prompt and raccoon_system_prompt.
    Modify these prompts to change how each AI responds, their attitudes, or their manner of speech.

2. Model Settings
    - The code references model="llama-3.3-70b-versatile", but you can change this to any available Groq model (or eventually a different API) by modifying the generate_ai_response function in app.py.

3. Temperature / Max Tokens
    - Tweak temperature=0.5 for more “creative” or “deterministic” responses (higher = more creative), or adjust max_tokens=1024 to control the length of replies.

4. Chat Flow
    - Currently, each AI responds exactly once in round-robin style. To add more messages per AI or tweak the interaction order, see the logic in chat() route.


## Future Plans

- Multiple Messages Per Turn: Allow each AI to continue the conversation beyond a single response.
- Additional Personalities: Integrate more characters or split them across different models.
- Enhanced Front-end: Real-time streaming of tokens, improved UI/UX elements, or third-party chat integrations.
- Automatic Summaries: Summarize the conversation so far for each AI if contexts get large.

## Author
- Name: Jorges Nofulla
- Contact: jorgesnofulla12@gmail.com

Contributions and pull requests are welcome! If you have ideas for improvement or encounter issues, please open a GitHub issue.

Enjoy chatting with your two AI “personalities”! If you find this project useful, consider giving a star on GitHub and sharing your feedback.




