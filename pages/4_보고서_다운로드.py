"""보고서 다운로드 페이지 — 엑셀 리포트 생성 및 다운로드"""

from datetime import datetime

import streamlit as st

from config.metrics import DISPLAY_NAMES, KPI_METRICS
from utils.excel_exporter import generate_excel_report

st.set_page_config(page_title="보고서 다운로드", page_icon="📥", layout="wide")
st.title("📥 보고서 다운로드")

# --- 데이터 확인 ---
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("데이터가 없습니다. '데이터 업로드' 페이지에서 파일을 먼저 업로드해주세요.")
    st.stop()

df = st.session_state.df

# --- 리포트 미리보기 ---
st.markdown("### 리포트에 포함될 내용")

st.markdown(
    """
엑셀 파일에 다음 내용이 포함됩니다:

| 시트 | 내용 |
|------|------|
| **요약** | 주요 KPI 지표 + 캠페인별 성과 테이블 |
| **일별 데이터** | 일별 집계 데이터 + 노출수/클릭수 추이 차트 |
| **전체 데이터** | 업로드한 원본 데이터 전체 |
"""
)

# KPI 미리보기
st.markdown("### 주요 지표 미리보기")
kpi_cols = st.columns(len(KPI_METRICS))

for i, (metric_key, metric_info) in enumerate(KPI_METRICS.items()):
    if metric_key in df.columns:
        if metric_key == "ctr":
            value = df["clicks"].sum() / df["impressions"].sum() * 100 if df["impressions"].sum() > 0 else 0
        elif metric_key == "cpa":
            value = df["ad_spend"].sum() / df["conversions"].sum() if "conversions" in df.columns and df["conversions"].sum() > 0 else 0
        else:
            value = df[metric_key].sum()
        kpi_cols[i].metric(metric_info["label"], metric_info["format"].format(value))
    else:
        kpi_cols[i].metric(metric_info["label"], "—")

# --- 다운로드 ---
st.markdown("---")
st.markdown("### 엑셀 리포트 다운로드")

today = datetime.now().strftime("%Y%m%d")

if "date" in df.columns:
    start = df["date"].min().strftime("%Y%m%d")
    end = df["date"].max().strftime("%Y%m%d")
    filename = f"왓챠_광고리포트_{start}_{end}.xlsx"
else:
    filename = f"왓챠_광고리포트_{today}.xlsx"

excel_bytes = generate_excel_report(df)

st.download_button(
    label="📥 엑셀 리포트 다운로드",
    data=excel_bytes,
    file_name=filename,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    type="primary",
    use_container_width=True,
)

st.caption(f"파일명: {filename} | 데이터: {len(df):,}행")
