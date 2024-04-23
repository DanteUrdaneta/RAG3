from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_text_splitters import CharacterTextSplitter


# open the text file
loader = TextLoader("utils/test.txt", encoding='utf-8')
documents = loader.load()


# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") # we need to use OPENAI EMBEDDINGS

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)

# query it
query = "what does rag in langchain stand for?"
docs = db.similarity_search(query)

# print results
print(docs[0].page_content)
