
from __future__ import print_function

import numpy as np
import pickle
import time

from preprocessing.text_processor import IndexVectorizer, FlatIndexVectorizer
from preprocessing import text_processor as tp


demo = False

fb = True


def main():

    i_path = "/data/eval/fb/true_pairs.pkl"

    from utils import prepare_sqa_data

    # Get pairs from scratch or from serialized file
    if i_path is None:
        spos = prepare_sqa_data.get_spo_from_rel(filter_stopwords=True)
        uns_spos, loc_dic = prepare_sqa_data.get_spo_from_uns()
        spos = spos + uns_spos
        pos_samples = []
        # positive pairs
        for s, p, o in spos:
            pos_samples.append(s + " " + p)
            pos_samples.append(s + " " + o)
            pos_samples.append(p + " " + o)
    else:
        print("Loading data from: " + str(i_path))
        with open(i_path, "rb") as f:
            true_pairs = pickle.load(f)
        pos_samples = []
        seen = set()
        for e1, e2, label in true_pairs:
            if e1 + e2 in seen: 
                continue
            pos_samples.append(e1 + " " + e2)
            seen.add(e1 + e2)

    all_data = pos_samples
    print("Pos samples available: " + str(len(all_data)))

    if i_path is not None:
        with open("/data/eval/fb/tf_dictionary.pkl", "rb") as f:  
            vocab = pickle.load(f)
    else:
        vocab = dict()

    print("Initial vocab lenght: " + str(len(vocab)))

    if not fb:
        sparsity_code_size = 48
        idx_vectorizer = IndexVectorizer(vocab_index=vocab, sparsity_code_size=sparsity_code_size, tokenizer_sep=" ")
        vectorizer = tp.CustomVectorizer(idx_vectorizer)
    else:
        sparsity_code_size = 12
        idx_vectorizer = FlatIndexVectorizer(vocab_index=vocab, sparsity_code_size=sparsity_code_size)
        vectorizer = tp.CustomVectorizer(idx_vectorizer)

    # vectorization happens here
    X = []
    #all_data = all_data[:1000]  # test
    for el in all_data:
        ve = vectorizer.get_vector_for_tuple(el)
        ve = ve.toarray()[0]
        X.append(ve)

    X = np.asarray(X)

    vocab, inv_vocab = vectorizer.get_vocab_dictionaries()

    # def model1():
    input_dim = sparsity_code_size * 32

    from architectures import fabric_binary as bae
    model = bae.declare_model(input_dim, 256)
    model = bae.compile_model(model)

    st = time.time()

    model.fit(X, X, epochs=15, batch_size=128, shuffle=True)

    et = time.time()
    print("Total time: " + str(et - st))

    #o_path = "/data/eval/qatask/ad3/"
    o_path = "/data/eval/fbad/"

    bae.save_model_to_path(model, o_path, log="ad")

    with open(o_path + "tf_dictionary.pkl", "wb") as f:
        pickle.dump(vocab, f)


if __name__ == "__main__":
    print("test anomaly detector")
    main()
