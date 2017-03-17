import inputoutput as IO
from fabric_extractor import RankLeftFnIdx, RankRightFnIdx, load_input_data
from fabric_extractor import mat2idx, Embeddings, LayerTrans, Unstructured, l2_norm
import numpy as np
import pickle

ranker_s = None
ranker_o = None

o_train_idx = None

idx_to_er = None


def prepare_env(data_path, path, model_path):
    print("Loading train, validation and test data...")
    config = IO.load_config(path)

    s_in_mat, p_in_mat, o_in_mat = load_input_data(data_path, config)
    print("Train size: " + str(s_in_mat.shape))
    s_val_mat, p_val_mat, o_val_mat = load_input_data(data_path, config)
    print("Val size: " + str(s_val_mat.shape))
    s_test_mat, p_test_mat, o_test_mat = load_input_data(data_path, config)
    print("Test size: " + str(s_test_mat.shape))

    # Indexes
    global o_train_idx
    s_train_idx, p_train_idx, o_train_idx = mat2idx(s_in_mat), mat2idx(p_in_mat), mat2idx(o_in_mat)
    s_val_idx, p_val_idx, o_val_idx = mat2idx(s_val_mat), mat2idx(p_val_mat), mat2idx(o_val_mat)
    s_test_idx, p_test_idx, o_test_idx = mat2idx(s_test_mat), mat2idx(p_test_mat), mat2idx(o_test_mat)

    global idx_to_er
    idx_to_er = IO.load_dict_encoded(path)


def true_or_false(subject, predicate, obj):
    error_s = [np.argsort(np.argsort((ranker_s(obj, predicate)[0]).flatten())[::-1]).flatten()[subject] + 1]
    error_o = [np.argsort(np.argsort((ranker_o(subject, predicate)[0]).flatten())[::-1]).flatten()[obj] + 1]
    return error_o + error_s


def qa(subject, predicate):
    error_s = []
    error_o = []
    for obj in o_train_idx:
        error_s += [np.argsort(np.argsort((ranker_s(obj, predicate)[0]).flatten())[::-1]).flatten()[subject] + 1]
        error_o += [np.argsort(np.argsort((ranker_o(subject, predicate)[0]).flatten())[::-1]).flatten()[obj] + 1]
    error_all = error_s + error_o
    # top 10 indices
    return translate_idx_to_er(error_all[:10])


def translate_idx_to_er(idxs):
    es = []
    for idx in idxs:
        e = idx_to_er[idx]
        es.append(e)
    return es

if __name__ == "__main__":
    model_path = "data/FB15k/processed/model"
    path = "data/FB15k/processed"
    data_path = "data/FB15k/processed/test"
    #embeddings, s_op, o_op, l2sim = IO.load_model(model_path)
    f = open(model_path + '/bestmodel.pkl', 'rb')
    embeddings = pickle.load(f)
    s_op = pickle.load(f)
    o_op = pickle.load(f)
    l2norm = pickle.load(f)
    f.close()

    #global ranker_s
    ranker_s = RankLeftFnIdx(l2norm, embeddings, s_op, o_op)
    #global ranker_o
    ranker_o = RankRightFnIdx(l2norm, embeddings, s_op, o_op)

    prepare_env(data_path, path, model_path)

    res = qa("subject", "predicate")
    print(str(res))

    print("evaluator")
