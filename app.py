from flask import Flask, request
from joblib import load
import numpy as np
import helper as hp
import json

app = Flask(__name__)

narrators = open('narrators.csv').read().split("\n")
narrators = np.array(narrators)

pca = load('pca.2200.jlb')
nn = load('nn.all.600.jlb')

@app.route('/apiv1', methods=['POST'])
def info():
    if request.method == 'POST':
        hadith = request.form['hadith']
        hadith = hp.clean(hadith).strip()
        hadith_narrators = hp.scan_narrator(narrators, hadith)
        vectors = np.array([hp.tfbinary(narrators, hadith_narrators)])
        vectors = np.array(pca.transform(vectors))
        output = nn.predict(vectors)[0]

        return json.dumps({
            'result': output,
            'narrators': hadith_narrators.tolist(),
            'cleaned_hadith': hadith
        })

    return json.dumps(None)

if __name__ == '__main__':
    app.run()
