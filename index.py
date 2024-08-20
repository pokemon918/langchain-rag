from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory

history = FileChatMessageHistory('chat_history.json')
memory = ConversationBufferMemory(
    memory_key='chat_history',
    chat_memory=history,
    return_messages=True
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

prompt = ChatPromptTemplate(
    input_variables=['content'],
    messages=[
        SystemMessage(content='You are chatbot having a conversation with a human.'),
        MessagesPlaceholder(variable_name='chat_history'),
        HumanMessagePromptTemplate.from_template('{content}')
    ]
)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=False
)

while True:
    content = input('Your prompt: ')
    if content in ['quit', 'exit', 'bye']:
        print('Goodbye!')
        break

    response = chain.run({'content': content})
    print(response)
    print('-' * 50)