"""광고 지표 정의 및 컬럼 매핑 설정"""

# 왓챠 광고 대시보드 컬럼명 → 내부 표준 컬럼명 매핑
# 왓챠 대시보드에서 다운로드한 파일의 컬럼명이 변경되면 여기만 수정하면 됩니다.
COLUMN_MAP = {
    # 날짜/기간
    "날짜": "date",
    "일자": "date",
    "기간": "date",
    # 캠페인 구분
    "캠페인": "campaign",
    "캠페인명": "campaign",
    "캠페인 이름": "campaign",
    # 광고그룹
    "광고그룹": "ad_group",
    "광고그룹명": "ad_group",
    "광고 그룹": "ad_group",
    # 소재
    "소재": "creative",
    "소재명": "creative",
    "소재 이름": "creative",
    "광고소재": "creative",
    # 노출수
    "노출수": "impressions",
    "노출": "impressions",
    "임프레션": "impressions",
    "Impressions": "impressions",
    # 클릭수
    "클릭수": "clicks",
    "클릭": "clicks",
    "Clicks": "clicks",
    # 클릭률
    "클릭률": "ctr",
    "클릭률(%)": "ctr",
    "CTR": "ctr",
    "CTR(%)": "ctr",
    # 광고비
    "광고비": "ad_spend",
    "비용": "ad_spend",
    "소진액": "ad_spend",
    "소진 금액": "ad_spend",
    "Cost": "ad_spend",
    # 전환수
    "전환수": "conversions",
    "전환": "conversions",
    "Conversions": "conversions",
    # 매출/수익
    "매출": "revenue",
    "수익": "revenue",
    "Revenue": "revenue",
    # CPM
    "CPM": "cpm",
    # CPC
    "CPC": "cpc",
    # CPA
    "CPA": "cpa",
}

# 표준 컬럼명 → 한글 표시명 (UI에서 사용)
DISPLAY_NAMES = {
    "date": "날짜",
    "campaign": "캠페인",
    "ad_group": "광고그룹",
    "creative": "소재",
    "impressions": "노출수",
    "clicks": "클릭수",
    "ctr": "클릭률(%)",
    "ad_spend": "광고비(원)",
    "conversions": "전환수",
    "revenue": "매출(원)",
    "cpm": "CPM(원)",
    "cpc": "CPC(원)",
    "cpa": "CPA(원)",
    "roas": "ROAS(%)",
}

# 필수 컬럼 (이 컬럼들이 있어야 대시보드가 제대로 동작)
REQUIRED_COLUMNS = ["date", "impressions", "clicks", "ad_spend"]

# 숫자형으로 처리해야 하는 컬럼
NUMERIC_COLUMNS = [
    "impressions", "clicks", "ctr", "ad_spend",
    "conversions", "revenue", "cpm", "cpc", "cpa",
]

# KPI 카드에 표시할 지표와 포맷
KPI_METRICS = {
    "impressions": {"label": "총 노출수", "format": "{:,.0f}"},
    "clicks": {"label": "총 클릭수", "format": "{:,.0f}"},
    "ctr": {"label": "평균 CTR", "format": "{:.2f}%"},
    "ad_spend": {"label": "총 광고비", "format": "₩{:,.0f}"},
    "conversions": {"label": "총 전환수", "format": "{:,.0f}"},
    "cpa": {"label": "평균 CPA", "format": "₩{:,.0f}"},
}
