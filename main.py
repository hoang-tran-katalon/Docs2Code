import spacy

import extract_tutorials
import constants

nlp = spacy.load("en_core_web_md")

if __name__ == "__main__":
    tutorials = extract_tutorials.predict_tutorials_from_url(constants.URL_TEST)
    

    sent = ' '.join(tutorials)
    doc = nlp(sent)

    template = []
    for chunk in list(doc.noun_chunks):
        if chunk.root.dep_ in ['dobj', 'nsubj'] and chunk.root.head.dep_ in ['ROOT', 'conj', 'advcl']:
            result = (chunk.root.head.text.capitalize(), chunk.text)
            template.append(result)
            
            template = [item for item in template if item[0] not in ['Receive', 'Is', 'Happen']]
    print(template)
