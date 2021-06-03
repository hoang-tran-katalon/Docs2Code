import spacy
from datetime import datetime

import extract_tutorials
import constants


nlp = spacy.load("en_core_web_md")

def generate_template_dependency_parsing(tutorials):
    
    template = []
    template_string = '<Start> => '

    for tutorial in tutorials:
        tutorial = tutorial.replace('to ', '').replace(',', '')
        doc = nlp(tutorial)
        
        for chunk in list(doc.noun_chunks):
            if chunk.root.dep_ in ['dobj', 'nsubj'] and chunk.root.head.dep_ in ['ROOT', 'conj', 'advcl']:
                result = (chunk.root.head.text.capitalize(), chunk.text)
                template.append(result)
                template = [item for item in template if item[0] not in ['Receive', 'Is', 'Happen']]
                
                template_string+=chunk.root.head.text.capitalize()+' '+chunk.text
                template_string+=' => '

    template_string+='<End>'

    return template_string