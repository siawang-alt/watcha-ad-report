"""CSV/엑셀 파일 읽기, 컬럼 매핑, 파생 지표 계산"""

from __future__ import annotations

import io

import chardet
import pandas as pd

from config.metrics import COLUMN_MAP, NUMERIC_COLUMNS, REQUIRED_COLUMNS


def detect_encoding(file_bytes: bytes) -> str:
    """파일의 문자 인코딩을 감지합니다 (한글 CSV 대응)."""
    result = chardet.detect(file_bytes)
    encoding = result.get("encoding", "utf-8")
    # chardet이 EUC-KR 계열로 감지하면 cp949 사용 (더 넓은 호환성)
    if encoding and encoding.lower() in ("euc-kr", "euc_kr", "iso-2022-kr"):
        return "cp949"
    return encoding or "utf-8"


def read_uploaded_file(uploaded_file) -> pd.DataFrame:
    """업로드된 파일(CSV 또는 엑셀)을 DataFrame으로 읽습니다."""
    file_bytes = uploaded_file.getvalue()
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        encoding = detect_encoding(file_bytes)
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
        except UnicodeDecodeError:
            # 인코딩 감지 실패 시 cp949로 재시도
            df = pd.read_csv(io.BytesIO(file_bytes), encoding="cp949")
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {filename}")

    return df


def auto_map_columns(df: pd.DataFrame) -> dict:
    """DataFrame의 컬럼명을 표준 컬럼명으로 자동 매핑합니다.

    Returns:
        매핑 딕셔너리 {원본 컬럼명: 표준 컬럼명}
    """
    mapping = {}
    for col in df.columns:
        col_stripped = col.strip()
        if col_stripped in COLUMN_MAP:
            mapping[col] = COLUMN_MAP[col_stripped]
        elif col_stripped.lower() in {k.lower(): v for k, v in COLUMN_MAP.items()}:
            lower_map = {k.lower(): v for k, v in COLUMN_MAP.items()}
            mapping[col] = lower_map[col_stripped.lower()]
    return mapping


def apply_column_mapping(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """컬럼 매핑을 적용하고 데이터를 정제합니다."""
    df = df.rename(columns=mapping)

    # 날짜 컬럼 파싱
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df = df.sort_values("date")

    # 숫자 컬럼 정제
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.replace("%", "")
                .str.replace("₩", "")
                .str.replace("원", "")
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def calculate_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """파생 지표를 계산합니다 (CTR, CPA, ROAS 등)."""
    df = df.copy()

    # CTR 계산 (데이터에 없거나 0인 경우)
    if "impressions" in df.columns and "clicks" in df.columns:
        mask = df["impressions"] > 0
        if "ctr" not in df.columns or df["ctr"].sum() == 0:
            df.loc[mask, "ctr"] = (df.loc[mask, "clicks"] / df.loc[mask, "impressions"]) * 100
            if "ctr" not in df.columns:
                df["ctr"] = 0.0

    # CPC 계산
    if "ad_spend" in df.columns and "clicks" in df.columns:
        mask = df["clicks"] > 0
        if "cpc" not in df.columns:
            df["cpc"] = 0.0
        df.loc[mask, "cpc"] = df.loc[mask, "ad_spend"] / df.loc[mask, "clicks"]

    # CPM 계산
    if "ad_spend" in df.columns and "impressions" in df.columns:
        mask = df["impressions"] > 0
        if "cpm" not in df.columns:
            df["cpm"] = 0.0
        df.loc[mask, "cpm"] = (df.loc[mask, "ad_spend"] / df.loc[mask, "impressions"]) * 1000

    # CPA 계산
    if "ad_spend" in df.columns and "conversions" in df.columns:
        mask = df["conversions"] > 0
        if "cpa" not in df.columns:
            df["cpa"] = 0.0
        df.loc[mask, "cpa"] = df.loc[mask, "ad_spend"] / df.loc[mask, "conversions"]

    # ROAS 계산
    if "revenue" in df.columns and "ad_spend" in df.columns:
        mask = df["ad_spend"] > 0
        if "roas" not in df.columns:
            df["roas"] = 0.0
        df.loc[mask, "roas"] = (df.loc[mask, "revenue"] / df.loc[mask, "ad_spend"]) * 100

    return df


def process_uploaded_file(uploaded_file, custom_mapping: dict | None = None) -> pd.DataFrame:
    """파일 업로드부터 최종 데이터프레임까지 전체 파이프라인을 실행합니다."""
    df = read_uploaded_file(uploaded_file)
    auto_mapping = auto_map_columns(df)

    # 사용자 커스텀 매핑이 있으면 합침
    if custom_mapping:
        auto_mapping.update(custom_mapping)

    df = apply_column_mapping(df, auto_mapping)
    df = calculate_derived_metrics(df)
    return df


def validate_data(df: pd.DataFrame) -> list[str]:
    """데이터의 필수 컬럼 존재 여부를 확인합니다.

    Returns:
        누락된 필수 컬럼 이름 리스트 (비어있으면 OK)
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing
