import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# 这里导入你的函数，请确保 d3functions.py 和 d2functions.py 路径正确
from d3functions import generalized_product_3d_gielis


def build_poly_f_ui(label, key_prefix):
    """
    UI 组件：生成多项式 f(x) 的输入控件，并返回一个可执行的 lambda 函数
    """
    st.markdown(f"**{label}**")
    # 独立控制是否套用绝对值
    use_abs = st.checkbox(f"套用绝对值 |f(x)|", value=False, key=f"{key_prefix}_abs")

    # 布局：前三个高次项放一行，低次项放一行，节省空间
    c_cols1 = st.columns(3)
    c4 = c_cols1[0].number_input("x⁴", value=0.0, step=0.1, key=f"{key_prefix}_c4")
    c3 = c_cols1[1].number_input("x³", value=0.0, step=0.1, key=f"{key_prefix}_c3")
    c2 = c_cols1[2].number_input("x²", value=0.0, step=0.1, key=f"{key_prefix}_c2")

    c_cols2 = st.columns(2)
    c1 = c_cols2[0].number_input(
        "x¹", value=1.0, step=0.1, key=f"{key_prefix}_c1"
    )  # 默认为 f(x)=x
    c0 = c_cols2[1].number_input("常数 C", value=0.0, step=0.1, key=f"{key_prefix}_c0")

    st.divider()  # 添加分隔线

    # 动态构建闭包函数
    def f(x):
        val = c4 * x**4 + c3 * x**3 + c2 * x**2 + c1 * x + c0
        return np.abs(val) if use_abs else val

    return f


def main():
    st.set_page_config(layout="wide")  # 使用宽屏模式，给 3D 图留出更多空间
    st.title("3D Gielis: Polynomial Modulated Explorer")

    # ================= UI 侧边栏架构 =================
    st.sidebar.header("🎛️ 参数控制中心")

    # 使用 Tabs 分离经度和纬度的参数，避免侧边栏过长
    tab_r1, tab_r2 = st.sidebar.tabs(["经度截面 (Theta, r1)", "纬度截面 (Phi, r2)"])

    # -------- 经度 (r1) 参数面板 --------
    with tab_r1:
        st.subheader("基础参数")
        cols = st.columns(2)
        alpha1 = cols[0].slider("alpha1", 0.1, 10.0, 3.0, key="a1")
        beta1 = cols[1].slider("beta1", 0.1, 10.0, 4.0, key="b1")
        m11 = cols[0].slider("m11 (cos对称)", 0.0, 20.0, 2.0, key="m11")
        m12 = cols[1].slider("m12 (sin对称)", 0.0, 20.0, 2.0, key="m12")
        n11 = st.slider("n11 (外层指数)", -20, 20, -3, key="n11")
        n12 = st.slider("n12 (cos指数)", 0, 20, 2, key="n12")
        n13 = st.slider("n13 (sin指数)", 0, 20, 8, key="n13")

        with st.expander("🛠️ 展开配置 f11(θ) 与 f12(θ)"):
            f11_func = build_poly_f_ui("f11(θ) [作用于 cos]", "f11")
            f12_func = build_poly_f_ui("f12(θ) [作用于 sin]", "f12")

    # -------- 纬度 (r2) 参数面板 --------
    with tab_r2:
        st.subheader("基础参数")
        cols = st.columns(2)
        alpha2 = cols[0].slider("alpha2", 0.1, 10.0, 3.0, key="a2")
        beta2 = cols[1].slider("beta2", 0.1, 10.0, 4.0, key="b2")
        m21 = cols[0].slider("m21 (cos对称)", 0.0, 20.0, 2.0, key="m21")
        m22 = cols[1].slider("m22 (sin对称)", 0.0, 20.0, 2.0, key="m22")
        n21 = st.slider("n21 (外层指数)", -20, 20, -3, key="n21")
        n22 = st.slider("n22 (cos指数)", -20, 20, 2, key="n22")
        n23 = st.slider("n23 (sin指数)", -20, 20, 8, key="n23")

        with st.expander("🛠️ 展开配置 f21(φ) 与 f22(φ)"):
            f21_func = build_poly_f_ui("f21(φ) [作用于 cos]", "f21")
            f22_func = build_poly_f_ui("f22(φ) [作用于 sin]", "f22")

    # ================= 数据计算与渲染 =================

    # 为了保证闭合且能容纳多项式展开，定义域使用 [0, 2pi]
    theta_1d = np.linspace(0, 2 * np.pi, 150)
    phi_1d = np.linspace(-np.pi / 2, np.pi / 2, 150)
    Theta, Phi = np.meshgrid(theta_1d, phi_1d)

    # 调用你的终极广义函数
    X, Y, Z = generalized_product_3d_gielis(
        Theta,
        Phi,
        alpha1=alpha1,
        beta1=beta1,
        m11=m11,
        m12=m12,
        n11=n11,
        n12=n12,
        n13=n13,
        f11=f11_func,
        f12=f12_func,
        alpha2=alpha2,
        beta2=beta2,
        m21=m21,
        m22=m22,
        n21=n21,
        n22=n22,
        n23=n23,
        f21=f21_func,
        f22=f22_func,
    )

    # Plotly 3D 渲染
    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale="Viridis",
                showscale=False,
                lighting=dict(ambient=0.4, diffuse=0.8, roughness=0.1, specular=0.6),
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=0),
        height=800,
        scene=dict(
            xaxis=dict(showbackground=False, visible=False),
            yaxis=dict(showbackground=False, visible=False),
            zaxis=dict(showbackground=False, visible=False),
            aspectmode="data",  # 保持真实比例，防止被拉伸
        ),
        paper_bgcolor="#0E1117",
    )

    st.plotly_chart(fig, width="content")


if __name__ == "__main__":
    main()
