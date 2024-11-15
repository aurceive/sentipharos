from sentence_transformers import SentenceTransformer
from pprint import pprint

model_name = 'intfloat/multilingual-e5-large-instruct'
model = SentenceTransformer(model_name)

input_texts = "Today is a sunny day and I will get some ice cream."

embeddings = model.encode(input_texts, normalize_embeddings=True)

pprint(embeddings.tolist())