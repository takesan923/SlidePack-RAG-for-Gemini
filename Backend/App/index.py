from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from vecter_store import Vecter_Store
from pathlib import Path

import os


vector_store = Vecter_Store()

# プロジェクトルートを基準にした絶対パス
project_root = Path(__file__).parent.parent
doc_files = [
    project_root / "Doc" / "slidepack_api_endpoints.md",
    project_root / "Doc" / "slidepack_data_json.md"
]

# Markdown見出しを優先した区切り設定
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,  # 見出し単位なのでサイズを大きめに調整
    chunk_overlap=200,
    separators=[
        "\n# ",      # H1見出し
        "\n## ",     # H2見出し  
        "\n### ",    # H3見出し
        "\n#### ",   # H4見出し
        "\n\n\n",    # 空行3つ
        "\n\n",      # 空行2つ
        "\n",        # 改行
        ".",         # 文の区切り
        ",",         # カンマ
        " ",         # スペース
        "\u200b",    # Zero-width space
        "\uff0c",    # Fullwidth comma
        "\u3001",    # Ideographic comma
        "\uff0e",    # Fullwidth full stop
        "\u3002",    # Ideographic full stop
        "",
    ],
)

# すべてのドキュメントを読み込んでDocumentオブジェクトを作成
documents = []
for file_path in doc_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # ファイルごとに分割してメタデータを付与
            chunks = text_splitter.split_text(content)
            for i, chunk in enumerate(chunks):
                documents.append(Document(
                    page_content=chunk,
                    metadata={
                        "source": file_path,
                        "chunk_id": i,
                        "total_chunks": len(chunks)
                    }
                ))

# ベクトルストアに追加
if documents:
    vector_store.add_documents(documents)
    print(f"追加されたドキュメント数: {len(documents)}")
else:
    print("読み込まれたドキュメントがありません")