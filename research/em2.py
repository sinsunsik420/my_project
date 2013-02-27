# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

import sys
import numpy as np
from matplotlib import pyplot as plt

K = 2  # 混合ガウス分布の数（固定）

def scale(X):
    """データ行列Xを属性ごとに標準化したデータを返す"""
    # 属性の数（=列の数）
    #col = X.shape[1]
    
    # 属性ごとに平均値と標準偏差を計算
    mu = np.mean(X)
    sigma = np.std(X)
    
    # 属性ごとデータを標準化
    X = (X - mu) / sigma
    
    return X

def gaussian(x, mean, var):
    """ガウス関数"""
    temp1 = (- 0.5) * (x - mean)*(x - mean)/(var * var)
    temp2 = np.power(2 * np.pi * var * var,0.5)
    return np.exp(temp1) / temp2

def likelihood(X, mean, var, pi):
    """対数尤度関数"""
    sum = 0.0
    for x in X:
        temp = 0.0
        for k in range(K):
            temp += pi[k] * gaussian(x, mean[k], var[k])
        sum += np.log(temp)
    return sum

if __name__ == "__main__":
    # 訓練データをロード
    data = np.loadtxt(sys.argv[1],delimiter=" ")
    X = scale(data[:,2])  # データを標準化（各次元が平均0、分散1になるように）
    N = len(X)    # データ数
    
    # 訓練データから混合ガウス分布のパラメータをEMアルゴリズムで推定する
    
    # 平均、分散、混合係数を初期化
    mean = np.random.rand(K)
    var = np.random.rand(K) 
    pi = np.random.rand(K)
    
    # 負担率の空配列を用意
    gamma = np.zeros( (N, K) )
    
    # 対数尤度の初期値を計算
    like = likelihood(X, mean, var, pi)

    turn = 0
    while True:
        print turn, like
        
        # E-step : 現在のパラメータを使って、負担率を計算
        for n in range(N):
            # 分母はkによらないので最初に1回だけ計算
            denominator = 0.0
            for j in range(K):
                denominator += pi[j] * gaussian(X[n], mean[j], var[j])
            # 各kについて負担率を計算
            for k in range(K):
                gamma[n][k] = pi[k] * gaussian(X[n], mean[k], var[k]) / denominator
        
        # M-step : 現在の負担率を使って、パラメータを再計算
        for k in range(K):
            # Nkを計算する
            Nk = 0.0
            for n in range(N):
                Nk += gamma[n][k]
            
            # 平均を再計算
            mean[k] = 0.0
            for n in range(N):
                mean[k] += gamma[n][k] * X[n]
            mean[k] /= Nk
            
            # 共分散を再計算
            var[k] = 0.0
            for n in range(N):
                temp = X[n] - mean[k]
                var[k] += gamma[n][k] * temp * temp  # 縦ベクトルx横ベクトル
            var[k] /= Nk
            
            # 混合係数を再計算
            pi[k] = Nk / N
            
        # 収束判定
        new_like = likelihood(X, mean, var, pi)
        diff = new_like - like
        if diff < 0.01:
            break
        like = new_like
        turn += 1
    
    print mean,var
