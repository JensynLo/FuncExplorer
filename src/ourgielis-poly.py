import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import Callable

# ================= 1. 核心数学模型 =================


def our_gielis_poly(
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
    f_theta: Callable = lambda x: x,
    f_phi: Callable = lambda x: x,
):
    """
    (Our Gielis - 引入独立多项式调制版)
    """
    # 1. 计算调制后的角度
    t_mod = f_theta(theta)
    p_mod = f_phi(phi)

    # 2. 计算半径 r (内部使用调制角度 t_mod, p_mod，并严格保持绝对值保护)
    part1 = (np.abs(np.sin(m1 / 2 * p_mod) * np.cos(m2 * t_mod / 4)) / a) ** n1
    part2 = (np.abs(np.sin(m1 / 2 * p_mod) * np.sin(m2 * t_mod / 4)) / b) ** n2
    part3 = (np.abs(np.cos(m1 / 2 * p_mod)) / c) ** n3

    # 防止 n0 为 0 导致除零错误 (ZeroDivisionError)
    n0_safe = n0 if n0 != 0 else 0.0001
    r = (part1 + part2 + part3) ** (-1 / n0_safe) * l

    # 3. 映射到笛卡尔空间 (外部投影必须使用原始角度 theta, phi)
    X = r * np.cos(theta) * np.cos(phi)
    Y = r * np.sin(theta) * np.cos(phi)
    Z = r * np.sin(phi)

    return X, Y, Z


# ================= 2. UI 组件生成器 =================


def build_poly_f_ui(label, key_prefix):
    """
    UI 组件：生成多项式 f(x) 的输入控件，并返回一个可执行的 lambda 函数
    """
    st.markdown(f"**{label}**")
    # 独立控制是否套用绝对值
    use_abs = st.checkbox(f"套用绝对值 |f(x)|", value=False, key=f"{key_prefix}_abs")

    # 布局：前三个高次项放一行，低次项放一行
    c_cols1 = st.columns(3)
    c4 = c_cols1[0].number_input("x⁴", value=0.0, step=0.1, key=f"{key_prefix}_c4")
    c3 = c_cols1[1].number_input("x³", value=0.0, step=0.1, key=f"{key_prefix}_c3")
    c2 = c_cols1[2].number_input("x²", value=0.0, step=0.1, key=f"{key_prefix}_c2")

    c_cols2 = st.columns(2)
    c1 = c_cols2[0].number_input(
        "x¹", value=1.0, step=0.1, key=f"{key_prefix}_c1"
    )  # 默认为 f(x)=x
    c0 = c_cols2[1].number_input("常数 C", value=0.0, step=0.1, key=f"{key_prefix}_c0")

    st.divider()

    # 动态构建闭包函数
    def f(x):
        val = c4 * x**4 + c3 * x**3 + c2 * x**2 + c1 * x + c0
        return np.abs(val) if use_abs else val

    return f


# ================= 3. Streamlit 主程序 =================


def main():
    st.set_page_config(layout="wide", page_title="Our Gielis Poly Explorer")
    st.title("🧬 Our Gielis 3D: 多项式调制探索器")

    # --- 侧边栏参数控制 ---
    st.sidebar.header("🎛️ 基础形态参数")

    # 缩放与对称性并排，节省空间
    cols1 = st.sidebar.columns(2)
    a = cols1[0].slider("参数 a (x缩放)", 0.1, 10.0, 3.0)
    b = cols1[1].slider("参数 b (y缩放)", 0.1, 10.0, 3.0)
    c = cols1[0].slider("参数 c (z缩放)", 0.1, 10.0, 3.0)
    l = cols1[1].slider("总缩放 l", 0.1, 5.0, 1.0)

    m1 = cols1[0].slider("m1 (纬度对称)", 0.0, 20.0, 4.0, step=0.1)
    m2 = cols1[1].slider("m2 (经度对称)", 0.0, 20.0, 4.0, step=0.1)

    st.sidebar.subheader("指数参数 (n)")
    n0 = st.sidebar.slider("n0 (总外层指数)", -20.0, 20.0, -3.0)
    n1 = st.sidebar.slider("n1 (项1指数)", 0.1, 20.0, 2.0)
    n2 = st.sidebar.slider("n2 (项2指数)", 0.1, 20.0, 8.0)
    n3 = st.sidebar.slider("n3 (项3指数)", 0.1, 20.0, 1.0)

    # --- 核心：多项式调制面板 ---
    st.sidebar.header("🎢 角度多项式调制")
    with st.sidebar.expander("🛠️ 调制 经度 f_theta(θ)", expanded=False):
        f_theta = build_poly_f_ui("f_theta(θ)", "ft")

    with st.sidebar.expander("🛠️ 调制 纬度 f_phi(φ)", expanded=False):
        f_phi = build_poly_f_ui("f_phi(φ)", "fp")

    # --- 数据计算 ---
    # 定义域：经度 0~2pi, 纬度 -pi/2~pi/2
    # 增加采样率以保证多项式扭曲后的曲面依然平滑
    theta_1d = np.linspace(0, 2 * np.pi, 200)
    phi_1d = np.linspace(-np.pi / 2, np.pi / 2, 200)
    Theta, Phi = np.meshgrid(theta_1d, phi_1d)

    # 注入所有的闭包函数和标量参数
    X, Y, Z = our_gielis_poly(
        Theta, Phi, a, b, c, l, m1, m2, n0, n1, n2, n3, f_theta, f_phi
    )

    # --- 3D 渲染 ---
    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale="Magma",  # 换个酷炫的热力学配色
                showscale=False,
                lighting=dict(ambient=0.4, diffuse=0.8, specular=0.6, roughness=0.2),
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=0),
        height=850,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",  # 锁定空间比例
        ),
        paper_bgcolor="#0E1117",
    )

    st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    main()
