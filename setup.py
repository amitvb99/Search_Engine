import nltk
import search_engine_best

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet', quiet=True)

search_engine_best.main()
