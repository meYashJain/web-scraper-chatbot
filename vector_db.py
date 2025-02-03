from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_core.documents import Document  # Add this import

class VectorDatabase:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_store = None

    def process_and_store(self, scraped_data):
        """Process documents and store in vector database"""
        # Create a LangChain Document object
        document = Document(
            page_content=scraped_data['content'],
            metadata={"source": scraped_data['url'], "domain": scraped_data['domain']}
        )
        
        chunks = self.text_splitter.split_documents([document])
        self.vector_store = Chroma.from_documents(
            chunks,
            self.embedding,
            persist_directory="./chroma_db"
        )
        return len(chunks)

    def search(self, query, k=3):
        """Search for relevant documents"""
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=k)