from pprint import pprint
import torch.nn.functional as F, os, pathlib
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

model_name = 'intfloat/multilingual-e5-large-instruct'

# Определение функции average_pool для усреднения с attention_mask
def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
  last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
  return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

# Инициализация модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

input_texts = "Today is a sunny day and I will get some ice cream."

# Токенизация текста с включением attention_mask
batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')
outputs = model(**batch_dict)

# Применение average_pool и нормализация
embeddings = average_pool(outputs.last_hidden_state, batch_dict.attention_mask)
embeddings = F.normalize(embeddings, p=2, dim=1)  # Нормализуем эмбеддинги

# Пример расчета cosine similarity для сравнения
# scores = (embeddings[:2] @ embeddings[2:].T) * 100
pprint(embeddings[0].tolist())

# 0.003874944057315588
# 0.003874944057315588
# 0.003874944057315588
# 0.0038749086670577526
# 0.0038749086670577526
# 0.0038749086670577526