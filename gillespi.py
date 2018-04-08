# -*- coding: utf-8 -*-
# @Time    : 2018/4/3 15:35
# @Author  : chenjian zhangtianrui

from __future__ import division
import numpy as np
import networkx as nx
import time
import multiprocessing
import threadpool


# gillespi函数输入节点数，邻接矩阵以及β,γ可以返回在初始条件为1各节点染毒的情况下200条样本路径,每次迭代1000次是否灭绝
def gillespi(N, a, gama, beta):
    Mbeta = np.multiply((0.01 * np.random.random(size=(N, N)) - 0.005 + beta), a)  # 对染毒速率进行随机波动构造染毒速率矩阵
    Mgama = 0.01 * np.random.random(size=(N)) - 0.005 + gama  # 对重装速率进行随机波动构造重装速率矩阵
    rads = np.arange(0, N, 1)
    np.random.shuffle(rads)  # 随机选取初始染毒节点
    Endflag = np.zeros(100)  # 100条样本路径中每次迭代1000次的演化结果
    for count in range(0, Endflag.size):
        x = np.zeros(N)  # 定义节点状态向量
        x[rads[0]] = 1  # 将初始条件中的染毒节点状态更新为1
        for k in range(300):
            V = np.zeros(N)  # 存储每个节点的转移速率
            Vtemp = np.zeros(N + 1)  # 储存循环到某个节点时当前所有节点总速率.第一位为0从第二位开始储存
            # 计算每个节点的转移速率
            for i in range(0, N):
                neighbor = np.nonzero(a[i])  # 取出某节点邻接矩阵中的相邻点下标返回类型为元组
                # 如果为脆弱节点
                if x[i] == 0:
                    for j in range(0, neighbor[1].size):  # 对邻居节点进行循环
                        if x[neighbor[1][j]] == 1:  # 如果邻居节点为染毒节点则累计向该节点传毒的速率
                            V[i] = V[i] + Mbeta[i, neighbor[1][j]]
                # 如果为染毒节点则转移速率为重装速率
                if x[i] == 1:
                    V[i] = Mgama[i]
                Vtemp[i+1] = Vtemp[i] + V[i]
            # 所有节点的染毒速率均为0表示病毒灭绝迭代终止
            if Vtemp[N] == 0:
                break
            for i in range(0, N+1):
                Vtemp[i] = Vtemp[i] / Vtemp[N]  # 将当前累加速率/所有节点总速率得到一个0-1的概率值用于选择转移节点
            # 选择一个要改变状态的节点并进行状态转移
            Nflag = np.random.rand()
            for i in range(0, N):
                # 随机数落在某个区间
                if (Nflag >= Vtemp[i]) and (Nflag < Vtemp[i+1]):
                    # 若为脆弱节点则改为染毒反之亦然
                    if x[i] == 0:
                        x[i] = 1
                    else:
                        x[i] = 0
                    # 选择一个节点并转移后跳出循环
                    break
        Endflag[count] = np.sum(x)
    if (np.sum(Endflag) / (100 * N)) < 0.01:
        return 0
    else:
        return 1





