import spacy
from datetime import datetime

import extract_tutorials, template_generation
import constants

nlp = spacy.load("en_core_web_md")

if __name__ == "__main__":
    headline, tutorials = extract_tutorials.predict_tutorials_from_url(constants.URL_TEST)
    template_string = template_generation.generate_template_dependency_parsing(tutorials)
    
    f = open("./output/[Template] {}.txt".format(headline), "a")
    f.write(template_string)
    f.close()
    print(headline)
    print(template_string)
