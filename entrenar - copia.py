import os
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    DirectoryLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# =========================
# 1. CONFIGURACIÓN INICIAL
# =========================
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_CONOCIMIENTO = os.path.join(BASE_DIR, "conocimiento")
RUTA_DB = os.path.join(BASE_DIR, "src", "db", "vector_db")


def iniciar_entrenamiento():
    print("🚀 Iniciando proceso de entrenamiento RAG...")

    # Validar carpeta de conocimiento
    if not os.path.exists(RUTA_CONOCIMIENTO):
        print("❌ Error: La carpeta 'conocimiento' no existe.")
        return

    docs = []

    try:
        # =========================
        # 2. CARGAR ARCHIVOS WORD
        # =========================
        print("📄 Buscando archivos Word...")
        loader_word = DirectoryLoader(
            RUTA_CONOCIMIENTO,
            glob="**/*.docx",
            loader_cls=UnstructuredWordDocumentLoader
        )

        docs_word = loader_word.load()
        docs.extend(docs_word)
        print(f"✅ Word cargados: {len(docs_word)} documentos.")

        # =========================
        # 3. CARGAR ARCHIVOS PDF
        # =========================
        print("📄 Buscando archivos PDF...")
        loader_pdf = DirectoryLoader(
            RUTA_CONOCIMIENTO,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )

        docs_pdf = loader_pdf.load()
        docs.extend(docs_pdf)
        print(f"✅ PDF cargados: {len(docs_pdf)} páginas.")

        if not docs:
            print("⚠️ No se encontró ningún archivo para procesar.")
            return

        # =========================
        # 4. DIVISIÓN DE TEXTO
        # =========================
        print("✂️ Dividiendo documentos en fragmentos...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

        splits = text_splitter.split_documents(docs)
        print(f"✅ Fragmentos generados: {len(splits)}")

        # =========================
        # 5. EMBEDDINGS (LOCAL)
        # =========================
        print("🧠 Generando embeddings locales...")

        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # =========================
        # 6. CREAR BASE VECTORIAL
        # =========================
        print("💾 Creando base vectorial (Chroma)...")

        # Asegurar que la carpeta exista
        os.makedirs(RUTA_DB, exist_ok=True)

        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=RUTA_DB
        )

        vectorstore.persist()

        print("\n" + "=" * 40)
        print("🎉 ENTRENAMIENTO COMPLETADO")
        print(f"📁 Base vectorial guardada en: {RUTA_DB}")
        print("=" * 40)

    except Exception as e:
        print(f"❌ Error inesperado: {e}")


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    iniciar_entrenamiento()