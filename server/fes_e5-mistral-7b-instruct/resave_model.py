from sentence_transformers import SentenceTransformer
from pathlib import Path
import os

# model_path = f"{Path.home()}\\.cache\\huggingface\\hub\\models--intfloat--e5-mistral-7b-instruct\\snapshots\\07163b72af1488142a360786df853f237b1a3ca1"
os.environ['SENTENCE_TRANSFORMERS_HOME'] = os.getenv(
  'SENTENCE_TRANSFORMERS_HOME',
  f"{Path.home()}\\.cache\\st"
#   f"{Path.home()}\\.cache\\huggingface\\hub"
)

# model_path = 'intfloat/multilingual-e5-large-instruct'
model_path = 'intfloat/e5-mistral-7b-instruct'

model = SentenceTransformer(model_path, model_kwargs={'torch_dtype': 'auto'})

print(next(model.parameters()).dtype)

# if float16
model.encode('Hello, World!') 
# array([ 0.02145 , -0.002232, -0.00882 , ...,  0.015305, -0.0109  ,
#         0.01468 ], dtype=float16)

# if float32
model.encode('Hello, World!')
# array([ 0.02142703, -0.00228734, -0.00875003, ...,  0.01534981,
#        -0.01086059,  0.01464904], dtype=float32)

model.half()

# float16
model.encode('Hello, World!')
# array([ 0.02145 , -0.002232, -0.00882 , ...,  0.015305, -0.0109  ,
        # 0.01468 ], dtype=float16)

path_to = f"{Path(__file__).parent.absolute()}\\.cache\\st\\models--intfloat--e5-mistral-7b-instruct"
# path_to = f"{Path(__file__).parent.absolute()}\\.cache\\st\\models--intfloat--e5-mistral-7b-instruct-halved"
model.save_pretrained(path_to)