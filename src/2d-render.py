import streamlit as st
import numpy as np
import plotly.graph_objects as go

from utils import load_json, load_functions


def main():
    # 1. 加载配置文件并获取函数列表
    config_path = st.sidebar.text_input("配置文件路径", "configs/d2functions.json")
    configs = load_json(config_path)

    # 2. 提取函数 (增加防御性判断)
    functions = load_functions(configs)
    if not functions:
        st.error(f"⚠️ 无法加载函数列表！请检查配置文件: `{config_path}`")
        st.stop()

    # 3. 创建 Streamlit 应用
    st.title("2D Polar Function Visualization")

    # 4. 创建一个下拉菜单来选择函数
    func_names = list(functions.keys())
    selected_func_name = st.sidebar.selectbox("选择函数", func_names)

    selected_func, params_str = functions[selected_func_name]
    st.sidebar.write(f"当前选择: {selected_func_name} ({params_str})")

    # 5. 生成角度数据网格 (自变量 Theta)
    # 极坐标通常需要完整的 0 到 2pi 周期，使用足够多的点让曲线平滑
    Theta = np.linspace(0, 2 * np.pi, 1000)

    # 6. 计算半径因变量 R
    # 此时 selected_func 接收的是角度数组，返回的是半径数组
    R = selected_func(Theta)

    # 7. 使用 Plotly 渲染 2D 极坐标曲线 (华丽版)
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=R,
                theta=Theta,
                thetaunit="radians",
                mode="lines",
                fill="toself",  # 🌟 核心魔法 1：填充首尾相连的闭合区域
                fillcolor="rgba(156, 39, 176, 0.25)",  # 🌟 核心魔法 2：半透明的紫色填充 (RGBA)
                line=dict(
                    color="#D500F9",  # 极高饱和度的亮紫色，制造“发光”感
                    width=3,
                    shape="spline",  # 让折线更加平滑
                ),
                hoverinfo="r+theta",  # 鼠标悬停时显示半径和角度
            )
        ]
    )

    # 8. 更新 2D 极坐标布局 (暗色科幻风)
    fig.update_layout(
        template="plotly_dark",  # 🌟 核心魔法 3：一键切换 Plotly 的全局暗色主题
        title=dict(
            text=f"🌌 <b>{selected_func_name}</b>",
            font=dict(size=26, color="#E0E0E0"),
            x=0.5,  # 标题居中
            y=0.95,
        ),
        autosize=False,
        width=800,
        height=700,
        margin=dict(l=50, r=50, b=50, t=100),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",  # 让极坐标的底色透明
            radialaxis=dict(
                visible=True,
                range=[0, 20],
                gridcolor="#333333",  # 非常暗的灰色网格，不喧宾夺主
                tickfont=dict(color="#666666"),  # 刻度文字调暗
                showline=False,  # 隐藏生硬的半径主轴线
            ),
            angularaxis=dict(
                visible=True,
                gridcolor="#333333",
                linecolor="#444444",  # 最外圈的边框线
                tickfont=dict(color="#888888"),
            ),
        ),
        # 完美融合 Streamlit 的默认暗色模式背景
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
    )
    # ==========================================================

    # 渲染图表，使用最新的适配宽度参数
    st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    main()
