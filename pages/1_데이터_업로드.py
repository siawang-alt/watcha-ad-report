"""데이터 업로드 페이지 — CSV/엑셀 파일 업로드 및 컬럼 매핑"""

import streamlit as st
import pandas as pd

from utils.data_processor import (
    read_uploaded_file,
    auto_map_columns,
    apply_column_mapping,
    calculate_derived_metrics,
    validate_data,
)
from config.metrics import DISPLAY_NAMES, REQUIRED_COLUMNS

st.set_page_config(page_title="데이터 업로드", page_icon="📁", layout="wide")
st.title("📁 데이터 업로드")
st.markdown("왓챠 광고 대시보드에서 다운로드한 CSV 또는 엑셀 파일을 업로드하세요.")

# --- 파일 업로드 ---
uploaded_file = st.file_uploader(
    "파일을 선택하세요",
    type=["csv", "xlsx", "xls"],
    help="왓챠 광고 대시보드에서 다운로드한 CSV 또는 엑셀 파일",
)

if uploaded_file is not None:
    # 1단계: 파일 읽기
    try:
        raw_df = read_uploaded_file(uploaded_file)
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()

    st.success(f"파일을 성공적으로 읽었습니다: {len(raw_df):,}행 × {len(raw_df.columns)}열")

    # 2단계: 컬럼 매핑
    st.markdown("### 컬럼 매핑")
    st.markdown("파일의 컬럼이 자동으로 매핑되었습니다. 필요하면 수정해주세요.")

    auto_mapping = auto_map_columns(raw_df)

    # 매핑 가능한 표준 컬럼 목록
    standard_cols = ["(매핑 안 함)"] + list(DISPLAY_NAMES.keys())
    standard_labels = ["(매핑 안 함)"] + [f"{DISPLAY_NAMES[k]} ({k})" for k in DISPLAY_NAMES]

    # 컬럼 매핑 UI
    mapping = {}
    cols_per_row = 3
    raw_columns = list(raw_df.columns)

    for i in range(0, len(raw_columns), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col_widget in enumerate(cols):
            idx = i + j
            if idx >= len(raw_columns):
                break
            original_col = raw_columns[idx]
            # 자동 매핑된 값이 있으면 기본값으로 설정
            default_idx = 0
            if original_col in auto_mapping:
                mapped = auto_mapping[original_col]
                if mapped in standard_cols:
                    default_idx = standard_cols.index(mapped)

            selected = col_widget.selectbox(
                f"**{original_col}**",
                options=standard_labels,
                index=default_idx,
                key=f"map_{idx}",
            )

            if selected != "(매핑 안 함)":
                # 라벨에서 영문 키 추출
                std_key = standard_cols[standard_labels.index(selected)]
                mapping[original_col] = std_key

    # 3단계: 매핑 적용 및 데이터 처리
    st.markdown("---")

    if st.button("✅ 매핑 적용 및 데이터 처리", type="primary", use_container_width=True):
        df = apply_column_mapping(raw_df, mapping)
        df = calculate_derived_metrics(df)

        # 필수 컬럼 검증
        missing = validate_data(df)
        if missing:
            missing_names = [DISPLAY_NAMES.get(m, m) for m in missing]
            st.warning(
                f"다음 필수 항목이 매핑되지 않았습니다: **{', '.join(missing_names)}**\n\n"
                "위에서 해당 컬럼을 매핑해주세요. 일부 차트가 표시되지 않을 수 있습니다."
            )

        # session_state에 저장
        st.session_state.df = df
        st.success("데이터 처리가 완료되었습니다! 왼쪽 메뉴에서 '대시보드'를 클릭하세요.")

        # 데이터 미리보기
        st.markdown("### 처리된 데이터 미리보기")

        # 한글 컬럼명으로 표시
        display_df = df.copy()
        display_rename = {k: v for k, v in DISPLAY_NAMES.items() if k in display_df.columns}
        display_df = display_df.rename(columns=display_rename)
        st.dataframe(display_df.head(20), use_container_width=True)

        # 기본 통계
        st.markdown("### 데이터 요약")
        summary_cols = st.columns(4)
        summary_cols[0].metric("총 행 수", f"{len(df):,}")
        if "date" in df.columns:
            summary_cols[1].metric(
                "데이터 기간",
                f"{df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}",
            )
        if "campaign" in df.columns:
            summary_cols[2].metric("캠페인 수", f"{df['campaign'].nunique()}")
        mapped_count = len([c for c in REQUIRED_COLUMNS if c in df.columns])
        summary_cols[3].metric("매핑된 필수 항목", f"{mapped_count}/{len(REQUIRED_COLUMNS)}")

elif "df" in st.session_state and st.session_state.df is not None:
    st.info("이미 데이터가 로드되어 있습니다. 새 파일을 업로드하면 기존 데이터가 교체됩니다.")
    st.dataframe(st.session_state.df.head(10), use_container_width=True)
