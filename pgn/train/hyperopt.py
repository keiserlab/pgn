"""Hyperparameter optimization. Adapted from:
https://github.com/chemprop/chemprop/blob/master/chemprop/hyperparameter_optimization.py"""

from hyperopt import fmin, hp, tpe

import numpy as np

from copy import deepcopy
import os.path as osp

SPACE = {
    'ffn_hidden_size': hp.quniform('ffn_hidden_size', low=200, high=2400, q=100),
    'depth': hp.quniform('depth', low=2, high=6, q=1),
    'dropout': hp.quniform('dropout', low=0.0, high=0.4, q=0.05),
    'ffn_num_layers': hp.quniform('ffn_num_layers', low=1, high=4, q=1),
    'lr': hp.loguniform('lr', low=1e-6, high=1e-2)
}

INT_KEYS = ['ffn_hidden_size', 'depth', 'ffn_num_layers']

def hyperopt(args):
    """
    Runs hyperparmeter optimization.
    :param args: The arguments class containing the arguments used for optimization
    and training.
    :return: None
    """
    results = []

    def objective(hyperparams):

        for key in INT_KEYS:
            hyperparams[key] = int(hyperparams[key])

        hyper_args = deepcopy(args)

        folder_name = '_'.join(f'{key}_{value}' for key, value in hyperparams.items())
        hyper_args.save_dir = osp.join(hyper_args.save_dir, folder_name)

        for key, value in hyperparams.items():
            setattr(hyper_args, key, value)

        #TODO: Run training
        score = float('inf')

        results.append({
            'score': score,
            'hyperparams': hyperparams
        })

        return (1 if hyper_args.minimize_score else -1) * score

    fmin(objective, SPACE, algo=tpe.suggest, max_evals=args.num_iters, rstate=np.random.RandomState(args.seed))
