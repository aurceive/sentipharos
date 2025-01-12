from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, torch, asyncio, shutil

app = FastAPI()

# Модель данных для запросов и ответов
class Request(BaseModel):
  inputs: str | list[str]

class Response(BaseModel):
  model: str
  outputs: list[float] | list[list[float]]

# Инициализация модели
# from pathlib import Path
# model_path = f'{Path(__file__).parent.parent.absolute()}\\.cache\\st\\models--intfloat--e5-mistral-7b-instruct'
model_name = 'intfloat/e5-mistral-7b-instruct'
model_path = '/root/.cache/st/models--intfloat--e5-mistral-7b-instruct'
torch.set_default_dtype(torch.float16)
with torch.inference_mode(): model = SentenceTransformer(model_path)

# Освобождаем память от ненужных файлов
if os.path.exists(f'{model_path}') and os.path.isdir(f'{model_path}'):
  shutil.rmtree(f'{model_path}')

# Переключаем модель на использование float32
with torch.inference_mode(): model.to(dtype=torch.float32)
print(f'Model dtype: {next(model.parameters()).dtype}')


@app.get('/', response_class=HTMLResponse)
async def root():
  return (
    '<head>'
    '<title>FES</title>'
    '</head>'
    '<h1>Feature extraction service is running.</h1>'
    f'<p>Model: {model_name}</p>'
    f'<p>Model dtype: {next(model.parameters()).dtype}</p>'
  )


@app.post('/predict')
async def predict(request: Request):
  if not request.inputs:
    raise HTTPException(status_code=400, detail='No inputs provided')

  batch_size = 1 if isinstance(request.inputs, str) else len(request.inputs)
  
  # Асинхронно выполняем код, который запускает модель
  with torch.inference_mode():
    embeddings = await asyncio.to_thread(
      lambda: model.encode(request.inputs, normalize_embeddings=True, batch_size=batch_size)
    )

  response = Response(model=model_name, outputs=embeddings.tolist())
  # Очищаем оперативную память
  del embeddings, request
  return response.model_dump()








# print(f'CPU count: {os.cpu_count()}')
# print(f'GPU count: {torch.cuda.device_count()}')
# print(f'PyTorch cuda available: {torch.cuda.is_available()}')
# print(f'Device: {SentenceTransformer().device}')
# print(f'PyTorch MKLDNN available: {torch.backends.mkldnn.is_available()}')
# print(f'MPS available: {torch.backends.mps.is_available()}')
# print(f'BFloat16 supported: {torch.cpu._is_avx512_bf16_supported()}')
# print(f'Default tensor type: {torch.get_default_dtype()}')
# print(f'Default number of threads: {torch.get_num_threads()}')
# torch.set_num_threads(os.cpu_count() or 1)
# print(f'Using {torch.get_num_threads()} threads for PyTorch')
# # torch.set_default_tensor_type(torch.BFloat16Tensor)
# torch.set_default_dtype(torch.float16)
# print(f'Using {torch.get_default_dtype()} as default dtype for PyTorch')
# print(torch.__config__.show())