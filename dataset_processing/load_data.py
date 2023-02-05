import os
import numpy as np
from firedrake import *


def load_dataset(config):
    data_dir = os.path.join(config.resources_dir, "datasets", config.name_dir)
    train_data = []
    test_data = []
    # Load training data
    with CheckpointFile(os.path.join(data_dir, "train_data.h5"), 'r') as afile:
        # Note: There should be a way to get this from the checkpoint file directly.
        ntrain = int(np.array(afile.h5pyfile["ntrain"]))
        # Load mesh
        mesh = afile.load_mesh("mesh")
        # Load training data
        for i in range(ntrain):
            k_train = afile.load_function(mesh, "k", idx=i)
            u_train = afile.load_function(mesh, "u", idx=i)
            u_obs_train = afile.load_function(mesh, "u_obs", idx=i)
            train_data.append((k_train, u_train, u_obs_train))
    # Load test data
    with CheckpointFile(os.path.join(data_dir, "test_data.h5"), 'r') as afile:
        # Note: There should be a way to get this from the checkpoint file directly.
        ntest = int(np.array(afile.h5pyfile["ntest"]))
        # Load test data
        for i in range(ntest):
            k_test = afile.load_function(mesh, "k", idx=i)
            u_test = afile.load_function(mesh, "u", idx=i)
            u_obs_test = afile.load_function(mesh, "u_obs", idx=i)
            test_data.append((k_test, u_test, u_obs_test))
    return mesh, train_data, test_data
