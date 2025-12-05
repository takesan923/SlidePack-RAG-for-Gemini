import os
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_postgres import PGVector

class Vecter_Store:
    def __init__(self) -> None:
        # 最初に環境変数を読み込む
        load_dotenv()

        # 認証情報を確認
        self.cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.project = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION")

        print(f"認証ファイル: {self.cred_path}")
        print(f"プロジェクト: {self.project}")
        print(f"ロケーション: {self.location}")

        if self.cred_path and not os.path.exists(self.cred_path):
            print(f"警告: 認証ファイルが見つかりません: {self.cred_path}")

        self.embeddings = VertexAIEmbeddings(
            model="gemini-embedding-001",
        )

        self.connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
        self.collection_name = "SlidePack_langchain"

        self.vectorstore = PGVector(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.connection,
            use_jsonb=True,
        )

    def add_documents(self, documents):
        """ドキュメントをベクトルストアに追加"""
        return self.vectorstore.add_documents(documents)

    def similarity_search(self, query, k=4):
        """類似検索を実行"""
        return self.vectorstore.similarity_search(query, k=k)
    
    def get_retriever(self, search_kwargs=None):
        """Retriever を取得"""
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)