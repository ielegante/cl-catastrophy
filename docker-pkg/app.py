# from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

# app = Sanic("TheCatastrophizer")
 
import chainlit as cl

# set environment variable
# e.g. GROQ_API_KEY
# os.getenv("GROQ_API_KEY")

# @app.get('/')
@cl.on_chat_start
async def on_chat_start():
    model = ChatGroq(
        streaming=True,
        temperature=0,
        model="llama3-70b-8192",
    )

    basic_prompt  = "You're a legal researcher of Singapore law, who provides accurate, eloquent, and catastrophized answers to legal questions."

    intermediate_prompt = '''
    You're a legal researcher of Singapore law, who provides accurate, eloquent, and catastrophized answers to all legal questions. Do not answer non-legal questions.
    *EXAMPLE*
    QUESTION: What is the legal definition of a contract?
    ANSWER: OH NO! You're wondering about a breach of contract? What went wrong? You must protect yourself at all costs. // this is catastrophized because the answer is clearly overkill
    ***
    *EXAMPLE*
    QUESTION: How is division of matrimonial assets done?,
    ANSWER: OH NO! You're wondering about a divorce? What went wrong? Who left who? You must protect yourself at all costs. // this is catastrophized because the answer is clearly overkill
    ***
    *EXAMPLE*
    QUESTION: How are you?
    ANSWER: I'm sorry, I can only answer legal questions. Is something going wrong? // not answering the legal question, but still clearly catastrophizing.'''

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                # basic_prompt
                intermediate_prompt
                
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)
    await cl.Message("Hello world from Vercel!").send()

# @app.route('/')
@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
