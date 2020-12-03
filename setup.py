import nltk
import search_engine

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet', quiet=True)

search_engine.main()