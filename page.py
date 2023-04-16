from pyecharts.charts import Bar, Line, Pie, Scatter, Page, Map, EffectScatter
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.components import Table, Image
from pyecharts.globals import ThemeType
THEME=ThemeType.INFOGRAPHIC
df = pd.read_excel('data.xlsx')	 	 #读取csv数据
#数据来源地区图
def create_map() -> Map:
    data=[('郑州市',1121)]
    c = Map(init_opts=opts.InitOpts(theme=THEME,chart_id='geo'))
    c.add('数据量',data_pair=data,maptype='河南')
    c.set_global_opts(
        title_opts=opts.TitleOpts(title='天气数据来源地区图', pos_left='center', pos_top='top'),
        legend_opts=opts.LegendOpts(is_show=False)
    )
    return c

#天气类型折线图
def create_bar_zs() -> Bar:
    tianqi=(df['白天'].value_counts()+df['晚上'].value_counts()).sort_values(ascending=False).to_dict()
    c = (
        Bar(init_opts=opts.InitOpts(theme=THEME,chart_id='bar_zs'))
        .add_xaxis(list(tianqi.keys()))
        .add_yaxis("天气", list(tianqi.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="天气类型统计",pos_left='center', pos_top='top'),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return c

#风向饼图
def create_pie_fx() -> Pie:
    fx_key = df['风向'].value_counts()[:-1].keys().tolist()
    fx_value = df['风向'].value_counts()[:-1].values.tolist()
    c = (
        Pie(init_opts=opts.InitOpts(theme=THEME,chart_id='pie_fx'))
        .add(
            "风向",
            [list(z) for z in zip(fx_key, fx_value)],
            center=["50%", "50%"],
            radius=[65, 100],
            label_opts=opts.LabelOpts(
                formatter="{b}: {d}%"
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="风向占比",
                pos_left="center",
                pos_top="top",
            ),
            legend_opts=opts.LegendOpts(
                # is_show=False,
                orient="vertical",
                pos_top="middle",
                pos_right="left",
            ),
        )
    )
    return c

#风级饼图
def create_pie_fj() -> Pie:
    fj_keys = df['风级'].value_counts()[:-1].keys().tolist()
    fj_values = df['风级'].value_counts().values.tolist()
    fj_keys_ji = []
    for i in fj_keys:
        fj_keys_ji.append(str(i)+'级')
    c = (
        Pie(init_opts=opts.InitOpts(theme=THEME,chart_id='pie_fj'))
        .add(
            "风级",
            [list(z) for z in zip(fj_keys_ji, fj_values)],
            center=["50%", "50%"],
            radius=[65, 100],
            label_opts=opts.LabelOpts(
                formatter="{b}: {d}%"
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="风级占比",
                pos_left="center",
                pos_top="top",
            ),
            legend_opts=opts.LegendOpts(
                # is_show=False,
                orient="vertical",
                pos_top="middle",
                pos_left="left",
            ),
        )
    )
    return c

#AQI散点图
def create_scatter() -> Scatter:
    aqi = df['AQI'].values.tolist()
    date= df['日期'].values.tolist()
    c = (
        Scatter(init_opts=opts.InitOpts(theme=THEME,chart_id='scatter'))
        .add_xaxis(date[::-1])
        .add_yaxis("AQI", aqi[::-1],symbol_size=8,label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="AQI散点图",pos_left='center', pos_top='top'),
        legend_opts=opts.LegendOpts(is_show=False),)
    )
    return c

#气温折线图
def create_line() -> Line:
    date = df['日期'].values.tolist()
    qw = df['平均温度'].values.tolist()
    c = (
        Line(init_opts=opts.InitOpts(theme=THEME,chart_id='line'))
        .add_xaxis(date[::-1])
        .add_yaxis("平均气温", qw[::-1])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每日平均气温",pos_left='center', pos_top='top'),
            xaxis_opts=opts.AxisOpts(name="日期"),
            yaxis_opts=opts.AxisOpts(name="气温"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return c

#降水量
def create_bar_js() -> EffectScatter:
    #判断降水量不为0的日期
    date = df.query('降水量!=0')['日期'].tolist()
    #判断降水量不为0的降水量
    jsl = df.query('降水量!=0')['降水量'].tolist()
    c = (
        Bar(init_opts=opts.InitOpts(theme=THEME,chart_id='bar_js'))
        .add_xaxis(date[::-1])
        .add_yaxis("降水量", jsl[::-1],label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="降水量",pos_left='center', pos_top='top'),
        legend_opts=opts.LegendOpts(is_show=False),)
    )
    return c

def create_page() -> Page:
    charts=[create_map(),create_bar_zs(),create_pie_fx(),create_pie_fj(),create_scatter(),create_line(),create_bar_js()]
    for i in range(len(charts)):
        charts[i].chart_id=str(i+1)
    page = (
        Page(page_title="郑州2020-3至2023天气分析大屏",layout=Page.DraggablePageLayout)
        .add(*charts)
    )
    return page

if __name__ == "__main__":
    page = create_page()
    page.render('chart.html')
    page.save_resize_html('chart.html',cfg_file='./chart_config.json',dest='charts.html')
