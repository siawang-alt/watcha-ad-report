"""미디어킷 페이지 — 왓챠 & 왓챠피디아 광고 상품 소개"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="미디어킷", page_icon="📖", layout="wide")

# --- 커스텀 스타일 ---
st.markdown(
    """
<style>
.product-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e9ecef;
    height: 100%;
}
.metric-highlight {
    font-size: 2.5rem;
    font-weight: 700;
    color: #FF2D78;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.9rem;
    color: #666;
}
.platform-badge-watcha {
    background: #FF2D78;
    color: white;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
}
.platform-badge-pedia {
    background: #4A90D9;
    color: white;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- 탭 선택 ---
tab_home, tab_watcha, tab_pedia, tab_products, tab_contact = st.tabs(
    ["🏠 홈", "🎬 왓챠", "📚 왓챠피디아", "📦 광고 상품", "📩 문의하기"]
)

# ===========================
# 홈 탭
# ===========================
with tab_home:
    st.markdown("# 콘텐츠 매니아 400만에게 다가가는 가장 확실한 방법")
    st.markdown("**왓챠 + 왓챠피디아**, 두 플랫폼의 MAU 400만 유저에게 광고를 전달하세요.")
    st.markdown("---")

    # 핵심 수치
    cols = st.columns(6)
    metrics = [
        ("400만", "통합 MAU"),
        ("7.5억+", "누적 별점"),
        ("77%", "20~30대 비율"),
        ("94%", "유료 구독자 비율"),
        ("3회/일", "일간 방문 빈도"),
        ("7년 연속 1위", "OTT 부문 브랜드"),
    ]
    for col, (value, label) in zip(cols, metrics):
        col.markdown(
            f'<div style="text-align:center">'
            f'<div class="metric-highlight">{value}</div>'
            f'<div class="metric-label">{label}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # 플랫폼 비교
    st.markdown("### 두 플랫폼 한눈에 비교")

    compare_data = {
        "항목": ["MAU", "주요 서비스", "핵심 유저", "유저 특성", "광고 특징"],
        "왓챠": [
            "약 100만",
            "OTT 구독형 스트리밍",
            "20~30대 (64%)",
            "유료 구독자 94%, 일 2시간 체류",
            "앱 진입 시 높은 주목도, 브랜딩에 최적",
        ],
        "왓챠피디아": [
            "약 300만",
            "콘텐츠 평가/리뷰 커뮤니티",
            "20~30대 (77%)",
            "주간 12.2회 방문, 누적 별점 7.5억",
            "높은 방문 빈도, 다양한 지면에 노출",
        ],
    }
    st.dataframe(
        pd.DataFrame(compare_data).set_index("항목"),
        use_container_width=True,
    )

    # 유저 프로필 차트
    st.markdown("### 유저 프로필")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            names=["여성", "남성"],
            values=[56, 44],
            title="성별 비율",
            color_discrete_sequence=["#FF2D78", "#4A90D9"],
        )
        fig.update_layout(height=300, margin=dict(t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            names=["20~30대", "기타"],
            values=[77, 23],
            title="연령 비율",
            color_discrete_sequence=["#FF2D78", "#E0E0E0"],
        )
        fig.update_layout(height=300, margin=dict(t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)


# ===========================
# 왓챠 탭
# ===========================
with tab_watcha:
    st.markdown("# 🎬 왓챠 (WATCHA)")
    st.markdown("MZ세대가 매일 3번씩 방문하여 2시간씩 머무르는 OTT 플랫폼")
    st.markdown("---")

    cols = st.columns(4)
    cols[0].metric("MAU", "약 100만")
    cols[1].metric("일간 방문", "약 3회")
    cols[2].metric("일일 체류시간", "약 2시간")
    cols[3].metric("유료 구독자", "94%")

    st.markdown("---")
    st.markdown("### 왓챠 광고 상품")

    # 스플래시
    st.markdown("#### 1. 스플래시 (앱 진입 전체화면)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
앱 실행 시 **진입 화면에 단독 노출**되어 유저 주목도가 높으며, 브랜드 인지도를 높이는 데 적합합니다.

- **노출 위치**: 앱 진입 시 전체화면(풀) 또는 하단(파셜)
- **구좌**: 총 1구좌, 1주일 단독 노출
- **디바이스**: APP (iOS, Android)
- **소재**: 이미지 소재만 가능
"""
        )
    with col2:
        st.markdown(
            """
| 항목 | 내용 |
|------|------|
| **예상 노출수** | 약 50만 |
"""
        )

    st.markdown("---")

    # 보드 배너
    st.markdown("#### 2. 보드 배너")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
앱, 웹 총 **4개 지면** 내 First View에 드로어 형태로 노출되어 우수한 노출량을 기록합니다.

- **노출 위치**: 홈 / 개봉관 / 웹툰 / 콘텐츠 상세 페이지
- **구좌**: 총 1구좌, 1주일 단독 노출
- **디바이스**: APP + WEB (PC, Mobile)
- **소재**: 이미지 소재, 외부 랜딩 가능
"""
        )
    with col2:
        st.markdown(
            """
| 항목 | 내용 |
|------|------|
| **예상 노출수** | 약 200만 |
| **예상 CTR** | 약 0.21% |
"""
        )

    st.markdown("---")

    # 전면 팝업
    st.markdown("#### 3. 전면 팝업 배너")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
앱, 웹 진입 시 **팝업 형태**로 노출되며 높은 유저 주목도를 바탕으로 클릭 효과를 극대화합니다.

- **노출 위치**: 앱, 웹 진입 시 전면 팝업
- **구좌**: 총 2구좌, 1주일 50% 랜덤 노출
- **디바이스**: APP + WEB (PC, Mobile)
- **소재**: 이미지 소재, 외부 랜딩 가능
"""
        )
    with col2:
        st.markdown(
            """
| 항목 | 내용 |
|------|------|
| **예상 노출수** | 약 45만 |
| **예상 CTR** | 약 2.1% |
"""
        )


# ===========================
# 왓챠피디아 탭
# ===========================
with tab_pedia:
    st.markdown("# 📚 왓챠피디아 (WATCHA PEDIA)")
    st.markdown("7.5억 별점 데이터 기반, 콘텐츠를 좋아하는 사람들의 놀이터")
    st.markdown("---")

    cols = st.columns(4)
    cols[0].metric("MAU", "약 300만")
    cols[1].metric("주간 방문", "12.2회")
    cols[2].metric("누적 별점", "7.5억+")
    cols[3].metric("누적 가입자", "1,387만")

    st.markdown("---")
    st.markdown("### 왓챠피디아 광고 상품")

    products_pedia = [
        {
            "name": "1. 전면 팝업 배너",
            "desc": "앱, 웹 진입 시 팝업 형태로 노출. 높은 유저 주목도를 바탕으로 클릭 효과를 극대화.",
            "location": "앱, 웹 진입 시 전면 팝업",
            "slots": "총 2구좌, 1주일 50% 랜덤 노출",
            "device": "APP + WEB",
            "price": "",
            "impressions": "약 60만",
            "ctr": "약 2.9%",
            "material": "이미지 소재, 외부 랜딩 가능",
        },
        {
            "name": "2. 빅배너",
            "desc": "홈 화면 및 왓챠피디아 세상 페이지에 위치. 이미지/동영상 소재 가능, 가장 유입이 많은 페이지에 노출되어 클릭을 유도.",
            "location": "메인 홈 화면 / 왓챠피디아 세상 페이지",
            "slots": "총 2구좌, 1주일 50% 랜덤 노출",
            "device": "APP + WEB",
            "price": "",
            "impressions": "약 150만",
            "ctr": "약 0.24%",
            "material": "이미지 및 동영상 소재 가능, 외부 랜딩 가능",
        },
        {
            "name": "3. 밀어 배너",
            "desc": "홈 밀어넣기 1지면에 노출되며 3초 뒤 다른 구좌로 전환. 주목도가 높은 영역에 이미지 소재를 노출시켜 클릭 유도.",
            "location": "메인 홈 화면 밀어 배너 1지면",
            "slots": "총 2구좌, 1주일 50% 랜덤 노출",
            "device": "APP + WEB",
            "price": "",
            "impressions": "약 70만",
            "ctr": "약 0.6%",
            "material": "이미지 소재, 외부 랜딩 가능",
        },
        {
            "name": "4. 드로어 배너",
            "desc": "앱, 웹 총 6개 지면 내 First View에 드로어 형태로 노출되어 우수한 노출량을 기록하고 클릭을 유도.",
            "location": "홈 / 왓챠피디아 세상 / 검색 / 나의 왓챠 / 컬렉션 세상 등 6개 지면",
            "slots": "총 2구좌, 1주일 50% 랜덤 노출",
            "device": "APP + WEB",
            "price": "",
            "impressions": "약 500만",
            "ctr": "약 0.12%",
            "material": "이미지 소재, 외부 랜딩 가능",
        },
        {
            "name": "5. 랭킹 HOT 배너",
            "desc": "메인 홈 > 왓챠피디아 HOT 랭킹 탭 2순위 위치에 노출. 포스터 클릭 시 아웃랜딩 유도 가능.",
            "location": "왓챠피디아 HOT 랭킹 2순위 위치",
            "slots": "총 2구좌, 1주일 50% 랜덤 노출",
            "device": "APP + WEB",
            "price": "",
            "impressions": "약 45만",
            "ctr": "약 1%",
            "material": "영화/왓챠피디아 관련 콘텐츠만 가능, 이미지 소재, 외부 랜딩 가능",
        },
        {
            "name": "6. 스플래시",
            "desc": "앱 실행 시 진입 화면에 단독 노출되어 유저 주목도가 높으며, 브랜드 인지도를 높이는 데 적합.",
            "location": "앱 진입 시 전체화면(풀) 또는 하단(파셜)",
            "slots": "총 1구좌, 1주일 단독 노출",
            "device": "APP (iOS, Android)",
            "price": "",
            "impressions": "약 50만",
            "ctr": "-",
            "material": "이미지 소재만 가능",
        },
        {
            "name": "7. 유저 참여 이벤트",
            "desc": "다양한 문화 예술 왓챠피디아에 대해 유저 참여 이벤트 집행 가능. 전면 팝업 배너 3일 포함되어 이벤트 인지도를 높일 수 있음.",
            "location": "검색 > 이벤트 탭 1주일 노출 + 전면 팝업 3일",
            "slots": "이벤트 전용 구좌",
            "device": "APP + WEB",
            "price": "",
            "impressions": "약 20만",
            "ctr": "약 5,000명 참여",
            "material": "추가 광고 집행 시 할인 적용",
        },
        {
            "name": "8. 전용관 페이지",
            "desc": "메인 홈 > 핫 아이템에 노출. 아이템 클릭 시 왓챠피디아에서 구축한 전용관 페이지로 랜딩.",
            "location": "홈 핫 아이템 클릭 시 전용관 페이지로 이동",
            "slots": "광고 구좌 / 핫 아이템 / 전용 페이지 / 미디어믹스",
            "device": "APP + WEB",
            "price": "",
            "impressions": "-",
            "ctr": "-",
            "material": "영화/왓챠피디아 관련 콘텐츠 외 커스텀 드로어 집행 가능",
        },
    ]

    for product in products_pedia:
        st.markdown(f"#### {product['name']}")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(
                f"""
{product['desc']}

- **노출 위치**: {product['location']}
- **구좌**: {product['slots']}
- **디바이스**: {product['device']}
- **소재**: {product.get('material', '이미지 소재, 외부 랜딩 가능')}
"""
            )
        with col2:
            st.markdown(
                f"""
| 항목 | 내용 |
|------|------|
| **예상 노출수** | {product['impressions']} |
| **예상 CTR** | {product['ctr']} |
"""
            )
        st.markdown("---")


# ===========================
# 상품 비교 탭
# ===========================
with tab_products:
    st.markdown("# 📦 전체 광고 상품 비교")
    st.markdown("왓챠 & 왓챠피디아의 모든 광고 상품을 한눈에 비교하세요.")
    st.markdown("---")

    # 필터
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        platform_filter = st.multiselect(
            "플랫폼",
            ["왓챠", "왓챠피디아"],
            default=["왓챠", "왓챠피디아"],
        )
    with col_filter2:
        purpose_filter = st.multiselect(
            "광고 목적",
            ["브랜딩/인지도", "클릭 유도", "높은 노출량"],
            default=["브랜딩/인지도", "클릭 유도", "높은 노출량"],
        )

    # 상품 데이터
    all_products = pd.DataFrame(
        [
            {
                "플랫폼": "왓챠",
                "상품명": "스플래시",
                "예상 노출수(만)": 50,
                "예상 CTR(%)": None,
                "구좌": "1구좌 단독",
                "디바이스": "APP",
                "특징": "브랜딩/인지도",
            },
            {
                "플랫폼": "왓챠",
                "상품명": "보드 배너",
                "예상 노출수(만)": 200,
                "예상 CTR(%)": 0.21,
                "구좌": "1구좌 단독",
                "디바이스": "APP+WEB",
                "특징": "높은 노출량",
            },
            {
                "플랫폼": "왓챠",
                "상품명": "전면 팝업 배너",
                "예상 노출수(만)": 45,
                "예상 CTR(%)": 2.1,
                "구좌": "2구좌 50%",
                "디바이스": "APP+WEB",
                "특징": "클릭 유도",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "전면 팝업 배너",
                "예상 노출수(만)": 60,
                "예상 CTR(%)": 2.9,
                "구좌": "2구좌 50%",
                "디바이스": "APP+WEB",
                "특징": "클릭 유도",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "빅배너",
                "예상 노출수(만)": 150,
                "예상 CTR(%)": 0.24,
                "구좌": "2구좌 50%",
                "디바이스": "APP+WEB",
                "특징": "높은 노출량",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "밀어 배너",
                "예상 노출수(만)": 70,
                "예상 CTR(%)": 0.6,
                "구좌": "2구좌 50%",
                "디바이스": "APP+WEB",
                "특징": "클릭 유도",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "드로어 배너",
                "예상 노출수(만)": 500,
                "예상 CTR(%)": 0.12,
                "구좌": "2구좌 50%",
                "디바이스": "APP+WEB",
                "특징": "높은 노출량",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "랭킹 HOT 배너",
                "예상 노출수(만)": 45,
                "예상 CTR(%)": 1.0,
                "구좌": "2구좌 50%",
                "디바이스": "APP+WEB",
                "특징": "클릭 유도",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "스플래시",
                "예상 노출수(만)": 50,
                "예상 CTR(%)": None,
                "구좌": "1구좌 단독",
                "디바이스": "APP",
                "특징": "브랜딩/인지도",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "유저 참여 이벤트",
                "예상 노출수(만)": 20,
                "예상 CTR(%)": None,
                "구좌": "이벤트 전용",
                "디바이스": "APP+WEB",
                "특징": "클릭 유도",
            },
            {
                "플랫폼": "왓챠피디아",
                "상품명": "전용관 페이지",
                "예상 노출수(만)": None,
                "예상 CTR(%)": None,
                "구좌": "전용 페이지",
                "디바이스": "APP+WEB",
                "특징": "높은 노출량",
            },
        ]
    )

    # 필터 적용
    filtered = all_products[all_products["플랫폼"].isin(platform_filter)]
    if purpose_filter:
        filtered = filtered[filtered["특징"].isin(purpose_filter)]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    # 노출수 비교 차트
    imp_data = filtered.dropna(subset=["예상 노출수(만)"])
    if not imp_data.empty:
        st.markdown("### 상품별 예상 노출수 비교")
        fig = px.bar(
            imp_data,
            x="상품명",
            y="예상 노출수(만)",
            color="플랫폼",
            text="예상 노출수(만)",
            color_discrete_map={"왓챠": "#FF2D78", "왓챠피디아": "#4A90D9"},
            height=450,
        )
        fig.update_traces(texttemplate="%{text}만", textposition="outside")
        fig.update_layout(xaxis_title="", yaxis_title="예상 노출수 (만)")
        st.plotly_chart(fig, use_container_width=True)

    # CTR 비교 차트
    ctr_data = filtered.dropna(subset=["예상 CTR(%)"])
    if not ctr_data.empty:
        st.markdown("### 상품별 예상 CTR 비교")
        fig2 = px.bar(
            ctr_data,
            x="상품명",
            y="예상 CTR(%)",
            color="플랫폼",
            text="예상 CTR(%)",
            color_discrete_map={"왓챠": "#FF2D78", "왓챠피디아": "#4A90D9"},
            height=400,
        )
        fig2.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig2.update_layout(xaxis_title="", yaxis_title="CTR (%)")
        st.plotly_chart(fig2, use_container_width=True)

    # 위약금 안내
    st.markdown("---")
    with st.expander("⚠️ 위약금 규정"):
        st.markdown(
            """
왓챠 광고는 **기간보장 상품**으로 양 사 날인 이후 계약 변경/취소 시 위약금이 발생합니다.

| 적용 일정 | 위약금 |
|-----------|--------|
| 광고 집행일로부터 **13~7 영업일 전** | 광고 최종 단가의 **50%** |
| 광고 집행일로부터 **6영업일 전 ~ 라이브 이후** | 광고 최종 단가의 **100%** |
"""
        )


# ===========================
# 문의하기 탭
# ===========================
with tab_contact:
    st.markdown("# 📩 광고 문의하기")
    st.markdown("왓챠 광고에 관심이 있으시면 아래 정보를 남겨주세요. 담당자가 1영업일 이내 연락드리겠습니다.")
    st.markdown("---")

    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("회사명 *")
            name = st.text_input("담당자 이름 *")
            email = st.text_input("이메일 *")
        with col2:
            phone = st.text_input("연락처 (선택)")
            purpose = st.selectbox(
                "광고 목적 (선택)",
                ["선택해주세요", "브랜드 인지도", "클릭 유도", "전환/가입", "이벤트 참여"],
            )
            budget = st.text_input("희망 집행 시기 (선택)")

        interested = st.multiselect(
            "관심 상품 (선택, 복수 선택 가능)",
            [
                "왓챠 - 스플래시",
                "왓챠 - 보드 배너",
                "왓챠 - 전면 팝업",
                "왓챠피디아 - 전면 팝업",
                "왓챠피디아 - 빅배너",
                "왓챠피디아 - 밀어 배너",
                "왓챠피디아 - 드로어 배너",
                "패키지 추천 받고 싶어요",
            ],
        )

        message = st.text_area("문의 내용 (선택)")

        submitted = st.form_submit_button("문의 보내기", type="primary", use_container_width=True)
        if submitted:
            if not company or not name or not email:
                st.error("회사명, 담당자 이름, 이메일은 필수 항목입니다.")
            else:
                st.success(
                    f"문의가 접수되었습니다! {name}님, 1영업일 이내에 {email}로 연락드리겠습니다."
                )
                st.balloons()

    st.markdown("---")
    st.markdown(
        """
**직접 연락하기**

- 📧 이메일: ad_sales@watcha.com
- 📱 전화: 010-5033-9698
- 👤 WATCHA 광고사업팀
"""
    )
