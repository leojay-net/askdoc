import openai
from decouple import config
import json
from openai import OpenAI


def get_response(problem, symptoms, medical_history):
    client = OpenAI(
        api_key=config("OPENAI_API_KEY")
    )


    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful medical assistant, You are diagnose and offer symptoms guidance and health tips, also emphasizing on how the the attention of a medical professional is needed regardless. You can also give out first aid things to do before seeking the attention of a medical professional "},
        {"role": "user", "content": "I am suffering from feeling really tired lately and I have been experiencing anemia and head aches. My medical history includes 'depression, unable to sleep'. What do I do?"},
        {"role": "assistant", "content": "I'm sorry to hear that you've been feeling tired and experiencing symptoms of anemia and headaches. Given your medical history of depression and difficulty sleeping, it's important to consult with a healthcare professional. Persistent fatigue can have various causes, including underlying medical conditions or inadequate sleep. Anemia may contribute to fatigue, and a thorough evaluation of your symptoms, medical history, and possibly further diagnostic tests will be essential.\
        It's crucial to address your mental health concerns as well. Depression and sleep disturbances can significantly impact your overall well-being. A healthcare provider can guide you through a comprehensive assessment and develop a tailored treatment plan, which may include lifestyle modifications, counseling, or medications.\
        Please prioritize seeking medical advice to ensure a comprehensive evaluation and appropriate management of your symptoms."},
        {"role": "user", "content": "I am suffering from persistent headache and I have been experiencing strong pains in my head, I also find it hard to sleep. My medical history includes ulcer, tiredness, unable to sleep well. What do I do?"},
        {"role": "assistant", "content": "I'm sorry to hear about your persistent headache and the associated symptoms. Strong head pains and difficulty sleeping could be caused by various factors. \
        Given your medical history of ulcer, it's crucial to consider this in your evaluation. Persistent headaches may be related to tension, stress, or potentially underlying medical conditions. \
        It's important to consult with a healthcare professional to conduct a thorough examination. In the meantime, try managing stress through relaxation techniques, maintaining a consistent sleep schedule, and avoiding trigger foods that may aggravate your ulcer. \
        Ensure you stay hydrated and consider over-the-counter pain relief if suitable. However, it's crucial to seek personalized medical advice to address your specific situation and determine the most appropriate course of action.\
        Please consult with a healthcare provider for a comprehensive assessment and tailored recommendations based on your medical history and current symptoms."},
        {"role": "user", "content": "I am suffering from "+ str(problem).replace('"', "'")+" and I have been experiencing "+str(symptoms).replace('"', "'")+". My medical history includes "+str(medical_history).replace('"', "'")+". What do I do?"}
    ],
    #response_format={"type": "json_object"},
    temperature=0.7,
        max_tokens=500,
        n=1,
        stop=None
    )
    obj = response.choices[0].message.content
    return obj

    

# result = get_response(problem="ulcer", symptoms="severe stomach pain and nausea", medical_history="low blood sugar")
# print(result)
