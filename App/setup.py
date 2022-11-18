import streamlit as st
import json
import requests


API_URL = 'https://api-inference.huggingface.co/models/makarshatilov/transliteration_v1'
TOKEN = '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'
PREFIX = '<pe>'
headers = {"Authorization": f"Bearer {TOKEN}"}
st.title('Транслитерация')
hint_text = "**Здесь будет вывод на фарси** 👇"
error_text = '**Нужно загрузить модель, для этого [перейдите на страницу модели](https://huggingface.co/makarshatilov/transliteration_v1), нажмите Compute, немного подождите пока модель не загрузится, а затем перезагрузите текущую страницу**'

text = st.text_input(label='Введите текст на таджикском')
print(text)


def query(payload):
    response = requests.post(API_URL, headers=headers, data=payload)
    return json.loads(response.content.decode("utf-8"))


if text:
    json_data = {"inputs": [PREFIX + text.capitalize()], "parameters": {
        "max_length": 25, "num_beams": 10, "length_penalty": 0.1}}
    data = json.dumps(json_data)
    response = query(data)
    if ('error' in response):
        st.markdown(error_text, unsafe_allow_html=False)
    else:
        st.markdown(hint_text)
        st.write(response[0]["generated_text"])
else:
    st.markdown(hint_text)
