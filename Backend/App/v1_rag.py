from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel
from .vecter_store import Vecter_Store
from fastapi import APIRouter
from fastapi.responses import JSONResponse

v1_router = APIRouter()

class RequestModel(BaseModel):
     question: str

class AnswerModel(BaseModel):
     code: int
     answer: str


def format_docs(docs):
    """検索結果のドキュメントをテキストに整形"""
    return "\n\n".join(doc.page_content for doc in docs)

# Vector Store インスタンス作成
vector_store = Vecter_Store()

prompt = """
あなたは質問応答のアシスタントです。質問に答えるために、検索された文脈の以下の部分を使用してください。答えがわからない場合は、わからないと答えましょう。回答は2文以内で簡潔に。

質問: {question}
コンテキスト: {context}
答え:
"""

# retriever を正しく取得
retriever = vector_store.get_retriever()
llm = ChatVertexAI(model="gemini-2.5-flash")
prompt_template = PromptTemplate.from_template(prompt)

# RAG チェーンを構築
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

@v1_router.post("/rag")
async def rag_chat(request:RequestModel) -> AnswerModel:
    # ユーザーからの質問を受け取る
    question = request.question.strip()
                    
    # 空の入力をスキップ
    if not question:
        return AnswerModel(code=400, answer="質問が空です")
    
    # RAG チェーンで回答を生成
    _answer = rag_chain.invoke(question)

    return AnswerModel(code=400, answer=_answer)
                