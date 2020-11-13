from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import TweetTokenizer
from document import Document
import re


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        tt = TweetTokenizer()
        text_tokens = tt.tokenize(text)
        # text_tokens = text.split(' ')
        text_tokens_without_stopwords = [w for w in text_tokens if w not in self.stop_words]
        text_tokens_after_rules = []

        url_pattern = re.compile(r'^http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+')
        hashtag_pattern = re.compile(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)')
        mention_pattern = re.compile(r'(?:@[\w_]+)')
        numbers_pattern = re.compile(r'(?:(?:\d+,?)+(?:\.?\d+)?)')
        fractions_pattern = re.compile(r'(-?\d+)/(-?\d+)')
        currency_pattren = re.compile(r'^[\$¢£€]?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(\.[0-9][0-9])?[\$¢£€]?$')
        for (i, token) in enumerate(text_tokens_without_stopwords):
            if hashtag_pattern.match(token):
                text_tokens_after_rules = text_tokens_after_rules + self.hashtag_rule(token[1:])
            elif url_pattern.match(token):
                text_tokens_after_rules = text_tokens_after_rules + self.URL_rule(token)
            elif mention_pattern.match(token):
                text_tokens_after_rules.append(token)
            # TODO: Upper-Lower case rule
            elif i+1 < len(text_tokens_without_stopwords):
                if token[-1] == '%' or text_tokens_without_stopwords[i+1].lower() == 'percent' or text_tokens_without_stopwords[i+1].lower() == 'percentage':
                    text_tokens_after_rules.append(self.percentage_rule(token))
                elif token.replace('.', '').replace(',', '').isdigit():
                    if text_tokens_without_stopwords[i+1].lower() == 'thousand':
                        text_tokens_after_rules.append(self.numbers_rule(token + '0'*3))
                    elif text_tokens_without_stopwords[i+1].lower() == 'million':
                        text_tokens_after_rules.append(self.numbers_rule(token + '0'*6))
                    elif text_tokens_without_stopwords[i+1].lower() == 'billion':
                        text_tokens_after_rules.append(self.numbers_rule(token + '0'*9))
                    elif fractions_pattern.match(text_tokens_without_stopwords[i+1]):
                        frac = text_tokens_without_stopwords[i+1]
                        text_tokens_after_rules.append(self.numbers_rule(token) + f' {frac}')
                next(enumerate(text_tokens_without_stopwords), None)

        return text_tokens_after_rules

    def hashtag_rule(self, text):
        if '_' in text:
            return text.split('_') + ['#' + text.replace('_', '')]

        else:
            splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text)).split()
            return [s.lower for s in splitted] + ['#' + text]

    def URL_rule(self, text):
        splitted = re.split("[, \-!?:.=\n/…]+", text)
        splitted[2] = splitted[2] + '.' + splitted[3]
        splitted.remove(splitted[3])
        return splitted

    def upper_lower_case_rule(self, text):
        pass

    def percentage_rule(self, text):
        if text[-1] == '%':
            return text
        else:
            return text + '%'

    def numbers_rule(self, text):
        number = float(text.split()[0].replace(',', ''))
        if number < 10**3:
            return str(number)
        elif 10**3 <= number < 10**6:
            return str(round(number / 10**3, 3)) + 'K'
        elif 10**6 <= number < 10**9:
            return str(round(number / 10**6, 3)) + 'M'
        else:
            return str(round(number / 10**9, 3)) + 'B'

    def name_entity_rule(self, text):
        pass

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
