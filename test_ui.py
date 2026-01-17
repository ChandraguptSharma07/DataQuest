from ui.layout import setup_page, render_header, render_dashboard_structure

setup_page()
render_header()
live, chart, alerts = render_dashboard_structure()
live.info("Live Feed Container (Waiting for Data...)")
chart.line_chart([0, 10, 5, 20, 15])
alerts.error("Critical Alert Container (Waiting for Data...)")
