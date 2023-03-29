from flask import Flask, render_template, request
import requests
import json
import os
import openai

app = Flask(__name__)
openai.api_key = "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"

messages = []
question_list = []
answer_list = []

@app.route('/run', methods=['POST'])
def run_route():
    messages.clear()
    question_list.clear()
    answer_list.clear()
    print('clear...')
    return 'success'

@app.route('/', methods=['GET', 'POST'])
def home():
    messages.append(
        {"role": "system", "content": "You are a coding tutor bot to help user write and optimize python code."}
    )
    question = request.form.get('question')
    if question:
        answer = ask_chatGPT(question)
        print('\nq: ' + question + '\na: ' + answer )
        
        if question not in question_list: 
            question_list.append(question) 
            answer_list.append(answer)
    else:
        answer = ""
    print(question_list)
    return render_template('home.html', question_list=question_list, answer_list=answer_list)
    

def ask_chatGPT(prompt):
    
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    result = {"role": "assistant", "content": response["choices"][0]["message"].content}
    messages.append(result)
    return result["content"]


if __name__ == '__main__':
    app.run(debug=True)
    