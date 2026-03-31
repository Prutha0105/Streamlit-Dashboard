import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="Promoter Performance Dashboard",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.8;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    div[data-testid="metric-container"] {
        background-color: #1e1e2e;
        border: 1px solid #313244;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="metric-container"] > div {
        color: #cdd6f4;
    }
    div[data-testid="metric-container"] label {
        color: #a6adc8 !important;
    }
    .stSelectbox label, .stMultiSelect label, .stDateInput label {
        color: #cdd6f4;
        font-weight: 600;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #cba6f7;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── DUMMY DATA GENERATION ────────────────────────────────────────────────────

@st.cache_data
def generate_dummy_data():
    random.seed(42)
    np.random.seed(42)

    promoters = [
        "Live Nation", "AEG Presents", "SFX Entertainment",
        "Eventbrite Pro", "Ticketmaster Events", "Global Promotions",
        "StarStage Inc", "NightOwl Events"
    ]

    countries = ["USA", "UK", "Germany", "France", "Australia", "Canada", "India", "Japan", "Brazil", "UAE"]

    event_types = ["Concert", "Exhibition", "Trade Show", "Music Festival", "Stand-up Show", "Theater Show", "Sports Event", "Corporate Event"]

    venues = {
        "USA": ["Madison Square Garden", "Staples Center", "Hollywood Bowl", "Radio City Music Hall"],
        "UK": ["O2 Arena", "Wembley Stadium", "Royal Albert Hall", "Alexandra Palace"],
        "Germany": ["Mercedes-Benz Arena", "Olympiahalle Munich", "Lanxess Arena", "Barclaycard Arena"],
        "France": ["Accor Arena", "Zénith Paris", "Stade de France", "Le Grand Rex"],
        "Australia": ["Sydney Opera House", "Rod Laver Arena", "ICC Sydney", "Perth Arena"],
        "Canada": ["Rogers Centre", "Air Canada Centre", "Bell Centre", "Scotiabank Arena"],
        "India": ["NSCI Dome", "DY Patil Stadium", "Jawaharlal Nehru Stadium", "Pragati Maidan"],
        "Japan": ["Tokyo Dome", "Budokan", "Makuhari Messe", "Osaka-jo Hall"],
        "Brazil": ["Allianz Parque", "Maracanã", "Anhembi Arena", "Jeunesse Arena"],
        "UAE": ["Coca-Cola Arena", "Dubai World Trade Centre", "Abu Dhabi National Exhibition Centre", "Etihad Arena"],
    }

    records = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range_days = (end_date - start_date).days

    event_id = 1
    for _ in range(500):
        promoter = random.choice(promoters)
        country = random.choice(countries)
        event_type = random.choice(event_types)
        venue = random.choice(venues[country])
        event_date = start_date + timedelta(days=random.randint(0, date_range_days))

        total_capacity = random.choice([500, 1000, 2000, 3000, 5000, 8000, 10000, 15000, 20000, 50000])
        sold_pct = np.random.beta(6, 2)  # skewed toward high sales
        sold_capacity = int(total_capacity * sold_pct)
        tickets_left = total_capacity - sold_capacity

        ticket_price_base = {
            "Concert": (50, 250), "Exhibition": (20, 80), "Trade Show": (30, 150),
            "Music Festival": (80, 400), "Stand-up Show": (30, 120), "Theater Show": (40, 200),
            "Sports Event": (60, 500), "Corporate Event": (100, 600)
        }
        low, high = ticket_price_base[event_type]
        ticket_price = round(random.uniform(low, high), 2)
        revenue = round(sold_capacity * ticket_price, 2)

        event_name_templates = {
            "Concert": ["Rock Night", "Jazz Evening", "Pop Extravaganza", "Acoustic Sessions", "Grand Concert"],
            "Exhibition": ["Art Expo", "Tech Showcase", "Science Fair", "Cultural Exhibition", "Design Week"],
            "Trade Show": ["Industry Summit", "B2B Expo", "Innovation Fair", "Business Connect", "Market Days"],
            "Music Festival": ["Summer Beats", "Neon Fest", "Groove Festival", "Weekend Vibes", "Sound Wave"],
            "Stand-up Show": ["Comedy Night", "Laugh Factory", "Stand-up Special", "Comedy Gala", "Humor Fest"],
            "Theater Show": ["Broadway Nights", "Drama Night", "Classic Play", "Modern Theater", "Stage Stories"],
            "Sports Event": ["Championship Finals", "League Match", "Grand Prix", "Boxing Night", "Athletics Meet"],
            "Corporate Event": ["Annual Conference", "Leadership Summit", "Product Launch", "Awards Ceremony", "Gala Dinner"],
        }
        event_name = f"{random.choice(event_name_templates[event_type])} {event_id}"

        records.append({
            "event_id": event_id,
            "event_name": event_name,
            "promoter": promoter,
            "country": country,
            "event_type": event_type,
            "venue": venue,
            "event_date": event_date,
            "total_capacity": total_capacity,
            "sold_capacity": sold_capacity,
            "tickets_left": tickets_left,
            "ticket_price": ticket_price,
            "revenue": revenue,
            "sold_pct": round(sold_pct * 100, 1),
        })
        event_id += 1

    return pd.DataFrame(records)

df_full = generate_dummy_data()

# ─── SIDEBAR FILTERS ──────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<p class="sidebar-header">🎛️ Dashboard Filters</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Country filter
    all_countries = sorted(df_full["country"].unique().tolist())
    selected_countries = st.multiselect(
        "🌍 Select Countries",
        options=all_countries,
        default=all_countries,
        help="Filter by one or more countries"
    )

    st.markdown("---")

    # Date range filter
    min_date = df_full["event_date"].min().date()
    max_date = df_full["event_date"].max().date()

    date_from = st.date_input("📅 From Date", value=datetime(2024, 1, 1).date(), min_value=min_date, max_value=max_date)
    date_to = st.date_input("📅 To Date", value=max_date, min_value=min_date, max_value=max_date)

    st.markdown("---")

    # Promoter filter
    all_promoters = sorted(df_full["promoter"].unique().tolist())
    selected_promoters = st.multiselect(
        "🎤 Select Promoters",
        options=all_promoters,
        default=all_promoters,
        help="Filter by promoter"
    )

    st.markdown("---")

    # Event type filter
    all_event_types = sorted(df_full["event_type"].unique().tolist())
    selected_types = st.multiselect(
        "🎭 Event Types",
        options=all_event_types,
        default=all_event_types,
        help="Filter by event type"
    )

    st.markdown("---")
    st.markdown("**📊 Data Info**")
    st.caption(f"Total records in DB: {len(df_full):,}")

# ─── APPLY FILTERS ────────────────────────────────────────────────────────────

df = df_full[
    (df_full["country"].isin(selected_countries if selected_countries else all_countries)) &
    (df_full["promoter"].isin(selected_promoters if selected_promoters else all_promoters)) &
    (df_full["event_type"].isin(selected_types if selected_types else all_event_types)) &
    (df_full["event_date"].dt.date >= date_from) &
    (df_full["event_date"].dt.date <= date_to)
].copy()

# ─── HEADER ───────────────────────────────────────────────────────────────────

st.markdown('<h1 class="main-header">🎪 Promoter Performance Dashboard</h1>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#a6adc8; margin-top:-10px;'>Showing <b>{len(df):,}</b> events across <b>{df['country'].nunique()}</b> countries | {date_from} → {date_to}</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── TOP 5 KPIs ───────────────────────────────────────────────────────────────

if df.empty:
    st.warning("No data found for selected filters. Please adjust your filters.")
    st.stop()

total_events = len(df)
total_revenue = df["revenue"].sum()
avg_sold_pct = df["sold_pct"].mean()
total_audience = df["sold_capacity"].sum()
top_event_type = df.groupby("event_type")["revenue"].sum().idxmax()
top_promoter = df.groupby("promoter")["revenue"].sum().idxmax()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    prev = len(df_full) * 0.9
    st.metric("🎟️ Total Events", f"{total_events:,}", delta=f"{total_events - int(prev):+,} vs all-time 90%")
with col2:
    st.metric("💰 Total Revenue", f"${total_revenue/1_000_000:.2f}M", delta=f"Avg ${total_revenue/total_events:,.0f}/event")
with col3:
    st.metric("🎫 Avg Ticket Sold %", f"{avg_sold_pct:.1f}%", delta=f"{'Above' if avg_sold_pct >= 75 else 'Below'} 75% target")
with col4:
    st.metric("👥 Total Audience", f"{total_audience/1_000:.1f}K", delta=f"Avg {total_audience//total_events:,}/event")
with col5:
    st.metric("🏆 Top Event Type", top_event_type, delta=f"By {top_promoter}")

st.markdown("---")

# ─── TABS ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["📊 Overview Analytics", "🎯 Event Deep Dive", "🌍 Country & Promoter Intel"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns(2)

    # Chart 1 — Events by type per promoter (grouped bar)
    with col_a:
        st.subheader("📊 Events by Type per Promoter")
        df_prom_type = df.groupby(["promoter", "event_type"])["event_id"].count().reset_index(name="count")
        fig1 = px.bar(
            df_prom_type, x="promoter", y="count", color="event_type",
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"promoter": "Promoter", "count": "Number of Events", "event_type": "Event Type"},
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,30,46,0.8)",
            font_color="#cdd6f4", legend_title_text="Event Type",
            xaxis_tickangle=-30, height=400,
            xaxis=dict(gridcolor="#313244"), yaxis=dict(gridcolor="#313244")
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 — Revenue trend over time (line)
    with col_b:
        st.subheader("📈 Monthly Revenue Trend")
        df["month"] = df["event_date"].dt.to_period("M").astype(str)
        df_monthly = df.groupby(["month", "event_type"])["revenue"].sum().reset_index()
        fig2 = px.line(
            df_monthly, x="month", y="revenue", color="event_type",
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Vivid,
            labels={"month": "Month", "revenue": "Revenue ($)", "event_type": "Event Type"},
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,30,46,0.8)",
            font_color="#cdd6f4", height=400,
            xaxis_tickangle=-30,
            xaxis=dict(gridcolor="#313244", nticks=12), yaxis=dict(gridcolor="#313244")
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    # Chart 3 — Donut: Revenue share by event type
    with col_c:
        st.subheader("🍩 Revenue Share by Event Type")
        df_type_rev = df.groupby("event_type")["revenue"].sum().reset_index()
        fig3 = px.pie(
            df_type_rev, values="revenue", names="event_type", hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig3.update_traces(textinfo="percent+label", pull=[0.05]*len(df_type_rev))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_color="#cdd6f4", height=380,
            showlegend=True, legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4 — Scatter: Ticket price vs sold %
    with col_d:
        st.subheader("💡 Ticket Price vs Sold % (Bubble = Revenue)")
        fig4 = px.scatter(
            df.sample(min(300, len(df)), random_state=1),
            x="ticket_price", y="sold_pct",
            size="revenue", color="event_type",
            hover_name="event_name",
            hover_data=["promoter", "country", "venue"],
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={"ticket_price": "Ticket Price ($)", "sold_pct": "Sold %", "event_type": "Type"},
            size_max=40,
        )
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,30,46,0.8)",
            font_color="#cdd6f4", height=380,
            xaxis=dict(gridcolor="#313244"), yaxis=dict(gridcolor="#313244")
        )
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — EVENT DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🔍 Single Event Capacity & Sales Breakdown")
    st.markdown("Select a specific event to analyse its capacity, sales, ticket pricing and revenue performance.")

    # Selector
    event_options = df.sort_values("event_date", ascending=False)[["event_id", "event_name", "promoter", "country", "event_type", "venue", "event_date"]].copy()
    event_options["label"] = (
        event_options["event_name"] + " | " + event_options["event_type"] +
        " | " + event_options["country"] + " | " +
        event_options["event_date"].dt.strftime("%d %b %Y")
    )

    selected_label = st.selectbox(
        "🎟️ Choose an Event",
        options=event_options["label"].tolist(),
        help="Search by typing the event name, type, or country"
    )
    selected_row = df[df["event_id"] == event_options[event_options["label"] == selected_label]["event_id"].values[0]].iloc[0]

    # KPI row for the selected event
    ec1, ec2, ec3, ec4, ec5 = st.columns(5)
    with ec1:
        st.metric("🏟️ Total Capacity", f"{selected_row['total_capacity']:,}")
    with ec2:
        st.metric("✅ Sold Capacity", f"{selected_row['sold_capacity']:,}")
    with ec3:
        st.metric("🎫 Tickets Left", f"{selected_row['tickets_left']:,}")
    with ec4:
        st.metric("💵 Ticket Price", f"${selected_row['ticket_price']:.2f}")
    with ec5:
        st.metric("💰 Total Revenue", f"${selected_row['revenue']:,.0f}")

    st.markdown("---")

    col_left, col_right = st.columns([1.2, 0.8])

    with col_left:
        # Grouped bar chart for selected event
        fig_event = go.Figure()
        categories = ["Total Capacity", "Sold Capacity", "Tickets Left"]
        values = [selected_row["total_capacity"], selected_row["sold_capacity"], selected_row["tickets_left"]]
        colors = ["#7287fd", "#a6e3a1", "#f38ba8"]

        for cat, val, col in zip(categories, values, colors):
            fig_event.add_trace(go.Bar(
                name=cat, x=[cat], y=[val],
                marker_color=col,
                text=[f"{val:,}"],
                textposition="outside",
                textfont=dict(color="#cdd6f4", size=14),
                width=0.4
            ))

        fig_event.update_layout(
            title=f"Capacity Breakdown: {selected_row['event_name']}",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,30,46,0.8)",
            font_color="#cdd6f4", height=420, barmode="group",
            showlegend=True,
            xaxis=dict(gridcolor="#313244", showgrid=False),
            yaxis=dict(gridcolor="#313244", title="Seats"),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig_event, use_container_width=True)

    with col_right:
        # Gauge chart — sold percentage
        sold_pct_val = selected_row["sold_pct"]
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=sold_pct_val,
            number={"suffix": "%", "font": {"color": "#cdd6f4", "size": 36}},
            delta={"reference": 75, "increasing": {"color": "#a6e3a1"}, "decreasing": {"color": "#f38ba8"}},
            title={"text": "Tickets Sold %<br><span style='font-size:0.8em;color:#a6adc8'>vs 75% target</span>", "font": {"color": "#cdd6f4"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#cdd6f4", "tickfont": {"color": "#cdd6f4"}},
                "bar": {"color": "#cba6f7"},
                "bgcolor": "#313244",
                "borderwidth": 2,
                "bordercolor": "#585b70",
                "steps": [
                    {"range": [0, 50], "color": "#45475a"},
                    {"range": [50, 75], "color": "#585b70"},
                    {"range": [75, 100], "color": "#6c7086"},
                ],
                "threshold": {
                    "line": {"color": "#f38ba8", "width": 4},
                    "thickness": 0.75,
                    "value": 75
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_color="#cdd6f4", height=300
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Info card
        st.markdown(f"""
        <div style='background:#1e1e2e; border:1px solid #313244; border-radius:10px; padding:1rem; margin-top:0.5rem;'>
            <b style='color:#cba6f7'>📍 Venue:</b> <span style='color:#cdd6f4'>{selected_row['venue']}</span><br>
            <b style='color:#cba6f7'>🌍 Country:</b> <span style='color:#cdd6f4'>{selected_row['country']}</span><br>
            <b style='color:#cba6f7'>🎭 Type:</b> <span style='color:#cdd6f4'>{selected_row['event_type']}</span><br>
            <b style='color:#cba6f7'>📅 Date:</b> <span style='color:#cdd6f4'>{selected_row['event_date'].strftime('%d %B %Y')}</span><br>
            <b style='color:#cba6f7'>🎤 Promoter:</b> <span style='color:#cdd6f4'>{selected_row['promoter']}</span><br>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — COUNTRY & PROMOTER INTEL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col_e, col_f = st.columns(2)

    # Heatmap: Country vs Event Type (revenue)
    with col_e:
        st.subheader("🌡️ Revenue Heatmap: Country × Event Type")
        df_heat = df.groupby(["country", "event_type"])["revenue"].sum().reset_index()
        df_pivot = df_heat.pivot(index="country", columns="event_type", values="revenue").fillna(0)

        fig5 = px.imshow(
            df_pivot / 1_000_000,
            color_continuous_scale="Purples",
            labels=dict(x="Event Type", y="Country", color="Revenue ($M)"),
            aspect="auto",
        )
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_color="#cdd6f4", height=420,
            coloraxis_colorbar=dict(title="Revenue ($M)", tickfont=dict(color="#cdd6f4"), titlefont=dict(color="#cdd6f4"))
        )
        st.plotly_chart(fig5, use_container_width=True)

    # Horizontal bar: Top promoters by revenue
    with col_f:
        st.subheader("🏆 Promoter Revenue Ranking")
        df_prom_rev = df.groupby("promoter")["revenue"].sum().sort_values().reset_index()
        fig6 = px.bar(
            df_prom_rev, x="revenue", y="promoter", orientation="h",
            color="revenue", color_continuous_scale="Purpor",
            labels={"revenue": "Total Revenue ($)", "promoter": "Promoter"},
            text=df_prom_rev["revenue"].apply(lambda x: f"${x/1_000_000:.2f}M"),
        )
        fig6.update_traces(textposition="outside")
        fig6.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,30,46,0.8)",
            font_color="#cdd6f4", height=420, showlegend=False,
            xaxis=dict(gridcolor="#313244"), yaxis=dict(gridcolor="#313244"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig6, use_container_width=True)

    col_g, col_h = st.columns(2)

    # Treemap: Country → Event type → Revenue
    with col_g:
        st.subheader("🗺️ Revenue Treemap: Country → Event Type")
        df_tree = df.groupby(["country", "event_type"])["revenue"].sum().reset_index()
        fig7 = px.treemap(
            df_tree, path=["country", "event_type"], values="revenue",
            color="revenue", color_continuous_scale="Purples",
            hover_data={"revenue": ":$.2f"},
        )
        fig7.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_color="#cdd6f4", height=400,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig7, use_container_width=True)

    # Bar: Average sold % by country
    with col_h:
        st.subheader("📉 Avg Ticket Sold % by Country")
        df_country_sold = df.groupby("country")["sold_pct"].mean().sort_values(ascending=False).reset_index()
        df_country_sold.columns = ["country", "avg_sold_pct"]
        fig8 = px.bar(
            df_country_sold, x="country", y="avg_sold_pct",
            color="avg_sold_pct", color_continuous_scale="tealgrn",
            text=df_country_sold["avg_sold_pct"].apply(lambda x: f"{x:.1f}%"),
            labels={"country": "Country", "avg_sold_pct": "Avg Sold %"},
        )
        fig8.add_hline(y=75, line_dash="dot", line_color="#f38ba8", annotation_text="75% Target", annotation_font_color="#f38ba8")
        fig8.update_traces(textposition="outside")
        fig8.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,30,46,0.8)",
            font_color="#cdd6f4", height=400, showlegend=False,
            xaxis=dict(gridcolor="#313244"), yaxis=dict(gridcolor="#313244"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig8, use_container_width=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center; color:#585b70; font-size:0.8rem;'>Promoter Performance Dashboard • Built with Streamlit & Plotly • Dummy Data Only</p>", unsafe_allow_html=True)
