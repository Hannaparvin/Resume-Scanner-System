import re                                                           #Regular expression library for pattern matching
import spacy                                                        #NLP library for natural language processing

nlp = spacy.load("en_core_web_sm")                                  # Load the English language model


#Cleaning and normalizing the skill text
def preprocess_text(text):

    text = text.lower()
    text = text.replace("-", " ")
    text = text.replace("/", " ")
    text = re.sub(r'[^a-zA-Z0-9\s+.#]', ' ', text)                 #Remove special characters.
    
    return text


#Extract years of experience from the text
def extract_experience(text):

    text = text.lower()

    patterns = [                                                #list of regex patterns.
        
        r'(\d+)\+?\s+years',
        r'(\d+)\+?\s+yrs',
        r'experience\s+of\s+(\d+)',
        r'(\d+)\s+year'
    ]

    years = []                                                  #it will store the extracted years of experience.

    for pattern in patterns:                                    #checks each pattern in the list of patterns to find matches in the text.
        matches = re.findall(pattern, text)                     #returns all matches.
        years.extend(matches)                                   #adds the matches to the years list.
                                        
    if years:                                                   #checks whether the list is empty.
        years = [int(year) for year in years]                   #it converts the extracted years from string to integer.
        return max(years)                                       #returns the maximum value from the list.
    
    return 0

#Extract named entities from the text using spaCy's NLP model.
def extract_entities(text):

    doc = nlp(text)                                            #converts text into a spaCy document object for processing.

    entities = []                                             #it will store the extracted named entities.

    for ent in doc.ents:                                      #doc.ents contains recognized entities.

        entities.append({                                     #adds entity data as a dictionary

            "text": ent.text,                                 #stores the actual entity.

            "label": ent.label_                              #stores the type of entity (e.g., PERSON, ORG, DATE, etc.).
        })

    return entities