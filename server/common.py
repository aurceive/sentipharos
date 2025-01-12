from logging import getLogger, StreamHandler, INFO, Formatter

logger = getLogger()
logger.setLevel(INFO)
handler = StreamHandler()
handler.setFormatter(Formatter('%(message)s'))
logger.handlers = [handler]

# TODO: Secure the keys
MONGO_URI = 'mongodb+srv://admin:admin@sentipharos.nnvrgyb.mongodb.net/?retryWrites=true&w=majority&appName=Sentipharos'
YOUTUBE_API_KEY = 'AIzaSyCNPYsFp3Gq8R8zeYaI0_AJi8C-Rc7EaAI'
FES_API_URL = 'https://fes-qrrel3xmdq-lz.a.run.app/predict'
