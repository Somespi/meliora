from collections import Counter
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from typing import List
from pathlib import Path

nlp = spacy.load("en_core_web_md")
extras = set(STOP_WORDS).union(set(punctuation)).union({'\n'})

with open(Path(__file__).parent / "includes" / "common_titles.txt", "r") as f:
    commons = set(f.read().split('\n'))

def find_most_relevant_keyword(text: str, similarity_words: List[str]) -> str:
    def calculate_similarity(token, word):
        return token.similarity(nlp(word))
    
    def get_most_similar_keyword(token):
        similarities = {common: calculate_similarity(token, common) for common in commons}
        max_similarity = max(similarities.values())
        if max_similarity >= 0.57:
            return max(similarities, key=similarities.get)
        for similar in similarity_words:
            if calculate_similarity(token, similar) >= 0.6:
                return similar
        return token.text
    
    doc = nlp(text)
    words = (token.text for token in doc if token.text.lower() not in extras and token.text.isalpha())
    word_counter = Counter(words)
    
    if not word_counter:
        return None
    
    important = word_counter.most_common(1)[0][0]
    
    def find_keywords(word_list):
        if len(word_list) >= 3:
            text = " ".join(word_list[:3])
            doc = nlp(text)
            del word_list[:3]
            
            for token in doc:
                keyword = get_most_similar_keyword(token)
                if keyword:
                    return keyword
            return find_keywords(word_list)
        
        elif len(word_list) == 2:
            text = " ".join(word_list)
            doc = nlp(text)
            
            for token in doc:
                keyword = get_most_similar_keyword(token)
                if keyword:
                    return keyword
        
        elif len(word_list) == 1:
            token = nlp(word_list[0])[0]
            return get_most_similar_keyword(token)
    
    return find_keywords(list(word_counter.keys()))