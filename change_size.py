from pyecharts.charts import Page
Page.save_resize_html(
    source="chart.html",
    cfg_file="./charts_config.json",
    dest="my_new_charts.html"
)
