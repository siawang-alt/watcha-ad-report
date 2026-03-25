"""트렌드 분석 페이지 — 시계열 추이 및 기간 비교"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config.metrics import DISPLAY_NAMES
from utils.chart_builder import create_trend_comparison_chart, CHART_COLORS

st.set_page_config(page_title="트렌드 분석", page_icon="📈", layout="wide")
st.title("📈 트렌드 분석")

# --- 데이터 확인 ---
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("데이터가 없습니다. '데이터 업로드' 페이지에서 파일을 먼저 업로드해주세요.")
    st.stop()

df = st.session_state.df.copy()

if "date" not in df.columns:
    st.error("날짜 컬럼이 없어서 트렌드 분석을 할 수 없습니다. 데이터 업로드 시 날짜 컬럼을 매핑해주세요.")
    st.stop()

# 사용 가능한 숫자 지표
available_metrics = [
    col for col in ["impressions", "clicks", "ctr", "ad_spend", "conversions", "cpc", "cpm", "cpa", "revenue", "roas"]
    if col in df.columns
]
metric_options = {m: DISPLAY_NAMES.get(m, m) for m in available_metrics}

# --- 지표 선택 ---
st.sidebar.markdown("### 분석 설정")
selected_metrics = st.sidebar.multiselect(
    "표시할 지표",
    options=available_metrics,
    default=available_metrics[:2],
    format_func=lambda x: metric_options[x],
)

show_moving_avg = st.sidebar.checkbox("7일 이동평균 표시", value=True)

# --- 일별 추이 차트 ---
st.markdown("### 일별 추이")

if selected_metrics:
    daily = df.groupby("date")[selected_metrics].sum().reset_index().sort_values("date")

    fig = go.Figure()
    for i, metric in enumerate(selected_metrics):
        color = CHART_COLORS[i % len(CHART_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=daily["date"],
                y=daily[metric],
                name=metric_options[metric],
                line=dict(color=color, width=2),
                mode="lines+markers",
                marker=dict(size=4),
            )
        )
        # 7일 이동평균
        if show_moving_avg and len(daily) >= 7:
            ma = daily[metric].rolling(window=7, min_periods=1).mean()
            fig.add_trace(
                go.Scatter(
                    x=daily["date"],
                    y=ma,
                    name=f"{metric_options[metric]} (7일 평균)",
                    line=dict(color=color, width=1, dash="dash"),
                    mode="lines",
                    opacity=0.6,
                )
            )

    fig.update_layout(
        height=500,
        xaxis_title="날짜",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=20, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("왼쪽 메뉴에서 표시할 지표를 선택해주세요.")

# --- 주간/월간 비교 ---
st.markdown("### 기간 비교")
col1, col2 = st.columns(2)

compare_metric = st.selectbox(
    "비교할 지표",
    options=available_metrics,
    format_func=lambda x: metric_options[x],
)

with col1:
    fig_week = create_trend_comparison_chart(
        df, compare_metric, metric_options[compare_metric], "week"
    )
    st.plotly_chart(fig_week, use_container_width=True)

with col2:
    fig_month = create_trend_comparison_chart(
        df, compare_metric, metric_options[compare_metric], "month"
    )
    st.plotly_chart(fig_month, use_container_width=True)

# --- 요약 통계 ---
st.markdown("### 기간별 요약")

summary_period = st.radio("요약 단위", ["일별", "주별", "월별"], horizontal=True)

if summary_period == "일별":
    summary = df.groupby("date")[available_metrics].sum().reset_index()
    summary = summary.sort_values("date", ascending=False)
elif summary_period == "주별":
    df_copy = df.copy()
    df_copy["week"] = df_copy["date"].dt.to_period("W").apply(lambda r: r.start_time)
    summary = df_copy.groupby("week")[available_metrics].sum().reset_index()
    summary = summary.rename(columns={"week": "date"})
    summary = summary.sort_values("date", ascending=False)
else:
    df_copy = df.copy()
    df_copy["month"] = df_copy["date"].dt.to_period("M").apply(lambda r: r.start_time)
    summary = df_copy.groupby("month")[available_metrics].sum().reset_index()
    summary = summary.rename(columns={"month": "date"})
    summary = summary.sort_values("date", ascending=False)

# CTR 재계산 (합산이 아닌 비율)
if "impressions" in summary.columns and "clicks" in summary.columns:
    mask = summary["impressions"] > 0
    summary.loc[mask, "ctr"] = (summary.loc[mask, "clicks"] / summary.loc[mask, "impressions"]) * 100

# CPA 재계산
if "ad_spend" in summary.columns and "conversions" in summary.columns:
    mask = summary["conversions"] > 0
    summary.loc[mask, "cpa"] = summary.loc[mask, "ad_spend"] / summary.loc[mask, "conversions"]

display_summary = summary.rename(columns={m: metric_options.get(m, m) for m in available_metrics})
if "date" in display_summary.columns:
    display_summary = display_summary.rename(columns={"date": "날짜"})
    display_summary["날짜"] = display_summary["날짜"].dt.strftime("%Y-%m-%d")

st.dataframe(display_summary, use_container_width=True, height=400)
