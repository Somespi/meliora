import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from typing import List
from pathlib import Path

nlp = spacy.load("en_core_web_md")
extras = set(STOP_WORDS).union(set(punctuation)).union({'\n'})

with open(Path(__file__).parent / "includes" / "common_titles.txt", "r") as f:
    commons = set(f.read().split('\n'))


def find_suitable(text: str, similarity_words: List[str]) -> str:
    doc = nlp(text)
    words = [word.text for word in doc if word.text.lower() not in extras and word.text.isalpha()]
    
    if not words:
        return None
    
    frequency = {}
    for w in words:
        if w in frequency:
            frequency[w] += 1
        else:
            frequency[w] = 1
    
    important = max(frequency, key=frequency.get)
    
    def find(lis: List[str]) -> str:
        if len(lis) >= 3:
            text = " ".join(lis[:3])
            doc = nlp(text)
            del lis[:3]
            
            for tok in doc:
                similarities = {common: tok.similarity(nlp(common)) for common in commons}
                
                if max(similarities.values()) >= 0.4:
                    keyword_with_max_similarity = max(similarities, key=similarities.get)
                    return keyword_with_max_similarity
                
                elif tok.dep_ == 'nmod' or tok.text == important:
                    for similar in similarity_words:
                        if tok.similarity(nlp(similar)) >= 0.6:
                            return similar
                    return tok.text
            
            return find(lis)
        
        elif len(lis) == 2:
            text = " ".join(lis)
            doc = nlp(text)
            
            for tok in doc:
                similarities = {common: tok.similarity(nlp(common)) for common in commons}
                
                if max(similarities.values()) >= 0.4:
                    keyword_with_max_similarity = max(similarities, key=similarities.get)
                    return keyword_with_max_similarity
                
                if tok.dep_ == 'nmod' or tok.text == important:
                    for similar in similarity_words:
                        if tok.similarity(nlp(similar)) >= 0.6:
                            return similar
                    return tok.text
        
        elif len(lis) == 1:
            similarities = {common: nlp(lis[0]).similarity(nlp(common)) for common in commons}
            
            if max(similarities.values()) >= 0.4:
                keyword_with_max_similarity = max(similarities, key=similarities.get)
                return keyword_with_max_similarity
            
            for similar in similarity_words:
                if nlp(lis[0]).similarity(nlp(similar)) >= 0.6:
                    return similar
            return lis[0]
    
    return find(words)
