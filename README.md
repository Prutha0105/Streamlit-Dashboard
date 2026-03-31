# 🎪 Promoter Performance Dashboard

An interactive analytics dashboard built with **Streamlit** and **Plotly** to visualise promoter and event performance across countries, event types, and time periods — all powered by dummy data for demonstration.

---

## 📸 Screenshots

> To add screenshots: run the dashboard, take screenshots of each section, save them in a `screenshots/` folder, then replace the placeholder paths below.

### 1. Full Dashboard Overview
![Dashboard Overview](screenshots/dashboard_overview.png)
*The main dashboard view showing KPI cards at the top and the three analytics tabs.*

### 2. Sidebar Filters
![Sidebar Filters](screenshots/sidebar_filters.png)
*The collapsible sidebar with filters for country, date range, promoter, and event type.*

### 3. Tab 1 — Overview Analytics
![Overview Analytics](screenshots/tab1_overview.png)
*Four interactive charts: events by type per promoter, monthly revenue trend, revenue share donut, and ticket price vs sold % bubble chart.*

### 4. Tab 2 — Event Deep Dive
![Event Deep Dive](screenshots/tab2_event_deepdive.png)
*Per-event capacity breakdown bar chart, sold % gauge, and event info card.*

### 5. Tab 3 — Country & Promoter Intel
![Country & Promoter Intel](screenshots/tab3_country_promoter.png)
*Revenue heatmap by country × event type, promoter revenue ranking, treemap, and avg sold % by country.*

---

## 🚀 Features

### KPI Summary Bar
Five headline metrics update dynamically based on your sidebar filters:

| Metric | Description |
|--------|-------------|
| 🎟️ Total Events | Number of events matching current filters |
| 💰 Total Revenue | Sum of revenue across filtered events |
| 🎫 Avg Ticket Sold % | Average percentage of capacity sold |
| 👥 Total Audience | Total tickets sold (sum of sold capacity) |
| 🏆 Top Event Type | Highest revenue-generating event category |

---

### 🎛️ Sidebar Filters
Filter the entire dashboard in real time using:
- **Countries** — multi-select from 10 countries (USA, UK, Germany, France, Australia, Canada, India, Japan, Brazil, UAE)
- **Date Range** — from/to date pickers covering Jan 2023 – Dec 2025
- **Promoters** — multi-select from 8 promoters (Live Nation, AEG Presents, etc.)
- **Event Types** — multi-select from 8 types (Concert, Festival, Trade Show, etc.)

All charts and KPIs update instantly when filters change.

---

### 📊 Tab 1 — Overview Analytics

#### Events by Type per Promoter (Grouped Bar Chart)
Shows how each promoter distributes their events across different event types. Useful for understanding each promoter's specialisation and portfolio mix.

#### Monthly Revenue Trend (Line Chart)
Tracks total revenue per event type month-over-month. Helps identify seasonal peaks, high-performing months, and growth trends over the 2023–2025 period.

#### Revenue Share by Event Type (Donut Chart)
Displays the percentage contribution of each event type to total revenue. Quickly highlights which categories drive the most income.

#### Ticket Price vs Sold % — Bubble Chart
Scatter plot where each bubble is an event. The X-axis shows ticket price, Y-axis shows % of tickets sold, and bubble size represents total revenue. Reveals the relationship between pricing strategy and sellout rate.

---

### 🎯 Tab 2 — Event Deep Dive

A drill-down view for a single selected event. Choose any event from the dropdown (searchable by name, type, or country) to see:

- **Capacity Breakdown Bar Chart** — side-by-side bars for Total Capacity, Sold Capacity, and Tickets Left
- **Sold % Gauge** — a speedometer-style gauge showing the sold percentage against a 75% target threshold
- **Event Info Card** — venue, country, event type, date, and promoter at a glance

---

### 🌍 Tab 3 — Country & Promoter Intel

#### Revenue Heatmap: Country × Event Type
A colour-intensity grid showing revenue (in $M) for every country–event type combination. Darker purple = higher revenue. Identifies which markets perform best for which event categories.

#### Promoter Revenue Ranking (Horizontal Bar)
All promoters ranked by total revenue, displayed as horizontal bars with dollar values annotated. Instantly shows who the top earners are.

#### Revenue Treemap: Country → Event Type
A hierarchical area chart where each rectangle represents a country, subdivided by event type proportional to revenue. Great for spotting dominant markets and event mix at a glance.

#### Avg Ticket Sold % by Country (Bar Chart)
Average sell-through rate per country with a dashed 75% target line. Shows which markets are consistently selling out vs underperforming.

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| [Streamlit](https://streamlit.io) | ≥ 1.32 | Web app framework |
| [Plotly](https://plotly.com/python/) | ≥ 5.20 | Interactive charts |
| [Pandas](https://pandas.pydata.org) | ≥ 2.0 | Data manipulation |
| [NumPy](https://numpy.org) | ≥ 1.26 | Numerical operations |

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
streamlit run promoter_dashboard.py
```

Opens automatically at `http://localhost:8501`. See [SETUP.md](SETUP.md) for virtual environment setup and troubleshooting.

---

## 📁 Project Structure

```
Streamlit-Dashboard/
├── promoter_dashboard.py   # Main application (all charts, filters, layout)
├── requirements.txt        # Python dependencies
├── SETUP.md                # Step-by-step setup guide
├── README.md               # This file
└── screenshots/            # Add your screenshots here
    ├── dashboard_overview.png
    ├── sidebar_filters.png
    ├── tab1_overview.png
    ├── tab2_event_deepdive.png
    └── tab3_country_promoter.png
```

---

## 📌 Data

The dashboard uses **500 randomly generated events** with a fixed random seed (reproducible). Data includes:
- 8 promoters, 10 countries, 8 event types
- Event dates from January 2023 to December 2025
- Ticket prices and capacities vary by event type
- Sell-through rates skewed toward high sales using a Beta distribution

> All data is synthetic and for demonstration purposes only.
