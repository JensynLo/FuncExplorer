import streamlit as st
import numpy as np
import plotly.graph_objects as go

from d3functions import our_gielis


def main():
    st.set_page_config(layout="wide", page_title="Our Gielis Explorer")
    st.title("🧪 Our Gielis 3D 变体探索器")

    # --- 侧边栏参数控制 ---
    st.sidebar.header("维度与缩放参数")
    a = st.sidebar.slider("参数 a (x轴缩放)", 0.1, 10.0, 3.0)
    b = st.sidebar.slider("参数 b (y轴缩放)", 0.1, 10.0, 3.0)
    c = st.sidebar.slider("参数 c (z轴缩放)", 0.1, 10.0, 3.0)
    l = st.sidebar.slider("总缩放 l", 0.1, 5.0, 1.0)

    st.sidebar.header("对称性参数 (m)")
    m1 = st.sidebar.slider("m1 (纬度对称性)", 0.0, 20.0, 4.0, step=0.1)
    m2 = st.sidebar.slider("m2 (经度对称性)", 0.0, 20.0, 4.0, step=0.1)

    st.sidebar.header("指数参数 (n)")
    n0 = st.sidebar.slider("n0 (总外层指数)", -20.0, 20.0, -3.0)
    n1 = st.sidebar.slider("n1 (项1指数)", 0.1, 20.0, 2.0)
    n2 = st.sidebar.slider("n2 (项2指数)", 0.1, 20.0, 8.0)
    n3 = st.sidebar.slider("n3 (项3指数)", 0.1, 20.0, 1.0)

    # --- 数据计算 ---
    # 定义域：经度 0~2pi, 纬度 -pi/2~pi/2
    theta_1d = np.linspace(0, 2 * np.pi, 180)
    phi_1d = np.linspace(-np.pi / 2, np.pi / 2, 180)
    Theta, Phi = np.meshgrid(theta_1d, phi_1d)

    X, Y, Z = our_gielis(Theta, Phi, a, b, c, l, m1, m2, n0, n1, n2, n3)

    # --- 3D 渲染 ---
    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale="Viridis",
                showscale=False,
                lighting=dict(ambient=0.5, diffuse=0.8, specular=0.5, roughness=0.1),
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=0),
        height=800,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",
        ),
        paper_bgcolor="#0E1117",
    )

    st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    main()
