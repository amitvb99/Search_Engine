from nltk.corpus import wordnet as wn


def expand_query(query_as_list, stop_words):
    """
    This function expands the query using the WordNet method.
    :param query_as_list: The query to expand as a list of terms.
    :param stop_words: The stop words we need to ignore while expanding the query
    :return: The expanded query as list of terms.
    """

    wordnet_expantion = set()
    for term in query_as_list:
        synsets = wn.synsets(term)
        if len(synsets) != 0:
            for l in synsets[0].lemma_names():
                wordnet_expantion |= set(l.split('_'))
            wordnet_expantion -= {term}
            hypernyms = synsets[0].hypernyms()
            if len(hypernyms) != 0:
                for l in hypernyms[0].lemma_names():
                    wordnet_expantion |= set(l.split('_'))

    query_as_list += [term for term in wordnet_expantion if term not in stop_words]

    return query_as_list
