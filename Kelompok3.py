# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cp-yeCkiR3IwP6bwkVYKf6m_KjBzVlfL

**Kelompok 3**


1.   Agus Adi Pranata (1301184292)
2.   Pieter Edward (1301184479)
3.   Hauzan Jiyad Dhoifullah Komara (1301180212)
4.   Muhammad Sabil Naufal Mas (1301184193)

**Import Library**
"""

from bokeh.plotting import figure, show
from bokeh.io import output_file, output_notebook, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import row, widgetbox

import pandas as pd

"""**Load data from excel**"""

data = pd.read_excel("nasdaqStock.xlsx")

data.drop(columns=['Open', 'High', 'Low', 'Close'], inplace=True)

data_stock = data.rename(columns={"Adj Close": "Adj_Close"})

data.index = data.index.map(str)

"""**Set Select Option**"""

# Select sorted by stock name
option = data_stock['Name'].drop_duplicates()

option = list(option.map(str))

# Select 1 for stock 1
select1 = Select(
    options=option,
    title='Select stock 1',
    value=option[0]
)

# Select 2 for stock 2
select2 = Select(
    options=option,
    title='Select stock 2',
    value=option[1]
)

stock1 = select1.value
stock2 = select2.value

"""**Plotting Stock by Volume**"""

data_stock['Date'] = pd.to_datetime(data_stock['Date'])

output_notebook()

#membuat variabel baru untuk menampung setiap indeks saham
stocks1 = data_stock[data_stock['Name'] == stock1]
stocks2 = data_stock[data_stock['Name'] == stock2]

#membuat column data source untuk setiap index saham
data1 = ColumnDataSource(stocks1)
data2 = ColumnDataSource(stocks2)

#membuat plot figure untuk adj close
plot = figure(x_axis_type='datetime', x_axis_label='Date', y_axis_label='Volume', title='Stock Volume', plot_height=600, plot_width=1200)

#plot adj close untuk setiap indeks saham menggunakan line plot
plot.line(x='Date', y='Volume', source=data1, color='red')
plot.line(x='Date', y='Volume', source=data2, color='green')

plot.legend.location = "top_left"

#menambahkan hover tool
plot.add_tools(HoverTool(tooltips=[("Stock Name", "@Name"),("Volume", "@Volume"),]))

#show plot
show(plot)

"""**Update Function**"""

def update_plot(attr, old, new):
    stock1 = select1.value
    stock2 = select2.value

    new_stocks1 = data_stock[data_stock['Name'] == stock1]
    new_stocks2 = data_stock[data_stock['Name'] == stock2]

    data1 = new_stocks1
    data2 = new_stocks2

    plot.xaxis.axis_label = stock1
    plot.yaxis.axis_label = stock2

"""**Mengatur Select**"""

# if stock selected
select1.on_change('value', update_plot)
select2.on_change('value', update_plot)

"""**Set layout, panel, and tabs**"""

# make layout with widget
layout1 = row(widgetbox(select1, select2,), plot)

# make panel
line_panel = Panel(child=layout1, title='Line Vizualization')

# union panel to be tab
tabs = Tabs(tabs=[line_panel])

curdoc().add_root(tabs)
