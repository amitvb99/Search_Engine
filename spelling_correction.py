from spellchecker import SpellChecker


def correct_spelling(query_as_list):
    spell = SpellChecker()
    misspelled = spell.unknown(query_as_list)
    query_as_list = [term for term in query_as_list if term not in misspelled]
    for term in misspelled:
        query_as_list.append(spell.correction(term))
    return query_as_list


