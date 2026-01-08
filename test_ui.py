from ui.layout import setup_page, render_header, render_dashboard_structure

# 1. Run Setup
setup_page()

# 2. Render Header
render_header()

# 3. Render Dashboard
live, chart, alerts = render_dashboard_structure()

# 4. Fill with Dummy Data to "See" the layout
live.info("Live Feed Container (Waiting for Data...)")
chart.line_chart([0, 10, 5, 20, 15])
alerts.error("Critical Alert Container (Waiting for Data...)")
