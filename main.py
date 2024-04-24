# import
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate


# load the document and split it into chunks
loader = TextLoader("utils/state_of_the_union.txt", encoding="utf-8")
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)
embeddingsData = db.get(include=["embeddings"])


# VECTORS
vectors = embeddingsData["embeddings"]



query = "What did the president say about putin"

docs = db.similarity_search(query, k=5)
#print(docs[0])
# print results

# GENERATION #
 
#top five chunks by vector similarity
top_chunks = db.similarity_search_with_score(query, k=5)
i = 0

#prompt formatting
prompt = query + "\n\n" + "\n\n" 
for chunk, metada in top_chunks:
    document = chunk.page_content
    prompt += document + "\n\n"


 
#mount llm
llm = Ollama(model="llama2")
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

print('Generating...')
print(chain.invoke({"context":docs,"question":query}))


"""Generating...
Based on the provided context, the president said the following things about Putin:

1. "He badly miscalculated. He thought he could roll into Ukraine and the world would roll over. Instead, he met a wall of strength he never imagined."
2. "He rejected repeated efforts at diplomacy and thought the West and NATO wouldn’t respond. And he thought he could divide us at home."  
3. "We are enforcing powerful economic sanctions... cutting off Russia’s largest banks from the international financial system... choking off Russia’s access to technology that will sap its economic strength and weaken its military for years to come."
4. "The U.S. Department of Justice is assembling a dedicated task force to go after the crimes of Russian oligarchs."
5. "We see unity among leaders of nations and a more unified Europe, a more unified West... The world is clearly choosing the side of peace and security."
6. "Putin may circle Kyiv with tanks, but he will never gain the hearts and souls of the Ukrainian people... He will never extinguish their love of freedom."
7. "As I have made crystal clear, the United States and our allies will defend every inch of territory of NATO countries with the full force of our collective power."
8. "While Putin may make gains on the battlefield, he will pay a continuing high price over the long run."""