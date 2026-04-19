import numpy as np
import math
from typing import Callable
from d2functions import (
    base_gielis,
    linear,
    f_sin_power,
    f_cos_power,
    f_trig_poly,
    abs_f_cos_power,
    abs_f_sin_power,
    abs_f_trig_poly,
    abs_f_linear,
    generalized_gielis,
)


# Parametric Tuning of the Gielis Superformula for Non-Target Based Automated Evolution of 3D Printable Objects
# 这是这篇文章提到的函数,生成3d的方法是直接将两个维度的gielis函数相乘,然后通过球面坐标转换成三维坐标
def direct_product_3d_gielis(
    theta,
    phi,
    # r1 的参数 (控制经度截面)
    alpha1: float = 1.0,
    beta1: float = 1.0,
    m1: float = 4.0,
    n11: int = 2,
    n21: int = 2,
    n31: int = 2,
    # r2 的参数 (控制纬度截面)
    alpha2: float = 1.0,
    beta2: float = 1.0,
    m2: float = 4.0,
    n12: int = 2,
    n22: int = 2,
    n32: int = 2,
):
    """
    计算标准的 3D Gielis 曲面。
    返回的 X, Y, Z 会是与 theta 和 phi 维度相同的矩阵。
    """
    # 1. 分别计算两个维度的半径
    r1 = base_gielis(theta, alpha=alpha1, beta=beta1, m=m1, n1=n11, n2=n21, n3=n31)
    r2 = base_gielis(phi, alpha=alpha2, beta=beta2, m=m2, n1=n12, n2=n22, n3=n32)

    # 2. 通过球面坐标映射到笛卡尔空间 X, Y, Z
    X = r1 * np.cos(theta) * r2 * np.cos(phi)
    Y = r1 * np.sin(theta) * r2 * np.cos(phi)
    Z = r2 * np.sin(phi)

    return X, Y, Z


def generalized_product_3d_gielis(
    theta,
    phi,
    # r1 的参数 (控制经度截面)
    ctheta1: Callable = lambda x: 1,
    alpha1: float = 1.0,
    beta1: float = 1.0,
    m11: float = 2.0,
    m12: float = 2.0,
    n11: int = 2,
    n12: int = 2,
    n13: int = 2,
    f11: Callable = lambda x: x,
    f12: Callable = lambda x: x,
    # r2 的参数 (控制纬度截面)
    ctheta2: Callable = lambda x: 1,
    alpha2: float = 1.0,
    beta2: float = 1.0,
    m21: float = 2.0,
    m22: float = 2.0,
    n21: int = 2,
    n22: int = 2,
    n23: int = 2,
    f21: Callable = lambda x: x,
    f22: Callable = lambda x: x,
):
    """
    根据论文复现的广义 3D Gielis 函数
    """
    r1 = generalized_gielis(
        theta,
        ctheta=ctheta1,
        alpha=alpha1,
        beta=beta1,
        m1=m11,
        m2=m12,
        f1=f11,
        f2=f12,
        n1=n11,
        n2=n12,
        n3=n13,
    )
    r2 = generalized_gielis(
        phi,
        ctheta=ctheta2,
        alpha=alpha2,
        beta=beta2,
        m1=m21,
        m2=m22,
        f1=f21,
        f2=f22,
        n1=n21,
        n2=n22,
        n3=n23,
    )
    X = r1 * np.cos(theta) * r2 * np.cos(phi)
    Y = r1 * np.sin(theta) * r2 * np.cos(phi)
    Z = r2 * np.sin(phi)
    return X, Y, Z


