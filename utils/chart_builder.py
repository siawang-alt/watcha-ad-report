"""Plotly 차트 생성 함수들"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


CHART_COLORS = ["#FF2D78", "#4A90D9", "#50C878", "#FFB347", "#9B59B6", "#E74C3C"]


def create_kpi_bar_chart(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    title: str,
    color: str = CHART_COLORS[0],
) -> go.Figure:
    """그룹별 막대 차트를 생성합니다."""
    grouped = df.groupby(group_col)[value_col].sum().sort_values(ascending=False).head(15)
    fig = px.bar(
        x=grouped.index,
        y=grouped.values,
        title=title,
        labels={"x": group_col, "y": value_col},
        color_discrete_sequence=[color],
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400,
        margin=dict(t=40, b=80),
    )
    return fig


def create_daily_trend_chart(
    df: pd.DataFrame,
    metrics: list[str],
    metric_labels: dict[str, str],
    title: str = "일별 추이",
) -> go.Figure:
    """일별 추이 라인 차트를 생성합니다."""
    if "date" not in df.columns:
        return go.Figure()

    daily = df.groupby("date")[metrics].sum().reset_index()
    fig = go.Figure()

    for i, metric in enumerate(metrics):
        if metric in daily.columns:
            fig.add_trace(
                go.Scatter(
                    x=daily["date"],
                    y=daily[metric],
                    name=metric_labels.get(metric, metric),
                    line=dict(color=CHART_COLORS[i % len(CHART_COLORS)], width=2),
                    mode="lines+markers",
                    marker=dict(size=4),
                )
            )

    fig.update_layout(
        title=title,
        xaxis_title="날짜",
        height=400,
        margin=dict(t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    title: str,
) -> go.Figure:
    """그룹별 비율 파이 차트를 생성합니다."""
    grouped = df.groupby(group_col)[value_col].sum().sort_values(ascending=False)
    # 상위 8개 + 나머지
    if len(grouped) > 8:
        top = grouped.head(8)
        others = pd.Series({"기타": grouped[8:].sum()})
        grouped = pd.concat([top, others])

    fig = px.pie(
        names=grouped.index,
        values=grouped.values,
        title=title,
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_layout(height=400, margin=dict(t=40, b=40))
    return fig


def create_scatter_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: str | None,
    title: str,
    x_label: str = "",
    y_label: str = "",
) -> go.Figure:
    """산점도 차트를 생성합니다."""
    if group_col and group_col in df.columns:
        grouped = df.groupby(group_col)[[x_col, y_col]].sum().reset_index()
        fig = px.scatter(
            grouped,
            x=x_col,
            y=y_col,
            text=group_col,
            title=title,
            labels={x_col: x_label or x_col, y_col: y_label or y_col},
            color_discrete_sequence=[CHART_COLORS[1]],
        )
        fig.update_traces(textposition="top center", marker=dict(size=10))
    else:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=title,
            labels={x_col: x_label or x_col, y_col: y_label or y_col},
            color_discrete_sequence=[CHART_COLORS[1]],
        )
    fig.update_layout(height=400, margin=dict(t=40, b=40))
    return fig


def create_trend_comparison_chart(
    df: pd.DataFrame,
    metric: str,
    metric_label: str,
    period: str = "week",
) -> go.Figure:
    """주간/월간 비교 차트를 생성합니다."""
    if "date" not in df.columns:
        return go.Figure()

    daily = df.groupby("date")[[metric]].sum().reset_index()
    daily = daily.sort_values("date")

    if period == "week":
        daily["period"] = daily["date"].dt.isocalendar().week.astype(str) + "주차"
        daily["day_in_period"] = daily["date"].dt.dayofweek
        day_labels = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
        daily["day_label"] = daily["day_in_period"].map(day_labels)
    else:
        daily["period"] = daily["date"].dt.strftime("%Y-%m")
        daily["day_in_period"] = daily["date"].dt.day
        daily["day_label"] = daily["day_in_period"].astype(str) + "일"

    # 최근 4개 기간만
    recent_periods = daily["period"].unique()[-4:]
    daily = daily[daily["period"].isin(recent_periods)]

    fig = px.line(
        daily,
        x="day_label",
        y=metric,
        color="period",
        title=f"{metric_label} — {'주간' if period == 'week' else '월간'} 비교",
        labels={"day_label": "", metric: metric_label, "period": "기간"},
        color_discrete_sequence=CHART_COLORS,
        markers=True,
    )
    fig.update_layout(height=400, margin=dict(t=40, b=40))
    return fig
