from openai import OpenAI
import streamlit as st
import requests
import json

url = 'http://143.198.98.88/v1/workflows/run'
api_key = 'app-Sf1R3YdJez2Um2pxGNf7T8KZ'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Ottieni una chiave API OpenAI](https://platform.openai.com/account/api-keys)"

st.title("💬 Guida al Business Plan")
st.caption("🚀 A Streamlit chatbot powered by Umberto Past President")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Sono un assistente addestrato sulla Guida al Business Plan dell'ODCEC di Milano. Come posso aiutarti?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    data = {
        'inputs': {'question': prompt},
        'response_mode': 'blocking',
        'user': 'Streamlit'
    }

    response = requests.post(url, headers=headers, json=data)
    embeddings = response.json()["data"]["outputs"]["response"]

    filtered_embeddings = []
    for emb in embeddings:
        if emb["metadata"]['score'] > 0.8:
            filtered_embeddings.append(emb)

    if filtered_embeddings:
        prompt_with_embeddings = prompt + "\n Contesto:" + json.dumps(filtered_embeddings)
    else:
        prompt_with_embeddings = None

    st.session_state.messages.append({"role": "user", "content": prompt_with_embeddings if filtered_embeddings else prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