def fig_7_review(theta, phi):
    # 这是论文（# A Note About Generalized Forms of the Gielis Formula）中图7的函数
    f1 = lambda x: abs(linear(x, k=2, b=math.pi / 2))
    f2 = lambda x: abs(5 * x + math.pi / 2)
    f3 = lambda x: (2 * x + math.pi / 2) ** 2
    f4 = lambda x: (5 * x + math.pi / 2) ** 2
    m11 = m12 = m21 = m22 = 2
    alpha1 = alpha2 = 3
    beta1 = beta2 = 4
    n11 = n21 = -3
    n12 = n22 = 2
    n13 = n23 = 8

    r1 = generalized_gielis(
        theta,
        alpha=alpha1,
        beta=beta1,
        m1=m11,
        m2=m12,
        f1=f1,
        f2=f2,
        n1=n11,
        n2=n12,
        n3=n13,
    )
    r2 = generalized_gielis(
        phi,
        alpha=alpha2,
        beta=beta2,
        m1=m21,
        m2=m22,
        f1=f3,
        f2=f4,
        n1=n21,
        n2=n22,
        n3=n23,
    )
    X = r1 * np.cos(theta) * r2 * np.cos(phi)
    Y = r1 * np.sin(theta) * r2 * np.cos(phi)
    Z = r2 * np.sin(phi)
    return X, Y, Z


def fig_11_review(theta, phi, variant="left"):
    # 提取自论文 Fig. 11 的调制函数
    # 注意：为了让传入的 numpy 数组 (theta, phi) 能进行矢量化计算，
    # 这里全部使用 np.sin, np.cos, np.abs 和 np.pi
    f1 = lambda x: 3 * (np.sin(np.abs(2 * (x - np.pi / 3)))) ** 3
    f2 = lambda x: np.abs(3 * x)
    f3 = lambda x: 2 * (np.cos(np.abs(3 * (x + np.pi / 2)))) ** 2
    f4 = lambda x: np.abs(3 * x)

    # 论文给定的基础常数
    alpha1 = alpha2 = 3
    beta1 = beta2 = 4

    # 巧妙的指数映射 (Paper -> Code)
    # 论文: cos指数 n1=2, sin指数 n2=8, 外层指数 n3=-3
    # 代码: cos指数 n2=2, sin指数 n3=8, 外层指数 n1=-3
    n1_code = -3
    n2_code = 2
    n3_code = 8

    # 根据要渲染的是左图还是右图，切换 m 的值
    if variant == "left":
        m11 = m12 = m21 = m22 = 2
    else:  # variant == "right"
        m11 = m12 = m21 = m22 = 5

    # 调用修复后的 generalized_gielis_eq3
    r1 = generalized_gielis(
        theta,
        alpha=alpha1,
        beta=beta1,
        m1=m11,
        m2=m12,
        f1=f1,
        f2=f2,
        n1=n1_code,
        n2=n2_code,
        n3=n3_code,
    )

    r2 = generalized_gielis(
        phi,
        alpha=alpha2,
        beta=beta2,
        m1=m21,
        m2=m22,
        f1=f3,
        f2=f4,
        n1=n1_code,
        n2=n2_code,
        n3=n3_code,
    )

    # 球面坐标转换
    X = r1 * np.cos(theta) * r2 * np.cos(phi)
    Y = r1 * np.sin(theta) * r2 * np.cos(phi)
    Z = r2 * np.sin(phi)

    return X, Y, Z


def our_gielis(
    theta,
    phi,
    a: float = 3.0,
    b: float = 3.0,
    c: float = 3.0,
    l: float = 1.0,
    m1: float = 4.0,
    m2: float = 4.0,
    n0: float = -3.0,
    n1: float = 2.0,
    n2: float = 8.0,
    n3: float = 1.0,
):
    """
    (Our Gielis)
    """
    # 核心修复：给所有的三角函数基础项加上 np.abs()
    part1 = (np.abs(np.sin(m1 / 2 * phi) * np.cos(m2 * theta / 4)) / a) ** n1
    part2 = (np.abs(np.sin(m1 / 2 * phi) * np.sin(m2 * theta / 4)) / b) ** n2
    part3 = (np.abs(np.cos(m1 / 2 * phi)) / c) ** n3

    # 现在底数绝对大于等于 0，怎么求分数次幂都不会报 NaN 了
    r = (part1 + part2 + part3) ** (-1 / n0) * l

    X = r * np.cos(theta) * np.cos(phi)
    Y = r * np.sin(theta) * np.cos(phi)
    Z = r * np.sin(phi)

    return X, Y, Z
