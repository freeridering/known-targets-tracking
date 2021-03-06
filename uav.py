import parameter
import numpy as np
import typing


class UavSingle:  # 单个无人机

    def __init__(self, uid, p: parameter.Parameter):
        self.uid = uid  # uav的id
        self.pos_now = self.init_pos_now(uid, p)
        self.pos_past = np.copy(self.pos_now)  # uav的上一时刻位置/初始化位置
        self.all_way_local = -1 * np.ones([p.max_way_num, p.n_step * 2], dtype=int)  # 某一决策周期uav的所有可行路径，可以设定最大条数
        self.S_d = np.zeros([p.nx, p.ny], dtype=float)  # 调度信息素矩阵
        self.way_local = np.tile(self.pos_now.T, (p.n_step, 1))  # 短暂局部最优
        self.way_global = np.tile(self.pos_now.T, (p.n_step, 1))  # 全局最优
        self.path = -1 * np.ones([p.time_limit, 2], dtype=int)  # 走过的路径，原名wayed
        self.Jmax = -np.inf * np.ones([p.time_limit, ], dtype=float) # 记录每步的最优值，用于迭代优化
        self.way_global_inter = np.tile(self.pos_now.T, (p.n_step, 1))  # 迭代的每步全局最优
    def init_pos_now(self, uid, p: parameter.Parameter):
        """
        初始化uav位置
        :param uid:
        :param p:
        :return:
        """
        pos_now = np.zeros([2, ], dtype=int)
        if uid < p.nu / 2:
            flex_axis = (uid // 2 + 1) * np.round(p.nx // (p.ox + 1) / (p.ox + 1)) * (p.ox + 1)
            if uid % 2 == 0:
                pos_now[0] = flex_axis
                pos_now[1] = 0
            else:
                pos_now[0] = flex_axis
                pos_now[1] = p.nx - 1
        else:
            uid = uid - p.nu / 2
            flex_axis = (uid // 2 + 1) * np.round(p.ny // (p.oy + 1) / (p.nu / 4 + 1)) * (p.oy + 1)
            if uid % 2 == 0:
                pos_now[0] = 0
                pos_now[1] = flex_axis
            else:
                pos_now[0] = p.nx - 1
                pos_now[1] = flex_axis
        return pos_now


Uav_Swarm = typing.List[UavSingle]
