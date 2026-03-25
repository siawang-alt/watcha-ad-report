"""대시보드 페이지 — 핵심 광고 성과 지표 및 차트"""

import streamlit as st
import pandas as pd

from config.metrics import DISPLAY_NAMES, KPI_METRICS
from utils.chart_builder import (
    create_kpi_bar_chart,
    create_daily_trend_chart,
    create_pie_chart,
    create_scatter_chart,
)

st.set_page_config(page_title="대시보드", page_icon="📊", layout="wide")
st.title("📊 광고 성과 대시보드")

# --- 데이터 확인 ---
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("데이터가 없습니다. '데이터 업로드' 페이지에서 파일을 먼저 업로드해주세요.")
    st.stop()

df = st.session_state.df.copy()

# --- 필터 ---
st.sidebar.markdown("### 필터")

# 날짜 필터
if "date" in df.columns:
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.sidebar.date_input(
        "날짜 범위",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if len(date_range) == 2:
        start, end = date_range
        df = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)]

# 캠페인 필터
if "campaign" in df.columns:
    campaigns = ["전체"] + sorted(df["campaign"].unique().tolist())
    selected_campaign = st.sidebar.selectbox("캠페인", campaigns)
    if selected_campaign != "전체":
        df = df[df["campaign"] == selected_campaign]

# 광고그룹 필터
if "ad_group" in df.columns:
    ad_groups = ["전체"] + sorted(df["ad_group"].unique().tolist())
    selected_ad_group = st.sidebar.selectbox("광고그룹", ad_groups)
    if selected_ad_group != "전체":
        df = df[df["ad_group"] == selected_ad_group]

# --- KPI 카드 ---
st.markdown("### 주요 지표")
kpi_cols = st.columns(len(KPI_METRICS))

for i, (metric_key, metric_info) in enumerate(KPI_METRICS.items()):
    if metric_key in df.columns:
        if metric_key == "ctr":
            value = df["clicks"].sum() / df["impressions"].sum() * 100 if df["impressions"].sum() > 0 else 0
        elif metric_key == "cpa":
            value = df["ad_spend"].sum() / df["conversions"].sum() if "conversions" in df.columns and df["conversions"].sum() > 0 else 0
        else:
            value = df[metric_key].sum()
        kpi_cols[i].metric(
            metric_info["label"],
            metric_info["format"].format(value),
        )
    else:
        kpi_cols[i].metric(metric_info["label"], "—")

st.markdown("---")

# --- 차트 ---
# 1행: 캠페인별 노출수/클릭수 + 광고비 분포
col1, col2 = st.columns(2)

group_col = "campaign" if "campaign" in df.columns else None

if group_col:
    with col1:
        if "impressions" in df.columns:
            fig = create_kpi_bar_chart(df, group_col, "impressions", "캠페인별 노출수")
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        if "ad_spend" in df.columns:
            fig = create_pie_chart(df, group_col, "ad_spend", "캠페인별 광고비 비율")
            st.plotly_chart(fig, use_container_width=True)

# 2행: 일별 추이 + 효율 분석
col3, col4 = st.columns(2)

with col3:
    trend_metrics = [m for m in ["impressions", "clicks"] if m in df.columns]
    if trend_metrics and "date" in df.columns:
        fig = create_daily_trend_chart(
            df,
            trend_metrics,
            {m: DISPLAY_NAMES.get(m, m) for m in trend_metrics},
            "일별 노출수 · 클릭수 추이",
        )
        st.plotly_chart(fig, use_container_width=True)

with col4:
    if "ad_spend" in df.columns and "conversions" in df.columns and group_col:
        fig = create_scatter_chart(
            df,
            "ad_spend",
            "conversions",
            group_col,
            "광고비 vs 전환수 (캠페인별)",
            x_label="광고비(원)",
            y_label="전환수",
        )
        st.plotly_chart(fig, use_container_width=True)
    elif "ad_spend" in df.columns and "clicks" in df.columns and group_col:
        fig = create_scatter_chart(
            df,
            "ad_spend",
            "clicks",
            group_col,
            "광고비 vs 클릭수 (캠페인별)",
            x_label="광고비(원)",
            y_label="클릭수",
        )
        st.plotly_chart(fig, use_container_width=True)

# 3행: 광고비/CTR 추이
if "date" in df.columns:
    spend_metrics = [m for m in ["ad_spend", "ctr"] if m in df.columns]
    if spend_metrics:
        fig = create_daily_trend_chart(
            df,
            spend_metrics,
            {m: DISPLAY_NAMES.get(m, m) for m in spend_metrics},
            "일별 광고비 · CTR 추이",
        )
        st.plotly_chart(fig, use_container_width=True)

# --- 상세 데이터 테이블 ---
with st.expander("📋 상세 데이터 보기"):
    display_df = df.copy()
    display_rename = {k: v for k, v in DISPLAY_NAMES.items() if k in display_df.columns}
    display_df = display_df.rename(columns=display_rename)
    st.dataframe(display_df, use_container_width=True, height=400)
