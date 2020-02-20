import re
from unidecode import unidecode
import spacy
nlp = spacy.load('fr_core_news_md')


# To be removed
d = "_" or "|" or "/" or ":" or ","

# To be replaced
r = "'"

# To be removed for search entity
stop = "d'" or "l'" or "de" or "le" or "à"

# Location indicators
loc = 'rue avenue boulevard allée chemin route parvis place cité'

# URL regex
urlreg = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

# HTML cleaner
html_cleaner = re.compile('<.*?>')


def format_entry(entry):
    return unidecode(entry.lower().replace(d, "").replace(r, " ").replace("&", "%26"))


def format_query(entry):
    return entry.replace(" ", "+")


def format_goo_txt(entry):
    return entry.replace("\xa0", " ")


def entity_strict_match(entry, entity):
    # Verify every terms of the user input
    # are in the returned named entity
    # and so without extra terms
    f_entry = entry.replace(stop, "")
    n_entry = len(f_entry.split())
    f_entity = format_entry(entity).replace(stop, "").split()
    if n_entry == len(f_entity) and all(item in f_entry for item in f_entity):
        return entity
    else:
        return None


def entity_lazy_match(entry, entity):
    # Verify some terms of the user input
    # are in the returned named entity
    f_entry = entry.replace(stop, "")
    f_entity = format_entry(entity).replace(stop, "").split()
    if any(item in f_entry for item in f_entity):
        return entity
    else:
        return None


def location_check(entry):
    # Verify the address is a location
    f_place = entry.lower().split()
    ref = nlp(entry.lower())
    ner = [ent.label_ for ent in ref.ents]
    if any(elt in loc for elt in f_place) or 'LOC' in ner:
        return entry
    else:
        return None


def get_ner(doc):
    text = re.sub(html_cleaner, '', doc)
    doc = nlp(text.lower())
    ent_dict = {}
    for ent in doc.ents:
        ent_dict.update({'entity': ent.text, 'type': ent.label_})
    return ent_dict


def get_ner_(doc):
    text = re.sub(html_cleaner, '', doc)
    doc = nlp(text.lower())
    ner = [ent.text for ent in doc.ents]
    if len(ner) > 0:
        keywords = list(dict.fromkeys(ner))
        return keywords
