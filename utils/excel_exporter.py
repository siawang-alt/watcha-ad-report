"""서식 있는 엑셀 리포트 생성"""

import io
from datetime import datetime

import pandas as pd
import xlsxwriter

from config.metrics import DISPLAY_NAMES, KPI_METRICS


def generate_excel_report(df: pd.DataFrame) -> bytes:
    """분석 데이터를 서식 있는 엑셀 리포트로 생성합니다.

    Returns:
        엑셀 파일의 바이트 데이터
    """
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {"in_memory": True})

    # --- 서식 정의 ---
    title_fmt = workbook.add_format({
        "bold": True, "font_size": 16, "font_color": "#333333",
        "bottom": 2, "bottom_color": "#FF2D78",
    })
    header_fmt = workbook.add_format({
        "bold": True, "font_size": 11, "bg_color": "#FF2D78",
        "font_color": "#FFFFFF", "border": 1, "text_wrap": True,
        "align": "center", "valign": "vcenter",
    })
    number_fmt = workbook.add_format({
        "num_format": "#,##0", "border": 1, "align": "right",
    })
    currency_fmt = workbook.add_format({
        "num_format": "₩#,##0", "border": 1, "align": "right",
    })
    percent_fmt = workbook.add_format({
        "num_format": "0.00%", "border": 1, "align": "right",
    })
    text_fmt = workbook.add_format({
        "border": 1, "align": "left",
    })
    date_fmt = workbook.add_format({
        "num_format": "yyyy-mm-dd", "border": 1, "align": "center",
    })
    kpi_label_fmt = workbook.add_format({
        "bold": True, "font_size": 12, "bg_color": "#F5F5F5",
        "border": 1, "align": "left",
    })
    kpi_value_fmt = workbook.add_format({
        "bold": True, "font_size": 14, "border": 1,
        "align": "right", "font_color": "#FF2D78",
    })

    # --- 시트 1: 요약 ---
    ws_summary = workbook.add_worksheet("요약")
    ws_summary.set_column("A:A", 20)
    ws_summary.set_column("B:B", 25)

    ws_summary.write("A1", "왓챠 광고 리포트", title_fmt)
    ws_summary.write("A2", f"생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    if "date" in df.columns:
        ws_summary.write("A3", f"데이터 기간: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")

    row = 5
    ws_summary.write(row, 0, "주요 지표", title_fmt)
    row += 1

    for metric_key, metric_info in KPI_METRICS.items():
        if metric_key in df.columns:
            if metric_key == "ctr":
                value = df["clicks"].sum() / df["impressions"].sum() * 100 if df["impressions"].sum() > 0 else 0
            elif metric_key == "cpa":
                value = df["ad_spend"].sum() / df["conversions"].sum() if "conversions" in df.columns and df["conversions"].sum() > 0 else 0
            else:
                value = df[metric_key].sum()

            ws_summary.write(row, 0, metric_info["label"], kpi_label_fmt)
            ws_summary.write(row, 1, metric_info["format"].format(value), kpi_value_fmt)
            row += 1

    # 캠페인 요약 테이블
    if "campaign" in df.columns:
        row += 2
        ws_summary.write(row, 0, "캠페인별 성과", title_fmt)
        row += 1

        agg_cols = {col: "sum" for col in ["impressions", "clicks", "ad_spend", "conversions"] if col in df.columns}
        if agg_cols:
            campaign_summary = df.groupby("campaign").agg(agg_cols).reset_index()
            if "impressions" in campaign_summary.columns and "clicks" in campaign_summary.columns:
                mask = campaign_summary["impressions"] > 0
                campaign_summary["ctr"] = 0.0
                campaign_summary.loc[mask, "ctr"] = campaign_summary.loc[mask, "clicks"] / campaign_summary.loc[mask, "impressions"]

            # 헤더
            headers = ["campaign"] + list(agg_cols.keys())
            if "ctr" in campaign_summary.columns:
                headers.append("ctr")

            for col_idx, h in enumerate(headers):
                ws_summary.write(row, col_idx, DISPLAY_NAMES.get(h, h), header_fmt)
            row += 1

            # 데이터
            for _, data_row in campaign_summary.iterrows():
                for col_idx, h in enumerate(headers):
                    value = data_row.get(h, "")
                    if h == "campaign":
                        ws_summary.write(row, col_idx, value, text_fmt)
                    elif h in ("ad_spend",):
                        ws_summary.write_number(row, col_idx, value, currency_fmt)
                    elif h == "ctr":
                        ws_summary.write_number(row, col_idx, value, percent_fmt)
                    else:
                        ws_summary.write_number(row, col_idx, value, number_fmt)
                row += 1

    # --- 시트 2: 일별 데이터 ---
    ws_daily = workbook.add_worksheet("일별 데이터")

    if "date" in df.columns:
        daily_metrics = [m for m in ["impressions", "clicks", "ctr", "ad_spend", "conversions", "cpc", "cpm", "cpa"] if m in df.columns]
        daily_agg = {col: "sum" for col in daily_metrics if col != "ctr"}
        daily = df.groupby("date").agg(daily_agg).reset_index().sort_values("date")

        # CTR 재계산
        if "impressions" in daily.columns and "clicks" in daily.columns:
            mask = daily["impressions"] > 0
            daily["ctr"] = 0.0
            daily.loc[mask, "ctr"] = daily.loc[mask, "clicks"] / daily.loc[mask, "impressions"]

        # CPA 재계산
        if "ad_spend" in daily.columns and "conversions" in daily.columns:
            mask = daily["conversions"] > 0
            daily["cpa"] = 0.0
            daily.loc[mask, "cpa"] = daily.loc[mask, "ad_spend"] / daily.loc[mask, "conversions"]

        all_daily_cols = ["date"] + [m for m in daily_metrics if m in daily.columns]

        # 헤더
        for col_idx, h in enumerate(all_daily_cols):
            ws_daily.write(0, col_idx, DISPLAY_NAMES.get(h, h), header_fmt)
            ws_daily.set_column(col_idx, col_idx, 15)

        # 데이터
        for row_idx, (_, data_row) in enumerate(daily.iterrows(), start=1):
            for col_idx, h in enumerate(all_daily_cols):
                value = data_row.get(h, "")
                if h == "date":
                    ws_daily.write_datetime(row_idx, col_idx, value.to_pydatetime(), date_fmt)
                elif h in ("ad_spend", "cpc", "cpm", "cpa"):
                    ws_daily.write_number(row_idx, col_idx, value, currency_fmt)
                elif h == "ctr":
                    ws_daily.write_number(row_idx, col_idx, value, percent_fmt)
                else:
                    ws_daily.write_number(row_idx, col_idx, value, number_fmt)

        # 차트 추가
        if len(daily) > 1 and "impressions" in daily.columns:
            chart = workbook.add_chart({"type": "line"})
            imp_col = all_daily_cols.index("impressions")
            chart.add_series({
                "name": "노출수",
                "categories": ["일별 데이터", 1, 0, len(daily), 0],
                "values": ["일별 데이터", 1, imp_col, len(daily), imp_col],
                "line": {"color": "#FF2D78", "width": 2},
            })
            if "clicks" in all_daily_cols:
                click_col = all_daily_cols.index("clicks")
                chart.add_series({
                    "name": "클릭수",
                    "categories": ["일별 데이터", 1, 0, len(daily), 0],
                    "values": ["일별 데이터", 1, click_col, len(daily), click_col],
                    "line": {"color": "#4A90D9", "width": 2},
                    "y2_axis": True,
                })
            chart.set_title({"name": "일별 노출수/클릭수 추이"})
            chart.set_size({"width": 720, "height": 400})
            chart.set_y_axis({"name": "노출수"})
            chart.set_y2_axis({"name": "클릭수"})
            ws_daily.insert_chart(f"A{len(daily) + 3}", chart)

    # --- 시트 3: 전체 원본 데이터 ---
    ws_raw = workbook.add_worksheet("전체 데이터")
    display_cols = [c for c in df.columns if c in DISPLAY_NAMES]
    other_cols = [c for c in df.columns if c not in DISPLAY_NAMES]
    all_cols = display_cols + other_cols

    for col_idx, h in enumerate(all_cols):
        ws_raw.write(0, col_idx, DISPLAY_NAMES.get(h, h), header_fmt)
        ws_raw.set_column(col_idx, col_idx, 15)

    for row_idx, (_, data_row) in enumerate(df.iterrows(), start=1):
        for col_idx, h in enumerate(all_cols):
            value = data_row.get(h, "")
            if h == "date" and pd.notna(value):
                ws_raw.write_datetime(row_idx, col_idx, value.to_pydatetime(), date_fmt)
            elif h in ("ad_spend", "cpc", "cpm", "cpa") and pd.notna(value):
                ws_raw.write_number(row_idx, col_idx, float(value), currency_fmt)
            elif h == "ctr" and pd.notna(value):
                ws_raw.write_number(row_idx, col_idx, float(value), percent_fmt)
            elif isinstance(value, (int, float)) and pd.notna(value):
                ws_raw.write_number(row_idx, col_idx, value, number_fmt)
            else:
                ws_raw.write(row_idx, col_idx, str(value) if pd.notna(value) else "", text_fmt)

    workbook.close()
    return output.getvalue()
