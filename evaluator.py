from postprocessing import evaluate_discovery_model
import sys
import getopt
import pickle
import time

import config
import conductor as c
import keras

evaluate_discovery_model.main(
     #path_to_data="/data/fabricdata/mitdwh_index_nhrel/balanced_training_data.pklz",
     path_to_data="/data/fabricdata/mitdwh_index_nhrel/training_data.pklz",
     path_to_vocab= "/data/fabricdata/mitdwh_index_nhrel/tf_dictionary.pkl",
     path_to_location= "/data/fabricdata/mitdwh_index_nhrel/",
     path_to_model= "/data/fabricdata/mitdwh_index_nhrel/discoverymodel.h5epoch-80.hdf5",
     path_to_ae_model= "/data/fabricdata/mitdwh_index_nhrel/ae/",
     path_to_vae_model= "/data/fabricdata/mitdwh_index_nhrel/vae/",
     path_to_fqa_model= "/data/fabricdata/mitdwh_qa/fqa/",
     path_to_bae_model= "/data/fabricdata/mitdwh_index_nhrel/bae/",
     encoding_mode = "index",
     where_is_fabric = True)

#evaluate_discovery_model.main(
#    #path_to_data="/data/fabricdata/mitdwh_index_nhrel/balanced_training_data.pklz",
#    path_to_data="datafakehere/training_data.pklz",
#    path_to_vocab="datafakehere/tf_dictionary.pkl",
#    path_to_location="datafakehere/",
#    path_to_model="datafakehere/model.h5epoch-2.hdf5",
#    path_to_ae_model="datafakehere/ae/",
#    path_to_vae_model="datafakehere/vae/",
#    path_to_fqa_model=None,
#    encoding_mode="index",
#    where_is_fabric=False)

