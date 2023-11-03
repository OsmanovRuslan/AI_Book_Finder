from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import string
from nltk.tokenize import word_tokenize
import pandas as pd
import nltk
# скачивание специальных данных
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess

# загрузка данных из CSV-файла
data = pd.read_csv('books.csv')
# предобработка текста
stop_words = set(stopwords.words('russian'))


def preprocess_text(text):
    tokens = word_tokenize(text.lower())

    # Удаление пунктуации и стоп-слов
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]

    return tokens


documents = [TaggedDocument(words=preprocess_text(title + ' ' + description), tags=[i]) for i, (title, description) in
             enumerate(data.values)]  # создаются документы и образуется корпус

# создание модели
model = Doc2Vec(documents, vector_size=60, window=5, min_count=2, workers=4, epochs=20)

# сохранение модели в файл
model.save('doc2vec.model')

