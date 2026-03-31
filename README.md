# Promoter Performance Dashboard

An interactive analytics dashboard built with **Streamlit** and **Plotly** to visualise promoter and event performance across countries, event types, and time periods.

## Features

- **KPI Summary** — total events, revenue, audience, avg ticket sold %, and top event type at a glance
- **Overview Analytics** — grouped bar charts, monthly revenue trends, revenue share donut, and ticket price vs sold % scatter plot
- **Event Deep Dive** — per-event capacity breakdown with a gauge chart showing sold % vs target
- **Country & Promoter Intel** — revenue heatmap, promoter ranking, treemap, and avg sold % by country
- **Sidebar Filters** — filter by country, date range, promoter, and event type

## Tech Stack

| Library | Purpose |
|---------|---------|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [NumPy](https://numpy.org) | Numerical operations |

## Quick Start

See [SETUP.md](SETUP.md) for full setup instructions.

```bash
pip install -r requirements.txt
streamlit run promoter_dashboard.py
```

## Project Structure

```
Streamlit-Dashboard/
├── promoter_dashboard.py   # Main application
├── requirements.txt        # Python dependencies
├── SETUP.md                # Setup instructions
└── README.md               # This file
```

> **Note:** The dashboard uses randomly generated dummy data for demonstration purposes.
