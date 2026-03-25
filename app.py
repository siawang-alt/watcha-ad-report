"""왓챠 광고 리포팅 대시보드 - 메인 페이지"""

import streamlit as st
import pandas as pd

from utils.data_processor import (
    read_uploaded_file,
    auto_map_columns,
    apply_column_mapping,
    calculate_derived_metrics,
)
from config.metrics import DISPLAY_NAMES

st.set_page_config(
    page_title="왓챠 광고 리포트",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("왓챠 광고 리포팅 대시보드")

st.markdown("---")

# --- 빠른 업로드 & 자동 요약 ---
st.markdown("### 파일을 올리면 바로 요약해드립니다")

uploaded_file = st.file_uploader(
    "왓챠 대시보드에서 다운로드한 파일을 여기에 드래그하세요",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is not None:
    try:
        raw_df = read_uploaded_file(uploaded_file)
        mapping = auto_map_columns(raw_df)
        df = apply_column_mapping(raw_df, mapping)
        df = calculate_derived_metrics(df)
        st.session_state.df = df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()

if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df

    # --- 기간 정보 ---
    st.markdown("---")
    st.markdown("### 📋 전체 요약")

    if "date" in df.columns:
        st.caption(
            f"기간: **{df['date'].min().strftime('%Y-%m-%d')}** ~ **{df['date'].max().strftime('%Y-%m-%d')}** "
            f"({(df['date'].max() - df['date'].min()).days + 1}일간)"
        )

    # --- KPI 카드 ---
    cols = st.columns(6)

    total_impressions = df["impressions"].sum() if "impressions" in df.columns else 0
    total_clicks = df["clicks"].sum() if "clicks" in df.columns else 0
    total_spend = df["ad_spend"].sum() if "ad_spend" in df.columns else 0
    total_conversions = df["conversions"].sum() if "conversions" in df.columns else 0
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0

    cols[0].metric("총 노출수", f"{total_impressions:,.0f}")
    cols[1].metric("총 클릭수", f"{total_clicks:,.0f}")
    cols[2].metric("평균 CTR", f"{avg_ctr:.2f}%")
    cols[3].metric("총 광고비", f"₩{total_spend:,.0f}")
    cols[4].metric("총 전환수", f"{total_conversions:,.0f}")
    cols[5].metric("평균 CPA", f"₩{avg_cpa:,.0f}")

    # --- 캠페인별 요약 테이블 ---
    if "campaign" in df.columns:
        st.markdown("### 📊 캠페인별 요약")

        agg_dict = {}
        if "impressions" in df.columns:
            agg_dict["impressions"] = "sum"
        if "clicks" in df.columns:
            agg_dict["clicks"] = "sum"
        if "ad_spend" in df.columns:
            agg_dict["ad_spend"] = "sum"
        if "conversions" in df.columns:
            agg_dict["conversions"] = "sum"

        campaign_df = df.groupby("campaign").agg(agg_dict).reset_index()

        # CTR, CPA 계산
        if "impressions" in campaign_df.columns and "clicks" in campaign_df.columns:
            mask = campaign_df["impressions"] > 0
            campaign_df["ctr"] = 0.0
            campaign_df.loc[mask, "ctr"] = (
                campaign_df.loc[mask, "clicks"] / campaign_df.loc[mask, "impressions"] * 100
            )
        if "ad_spend" in campaign_df.columns and "conversions" in campaign_df.columns:
            mask = campaign_df["conversions"] > 0
            campaign_df["cpa"] = 0.0
            campaign_df.loc[mask, "cpa"] = (
                campaign_df.loc[mask, "ad_spend"] / campaign_df.loc[mask, "conversions"]
            )

        # 광고비 기준 내림차순
        if "ad_spend" in campaign_df.columns:
            campaign_df = campaign_df.sort_values("ad_spend", ascending=False)

        # 한글 컬럼명으로 표시
        display_campaign = campaign_df.rename(
            columns={k: v for k, v in DISPLAY_NAMES.items() if k in campaign_df.columns}
        )
        st.dataframe(display_campaign, use_container_width=True, hide_index=True)

    # --- 일별 요약 테이블 ---
    if "date" in df.columns:
        st.markdown("### 📅 일별 요약")

        daily_agg = {}
        for col in ["impressions", "clicks", "ad_spend", "conversions"]:
            if col in df.columns:
                daily_agg[col] = "sum"

        daily_df = df.groupby("date").agg(daily_agg).reset_index().sort_values("date", ascending=False)

        if "impressions" in daily_df.columns and "clicks" in daily_df.columns:
            mask = daily_df["impressions"] > 0
            daily_df["ctr"] = 0.0
            daily_df.loc[mask, "ctr"] = (
                daily_df.loc[mask, "clicks"] / daily_df.loc[mask, "impressions"] * 100
            )

        daily_df["date"] = daily_df["date"].dt.strftime("%Y-%m-%d")

        display_daily = daily_df.rename(
            columns={k: v for k, v in DISPLAY_NAMES.items() if k in daily_df.columns}
        )
        st.dataframe(display_daily, use_container_width=True, hide_index=True)

    # --- 하단 안내 ---
    st.markdown("---")
    st.caption("👈 왼쪽 메뉴에서 '대시보드', '트렌드 분석', '보고서 다운로드'를 선택하면 더 자세한 분석을 볼 수 있습니다.")

else:
    st.markdown(
        """
> **사용 방법**: 위에 파일을 올리면 자동으로 노출수, 클릭수, CTR, 광고비 등을 요약해드립니다.
>
> 왼쪽 메뉴에서 더 자세한 분석도 확인할 수 있습니다.
"""
    )
