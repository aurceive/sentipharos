import os
from pathlib import Path

os.environ['HF_HOME'] = Path(__file__).parent.absolute().as_posix() + '/.cache/huggingface'
# model_name = 'intfloat/multilingual-e5-large-instruct'
model_name = 'intfloat/e5-mistral-7b-instruct'

# Use a pipeline as a high-level helper
# from transformers import pipeline
# pipe = pipeline("feature-extraction", model=model_name)

# Cкачиваем и кэшируем модель
from transformers import AutoTokenizer, AutoModel
AutoTokenizer.from_pretrained(model_name)
AutoModel.from_pretrained(model_name)