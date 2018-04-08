# -*- coding: utf-8 -*-
# @Time    : 2018/4/8 12:14
# @Author  : timothy

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pylab
import imageio
import os


path = 'resources'
n = 10  # 节点数
G = nx.random_graphs.barabasi_albert_graph(n, 4, 0.3)
A = nx.to_numpy_matrix(G)
A = np.array(A)
enlarge = 20  # 节点放大倍数
node_size = [sum(A[:, i]) * enlarge for i in range(n)]  # 节点大小和度数成正比


# 画图
def draw(show=True):
    figures = []
    pylab.ion()
    num_plots = 10
    pos = nx.circular_layout(G)
    for i in range(num_plots):
        colors = np.random.randint(10, size=n)
        fig = pylab.figure()  # 每张图的句柄
        nx.draw(G, pos, node_color=colors, with_labels=False, node_size=node_size)
        if show:
            pylab.show()
            plt.pause(2)
            pylab.close(fig)
        figures.append(fig)
    return figures


# figure保存成png
def save(figures):
    if not os.path.exists(path):
        os.makedirs(path)
    i = 0
    for fig in figures:
        i += 1
        save_path = path + '/' + str(i) + '.png'
        fig.savefig(save_path)


# 用保存的png制作gif
def make_gif():
    images = []
    filenames = sorted(fn for fn in os.listdir(path+'/') if fn.endswith('.png'))
    for filename in filenames:
        images.append(imageio.imread(path + '/' + filename))
    sava_path = path + '/test.gif'
    imageio.mimsave(sava_path, images, format='GIF', duration=1)  # duration 每帧间隔时间，loop 循环次数


def main():
    figures = draw(show=True)
    save(figures)
    make_gif()


if __name__ == '__main__':
    main()
