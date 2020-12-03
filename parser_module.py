from datetime import datetime
import os

from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import nltk
from configuration import ConfigClass

import utils
from document import Document
from stemmer import Stemmer
import re
import json
import string
import time


class Parse:

    num_of_docs = 0
    filename_counter = 0

    def __init__(self, config=ConfigClass(), group_size=500000):
        self.stop_words = stopwords.words('english')
        self.punctuators = [punc for punc in string.punctuation] + ['...', '']
        self.tt = TweetTokenizer()
        self.stemmer = Stemmer()
        self.need_stemming = config.toStem
        self.caps_dict = {}
        self.group_size = group_size
        if config.toStem:
            self.relpath = config.saveFilesWithStem
        else:
            self.relpath = config.saveFilesWithoutStem
        self.start_time = time.time()  # just for measuring time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'started at: {current_time}')

    def parse_sentence(self, text, urls=dict()):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param urls:
        :param text:
        :return:
        """

        text_tokens = self.tt.tokenize(text)
        # text_tokens_without_stopwords = [w for w in text_tokens if w not in self.stop_words + self.punctuators]
        # ---------------------- NAMED-ENTITY-RECOGNITION -------------------#
        # pos_tagged_tokens = pos_tag(text_tokens_without_stopwords)
        # named_entities = [tok for (tok, tag) in pos_tagged_tokens if tag == 'NNP' or tag == 'NNPS']
        # named_entities = []
        ######################################################################
        # text_tokens_without_entities = [w for w in text_tokens_without_stopwords if w not in named_entities]
        # text_tokens_without_entities = text_tokens_without_stopwords

        text_tokens_after_rules = []

        # regEx patterns
        url_pattern = re.compile(r'^http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+')
        hashtag_pattern = re.compile(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)')
        mention_pattern = re.compile(r'(?:@[\w_]+)')
        numbers_pattern = re.compile(r'(?:(?:\d+,?)+(?:\.?\d+)?)')
        fractions_pattern = re.compile(r'(-?\d+)/(-?\d+)')
        # emoji_pattern = \
        #     re.compile(r'(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])')
        # currency_pattren = re.compile(r'^[\$¢£€]?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(\.[0-9][0-9])?[\$¢£€]?$')

        for i, token in enumerate(text_tokens):
            if token.lower() in self.stop_words + self.punctuators:
                continue

            maybe_ent = ''
            if token[0].isupper():
                maybe_ent += token
                text_tokens.remove(token)
                if len(text_tokens) > i:
                    token = text_tokens[i]
                while token[0].isupper():
                    maybe_ent += ' ' + token
                    text_tokens.remove(token)
                    if len(text_tokens) > i:
                        token = text_tokens[i]
                if maybe_ent[0].isupper():
                    self.caps_dict[maybe_ent.lower()] = False
                    self.check_capital(maybe_ent)
                    if len(maybe_ent.split()) == 1:
                        text_tokens_after_rules += [maybe_ent.lower()]
                    else:
                        text_tokens_after_rules += [maybe_ent.lower()] + [tok.lower() for tok in maybe_ent.split()]

            if token.lower() in self.stop_words + self.punctuators:
                continue

            if hashtag_pattern.match(token):
                text_tokens_after_rules += self.stemming_rule(self.hashtag_rule(token[1:]))

            elif url_pattern.match(token):
                if token in urls:
                    url = urls[token]
                    if url is not None:
                        text_tokens_after_rules += self.URL_rule(url)

            elif mention_pattern.match(token):
                text_tokens_after_rules += self.stemming_rule([token])

            elif numbers_pattern.match(token):
                if numbers_pattern.match(token).span() == (0, len(token)):
                    if i+1 < len(text_tokens):
                        if text_tokens[i+1].lower() in ['percent', 'percentage', '%']:
                            per = text_tokens[i+1]
                            text_tokens_after_rules += [self.numbers_rule(token)[0] + '%']
                            text_tokens.remove(per)

                        elif text_tokens[i+1] in ['$', '¢', '£', '€']:
                            sign = text_tokens[i+1]
                            text_tokens_after_rules += [sign + self.numbers_rule(token)[0]]

                        elif token.replace('.', '').replace(',', '').isdigit():
                            zeros_dict = {'thousand': '0' * 3, 'million': '0' * 6, 'billion': '0' * 9}
                            multiplier = text_tokens[i+1]
                            if multiplier.lower() in zeros_dict.keys():
                                text_tokens_after_rules += self.numbers_rule(token + zeros_dict[multiplier.lower()])
                                text_tokens.remove(multiplier)

                            elif fractions_pattern.match(text_tokens[i+1]):
                                frac = text_tokens[i+1]
                                text_tokens_after_rules += [self.numbers_rule(token)[0] + f' {frac}']
                                text_tokens.remove(frac)

                            else:
                                text_tokens_after_rules += self.numbers_rule(token)
                        elif token[-1].upper() in ['K', 'M', 'B']:
                            zeros_dict = {'K': '0' * 3, 'M': '0' * 6, 'B': '0' * 9}
                            multiplier = token[-1]
                            text_tokens_after_rules += self.numbers_rule(token[:-1] + zeros_dict[multiplier.upper()])
                        elif token[-2:].upper() in ['BN']:
                            zeros_dict = {'BN': '0' * 9}
                            multiplier = token[-2:]
                            text_tokens_after_rules += self.numbers_rule(token[:-2] + zeros_dict[multiplier.upper()])
                    else:
                        text_tokens_after_rules += self.numbers_rule(token)
                else:
                    text_tokens_after_rules += self.stemming_rule([token])

            else:
                text_tokens_after_rules += self.stemming_rule([token])

        text_tokens_after_rules = [w for w in text_tokens_after_rules if w not in self.stop_words]

        return text_tokens_after_rules

    def hashtag_rule(self, text):
        if '_' in text:
            return text.lower().split('_') + ['#' + text.lower().replace('_', '')]

        else:
            splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text)).split()
            return [s.lower() for s in splitted] + ['#' + text.lower()]

    def URL_rule(self, text):
        splitted = re.split("[, \-!?:=\n/…]+", text)
        splitted[1:1] = splitted[1].split('.', maxsplit=1)
        splitted.remove(splitted[3])
        without_empty = [s for s in splitted if s != '']
        return without_empty

    def numbers_rule(self, text):
        number_str = text.split()[0].replace(',', '')
        if '.' in number_str:
            number = float(number_str)
        else:
            number = int(number_str)
        if number < 10**3:
            return ["{:.3f}".format(number).strip('0').strip('.')]
        elif 10**3 <= number < 10**6:
            return ["{:.3f}".format(number / 10**3).strip('0').strip('.') + 'K']
        elif 10**6 <= number < 10**9:
            return ["{:.3f}".format(number / 10**6).strip('0').strip('.') + 'M']
        else:
            return ["{:.3f}".format(number / 10**9).strip('0').strip('.') + 'B']

    def stemming_rule(self, tokens):
        if self.need_stemming:
            after_tokens = []
            for token in tokens:
                after_tokens.append(self.stemmer(token))
            return after_tokens
        else:
            return tokens

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """

        self.num_of_docs += 1

        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        urls = json.loads(url)
        tokenized_text = self.parse_sentence(full_text, urls)
        parsed_text = [tok for tok in tokenized_text if tok not in self.stop_words + self.punctuators]

        # # urls rule
        # parsed_urls = [term for term in parsed_urls_with_puncs if term not in self.punctuators]

        doc_length = len(parsed_text)  # after text operations.

        for term in parsed_text:
            if term not in term_dict.keys():
                if term[:1].isupper():
                    term_dict[term.upper()] = 1
                else:
                    term_dict[term.lower()] = 1
            else:
                if term[:1].isupper():
                    term_dict[term.upper()] += 1
                else:
                    term_dict[term.lower()] += 1

        for term in [key for key in term_dict.keys() if key.islower()]:
            if term.upper() in term_dict.keys():
                term_dict[term] += term_dict.pop(term.upper())

        if self.num_of_docs % self.group_size == 0:
            self.write_file()
            checkpiont = time.time() - self.start_time
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'parsed {self.num_of_docs} documents, checkpoint time: {checkpiont}, time now: {current_time}')

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document

    def check_capital(self, token):
        if len(token.split()) > 1:
            for word in token.split():
                if word.lower() not in self.caps_dict.keys():
                    if word[0].isupper():
                        self.caps_dict[word.lower()] = False
                    else:
                        self.caps_dict[word.lower()] = True
                else:
                    if word[0].islower():
                        self.caps_dict[word.lower()] = True

    def write_file(self):
        utils.save_obj(self.caps_dict,
                       os.path.join(os.path.join(self.relpath, 'CapitalLetters'), f'cl{self.filename_counter}'))
        self.caps_dict = {}
        self.filename_counter += 1
