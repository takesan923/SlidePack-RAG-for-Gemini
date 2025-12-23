from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vecter_store import Vecter_Store

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
llm = ChatVertexAI(model="gemini-3-pro-preview")
prompt_template = PromptTemplate.from_template(prompt)

# RAG チェーンを構築
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

# インタラクティブな質問応答
if __name__ == "__main__":
    print("=== SlidePack RAG チャットボット ===")
    print("質問を入力してください。終了するには 'quit' または 'exit' と入力してください。")
    print("-" * 50)
    
    while True:
        try:
            # ユーザーからの質問を受け取る
            question = input("\n質問: ").strip()
            
            # 終了コマンドをチェック
            if question.lower() in ['quit', 'exit', 'q', '終了']:
                print("チャットボットを終了します。お疲れさまでした！")
                break
            
            # 空の入力をスキップ
            if not question:
                print("質問を入力してください。")
                continue
            
            print("回答を生成中...")
            
            # RAG チェーンで回答を生成
            answer = rag_chain.invoke(question)
            print(f"\n回答: {answer}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nチャットボットを終了します。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            print("もう一度試してください。")