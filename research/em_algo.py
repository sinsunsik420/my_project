# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

import sys
import numpy as np
from matplotlib import pyplot as plt

K = 2  # 混合ガウス分布の数（固定）

def scale(X):
    """データ行列Xを属性ごとに標準化したデータを返す"""
    # 属性の数（=列の数）
    col = X.shape[1]
    
    # 属性ごとに平均値と標準偏差を計算
    mu = np.mean(X,axis=0)
    sigma = np.std(X,axis=0)
    
    # 属性ごとデータを標準化
    for i in range(col):
        X[:,i] = (X[:,i] - mu[i]) / sigma[i]
    
    return X

def gaussian(x, mean, cov):
    """多変量ガウス関数"""
    temp1 = 1 / ((2 * np.pi) ** (x.size/2.0))
    temp2 = 1 / (np.linalg.det(cov) ** 0.5)
    temp3 = - 0.5 * np.dot(np.dot(x - mean, np.linalg.inv(cov)), x - mean)
    return temp1 * temp2 * np.exp(temp3)

def likelihood(X, mean, cov, pi):
    """対数尤度関数"""
    sum = 0.0
    for n in range(len(X)):
        temp = 0.0
        for k in range(K):
            temp += pi[k] * gaussian(X[n], mean[k], cov[k])
        sum += np.log(temp)
    return sum

if __name__ == "__main__":
    # 訓練データをロード
    data = np.loadtxt(sys.argv[1],delimiter=" ")
    X = scale(data)  # データを標準化（各次元が平均0、分散1になるように）
    N = len(X)    # データ数
    
    # 訓練データから混合ガウス分布のパラメータをEMアルゴリズムで推定する
    
    # 平均、分散、混合係数を初期化
    mean = np.random.rand(K, 3)
    cov = np.zeros( (K, 3, 3) ) 
    for k in range(K):
        cov[k] = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    pi = np.random.rand(K)
    
    # 負担率の空配列を用意
    gamma = np.zeros( (N, K) )
    
    # 対数尤度の初期値を計算
    like = likelihood(X, mean, cov, pi)

    turn = 0
    while True:
        print turn, like
        
        # E-step : 現在のパラメータを使って、負担率を計算
        for n in range(N):
            # 分母はkによらないので最初に1回だけ計算
            denominator = 0.0
            for j in range(K):
                denominator += pi[j] * gaussian(X[n], mean[j], cov[j])
            # 各kについて負担率を計算
            for k in range(K):
                gamma[n][k] = pi[k] * gaussian(X[n], mean[k], cov[k]) / denominator
        
        # M-step : 現在の負担率を使って、パラメータを再計算
        for k in range(K):
            # Nkを計算する
            Nk = 0.0
            for n in range(N):
                Nk += gamma[n][k]
            
            # 平均を再計算
            mean[k] = np.zeros(3)
            for n in range(N):
                mean[k] += gamma[n][k] * X[n]
            mean[k] /= Nk
            
            # 共分散を再計算
            cov[k] = np.zeros((3,3))
            for n in range(N):
                temp = X[n] - mean[k]
                cov[k] += gamma[n][k] * np.matrix(temp).reshape(3, 1) * np.matrix(temp).reshape(1, 3)  # 縦ベクトルx横ベクトル
            cov[k] /= Nk
            
            # 混合係数を再計算
            pi[k] = Nk / N
            
        # 収束判定
        new_like = likelihood(X, mean, cov, pi)
        diff = new_like - like
        if diff < 0.01:
            break
        like = new_like
        turn += 1
    
    print mean,cov
