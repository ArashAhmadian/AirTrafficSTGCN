# @Time     : Jan. 02, 2019 22:17
# @Author   : Veritas YIN
# @FileName : main.py
# @Version  : 1.0
# @Project  : Orion
# @IDE      : PyCharm
# @Github   : https://github.com/VeritasYin/Project_Orion

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from os.path import join as pjoin

import tensorflow as tf

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
tf.Session(config=config)

from utils.math_graph import *
from data_loader.data_utils import *
from models.trainer import model_train
from models.tester import model_test

import argparse

parser = argparse.ArgumentParser()
#30=hist + 7=pred -> 37 , kt=10, -> 27 -> 17 -> 7 -> error 
parser.add_argument('--n_route', type=int, default=228)
parser.add_argument('--n_his', type=int, default=7)
parser.add_argument('--n_pred', type=int, default=5)
parser.add_argument('--batch_size', type=int, default=50)
parser.add_argument('--epoch', type=int, default=50)
parser.add_argument('--save', type=int, default=10)
parser.add_argument('--ks', type=int, default=3)
parser.add_argument('--kt', type=int, default=3)
parser.add_argument('--lr', type=float, default=1e-3)
parser.add_argument('--opt', type=str, default='RMSProp')
parser.add_argument('--inf_mode', type=str, default='merge')
parser.add_argument('--V_Matrix', type=str, default='VMatrix.csv')
parser.add_argument('--W_Matrix', type=str, default='WMatrix.csv')

args = parser.parse_args()
print(f'Training configs: {args}')

n, n_his, n_pred = args.n_route, args.n_his, args.n_pred
Ks, Kt = args.ks, args.kt
# blocks: settings of channel size in st_conv_blocks / bottleneck design
blocks = [[1, 32, 64], [64, 32, 128]]

# Load wighted adjacency matrix W
if args.W_Matrix == 'default':
    W = weight_matrix(pjoin('./dataset', 'WMatrix.csv'))
else:
    # load customized graph weight matrix
    W = weight_matrix(pjoin('./dataset', args.W_Matrix))

# Calculate graph kernel
L = scaled_laplacian(W)
# Alternative approximation method: 1st approx - first_approx(W, n).
Lk = cheb_poly_approx(L, Ks, n)
tf.add_to_collection(name='graph_kernel', value=tf.cast(tf.constant(Lk), tf.float32))

# Data Preprocessing
data_file = args.V_Matrix

PeMS = data_gen(pjoin('./dataset', data_file), n, n_his + n_pred,day_slot=1)
print(f'>> Loading dataset with Mean: {PeMS.mean:.2f}, STD: {PeMS.std:.2f}')

if __name__ == '__main__':
    model_train(PeMS, blocks, args)
    model_test(PeMS, PeMS.get_len('test'), n_his, n_pred, args.inf_mode)
