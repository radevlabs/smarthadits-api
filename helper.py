from itertools import combinations
from sklearn.metrics import mean_squared_error
import re
import numpy as np
import string
import sys

def clean(text):
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\\[\\]\\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    return text

def scan_narrator(narrators, hadith):
    narrators = np.array(narrators)
    hadith = clean(hadith)
    
    narrators_hadith = []
    for narrator in narrators:
        if narrator in hadith:
            narrators_hadith.append(narrator)
            
    ns = []
    for ns0 in narrators_hadith:
        valid = True
        for ns1 in narrators_hadith:
            if ns0 != ns1:
                if ns0 in ns1:
                    valid = False
                    break
        if valid:
            ns.append(ns0)
    
    return np.array(ns)

def tfbinary(perawi_list, perawi_from_hadits):
    perawi_list = list(perawi_list)
    perawi_from_hadits = list(perawi_from_hadits)
    vector = np.zeros(len(perawi_list), dtype=np.int)

    for perawi in perawi_from_hadits:
        if perawi in perawi_list:
            vector[perawi_list.index(perawi)] = 1

    return vector


def combalpha(c, depth=3):
    alphabets = string.ascii_uppercase
    combalphas = []
    for d in np.arange(1, depth + 1):
        for comb in combinations(alphabets, d):
            combalphas.append(''.join(comb))

    return combalphas[c]