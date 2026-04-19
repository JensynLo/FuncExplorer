import math as m
from typing import Callable
import numpy as np


def linear(theta, k: float = 1.0, b: float = 0.0):
    return k * theta + b


def exponential(theta, k: float = 1.0, b: float = 0.0):
    return k * np.exp(theta) + b


def logarithmic(theta, k: float = 1.0, b: float = 0.0):
    return k * np.log(theta + 1) + b  # 加1避免log(0)错误


def base_gielis(
    theta,
    alpha: float = 2,
    beta: float = 2,
    m: float = 1,
    n1: int = 2,
    n2: int = 2,
    n3: int = 2,
):
    # 计算Gielis曲线的半径
    part1 = np.abs(np.cos(m * theta / 4) / alpha) ** n2
    part2 = np.abs(np.sin(m * theta / 4) / beta) ** n3
    r = (part1 + part2) ** (-1 / n1)
    return r


def generalized_gielis(
    theta,
    ctheta: Callable[[float], float] = lambda x: 1,
    alpha: float = 2,
    beta: float = 2,
    m1: float = 1,
    m2: float = 1,
    f1: Callable[[float], float] = lambda x: x,
    f2: Callable[[float], float] = lambda x: x,
    n1: int = 2,
    n2: int = 2,
    n3: int = 2,
):
    part1 = np.abs(np.cos(m1 * f1(theta) / 4) / alpha) ** n2
    part2 = np.abs(np.sin(m2 * f2(theta) / 4) / beta) ** n3
    r = (part1 + part2) ** (-1 / n1)
    return r * ctheta(theta)


def generalized_gielis_linear(
    theta,
    ctheta: Callable[[float], float] = lambda x: 1,
    alpha: float = 2,
    beta: float = 2,
    k1: float = 1,
    k2: float = 1,
    b1: float = 0,
    b2: float = 0,
    m1: float = 1,
    m2: float = 1,
    n1: int = 2,
    n2: int = 2,
    n3: int = 2,
):
    f1 = lambda x: linear(x, k=k1, b=b1)
    f2 = lambda x: linear(x, k=k2, b=b2)
    return generalized_gielis(
        theta,
        ctheta=ctheta,
        alpha=alpha,
        beta=beta,
        m1=m1,
        m2=m2,
        f1=f1,
        f2=f2,
        n1=n1,
        n2=n2,
        n3=n3,
    )


def f_sin_power(theta, n_f: float = 1.0, m_f: float = 0.0):
    """f(θ) = sin^(2m+1)(nθ)"""
    return np.sin(n_f * theta) ** (2 * m_f + 1)


def f_cos_power(theta, n_f: float = 1.0, m_f: float = 0.0):
    """f(θ) = cos^(2m+1)(nθ)"""
    return np.cos(n_f * theta) ** (2 * m_f + 1)


def f_trig_poly(theta, A_f: float = 1.0, B_f: float = 1.0):
    """f(θ) = A sin θ + B cos 2θ"""
    return A_f * np.sin(theta) + B_f * np.cos(2 * theta)


def abs_f_sin_power(theta, n_f: float = 1.0, m_f: float = 0.0):
    """f(θ) = |sin(nθ)|^(2m+1)"""
    return np.abs(f_sin_power(theta, n_f=n_f, m_f=m_f))


def abs_f_cos_power(theta, n_f: float = 1.0, m_f: float = 0.0):
    """f(θ) = |cos(nθ)|^(2m+1)"""
    return np.abs(f_cos_power(theta, n_f=n_f, m_f=m_f))


def abs_f_trig_poly(theta, A_f: float = 1.0, B_f: float = 1.0):
    """f(θ) = |A sin θ + B cos 2θ|"""
    return np.abs(f_trig_poly(theta, A_f=A_f, B_f=B_f))


def abs_f_linear(theta, k: float = 1.0, b: float = 0.0):
    """f(θ) = |kθ + b|"""
    return np.abs(linear(theta, k=k, b=b))
