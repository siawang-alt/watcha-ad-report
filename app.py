"""왓챠 광고 리포팅 대시보드 - 메인 페이지"""

import streamlit as st

st.set_page_config(
    page_title="왓챠 광고 리포트",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("왓챠 광고 리포팅 대시보드")

st.markdown("---")

st.markdown(
    """
### 사용 방법

1. **데이터 업로드** — 왓챠 광고 대시보드에서 다운로드한 CSV 또는 엑셀 파일을 업로드합니다.
2. **대시보드** — 주요 광고 성과 지표(노출수, 클릭수, CTR, 광고비 등)를 차트와 함께 확인합니다.
3. **트렌드 분석** — 기간별 추이를 분석하고 주간/월간 비교를 확인합니다.
4. **보고서 다운로드** — 분석 결과를 엑셀 파일로 자동 생성하여 다운로드합니다.

👈 왼쪽 메뉴에서 원하는 페이지를 선택하세요.
"""
)

# 현재 데이터 상태 표시
if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    st.success(f"데이터 로드 완료: {len(df):,}개 행")

    col1, col2, col3 = st.columns(3)
    if "date" in df.columns:
        col1.metric("데이터 기간", f"{df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
    if "campaign" in df.columns:
        col2.metric("캠페인 수", f"{df['campaign'].nunique()}개")
    col3.metric("데이터 행 수", f"{len(df):,}개")
else:
    st.info("아직 데이터가 업로드되지 않았습니다. '데이터 업로드' 페이지에서 파일을 업로드해주세요.")
