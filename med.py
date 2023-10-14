import pandas as pd
import re
from nltk.corpus import wordnet
import warnings
warnings.filterwarnings('ignore')
import random
from difflib import SequenceMatcher
import streamlit as st
import uuid

st.title('MedBot')
# Introductory message for MedBot
intro_message = "Hi! I am MedBot. You can ask me anything regarding MENTAL HEALTH, and I shall try my best to answer them."
st.markdown(intro_message)
# Initialize the messages attribute if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add more greeting words
greeting = [
    'hey', 'whats up', 'good morning', 'good evening', 'morning', 'evening',
    'hello there', 'hey there', 'hi', 'howdy', 'greetings', 'hi there'
]

synonyms = []
for word in greeting:
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            lem_name = re.sub(r'\[[0-9]*\]', ' ', lem.name())
            lem_name = re.sub(r'\s+', ' ', lem_name)
            synonyms.append(lem_name)

# inputs for greeting
greeting_inputs = ['hey', 'whats up', 'good morning', 'good evening', 'morning', 'evening', 'hello there', 'hey there']
# concatenating the synonyms and the inputs for greeting
greeting_inputs = greeting_inputs + synonyms
# inputs for a normal conversation
convo_inputs = ['how are you', 'how are you doing', 'you good']
# greeting responses by the bot
greeting_responses = ['Hello! How can I help you?',
                      'Hey there! So what do you want to know?',
                      'Hi, you can ask me anything regarding MENTAL HEALTH.',
                      'Hey! wanna know about MENTAL HEALTH? Just ask away!']
# conversation responses by the bot
convo_responses = ['Great! what about you?', 'Getting bored at home :( wbu??', 'Not too shabby']
# conversation replies by the user
convo_replies = ['great', 'i am fine', 'fine', 'good', 'super', 'superb', 'super great', 'nice']
# few limited questions and answers given as dictionary
question_answers = {'what are you': 'I am MEdBot',
                    'who are you': 'I am MEdBot',
                    'what can you do': 'Answer questions regarding MENTAL HEALTH!',
                    'what do you do': 'Answer questions regarding MENTAL HEALTH!'}

# Load your dataset from a Parquet file
data = pd.read_csv('mental_health_qa_dataset.csv')

# Convert the dataset into a format suitable for your chatbot
# In this example, we create a dictionary where questions are keys and answers are values
qa_dict = dict(zip(data['User Question'], data['Chatbot Response']))



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    generated_text = ""

if prompt in greeting_inputs:
    generated_text = random.choice(greeting_responses)
elif prompt in convo_inputs:
    generated_text = random.choice(convo_responses)
elif prompt in question_answers:
    generated_text = question_answers[prompt]
else:
    best_similarity = 0.0
    best_match = None

    if prompt is not None:
        for question, answer in qa_dict.items():
            if question is not None:
                similarity = SequenceMatcher(None, prompt, question).ratio()
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = answer
        generated_text = best_match

message_placeholder.markdown(generated_text)
st.session_state.messages.append({"role": "assistant", "content": generated_text})




