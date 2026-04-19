import streamlit as st
import numpy as np
import plotly.graph_objects as go

from utils import load_json, load_functions


def main():
    # 1. 加载配置文件
    config_path = st.sidebar.text_input("配置文件路径", "configs/d3functions.json")
    configs = load_json(config_path)

    # 2. 提取函数并验证
    functions = load_functions(configs)
    if not functions:
        st.error(f"⚠️ 无法加载函数列表！请检查配置文件: `{config_path}`")
        st.stop()

    # 3. 创建 Streamlit 应用
    st.title("3D Gielis Superformula Visualization")

    # 4. 下拉菜单选择函数
    func_names = list(functions.keys())
    selected_func_name = st.sidebar.selectbox("选择函数", func_names)

    selected_func, params_str = functions[selected_func_name]
    st.sidebar.write(f"当前选择: {selected_func_name} ({params_str})")

    # ================= 核心修改区域：3D 球面网格 =================

    # 5. 生成球面坐标数据网格
    # Theta (经度): 通常需要 -pi 到 pi
    # Phi (纬度): 通常需要 -pi/2 到 pi/2
    # theta_1d = np.linspace(-np.pi, np.pi, 200)
    # phi_1d = np.linspace(-np.pi / 2, np.pi / 2, 200)
    # 修改 3d-render.py 中的网格生成部分
    theta_1d = np.linspace(0, 2 * np.pi, 200)  # 修正为 [0, 2pi]
    phi_1d = np.linspace(-np.pi / 2, np.pi / 2, 200)

    Theta, Phi = np.meshgrid(theta_1d, phi_1d)

    # 6. 计算三维坐标矩阵 X, Y, Z
    # d3functions.py 中的函数现在返回三个矩阵
    X, Y, Z = selected_func(Theta, Phi)

    # 7. 使用 Plotly 渲染 3D 曲面
    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale="Plasma",  # 高对比度配色：Plasma 或 Viridis
                showscale=False,  # 隐藏颜色条，使界面更清爽
                lighting=dict(  # 添加金属光泽，增强立体感
                    ambient=0.5,
                    diffuse=0.8,
                    fresnel=0.2,
                    specular=0.5,
                    roughness=0.1,
                ),
                lightposition=dict(x=100, y=100, z=1000),  # 打光角度
            )
        ]
    )

    # 8. 更新 3D 布局 (暗色科幻风)
    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text=f"🌌 <b>{selected_func_name}</b>",
            font=dict(size=26, color="#E0E0E0"),
            x=0.5,
            y=0.95,
        ),
        autosize=False,
        width=800,
        height=800,
        margin=dict(l=0, r=0, b=0, t=80),
        scene=dict(
            xaxis=dict(showbackground=False, visible=False),  # 隐藏全部背景轴线
            yaxis=dict(showbackground=False, visible=False),
            zaxis=dict(showbackground=False, visible=False),
            aspectratio=dict(
                x=1, y=1, z=1
            ),  # 强制 1:1:1 比例，防止形状因坐标系而被压扁
        ),
        paper_bgcolor="#0E1117",
    )
    # ==========================================================

    st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    main()
