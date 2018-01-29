# -*- coding: utf-8 -*-
from chatterbot import ChatBot

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Bob',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

chatbot.train("chatterbot.corpus.english")

# 載入(簡體)中文的基本語言庫
chatbot.train("chatterbot.corpus.chinese")

# 載入(簡體)中文的問候語言庫
#chatbot.train("chatterbot.corpus.chinese.greetings")

# 載入(簡體)中文的對話語言庫
#chatbot.train("chatterbot.corpus.chinese.conversations")

# Get a response to the input text 'How are you?'
response = chatbot.get_response('今天天氣怎樣')

print(response)