#the basic steps to creatign plots with the bokeh.plotting interface are:
"""- Prepare some data
- Tell Bokeh where to generate output
- call figure() to create a plot with some overrall options like
  title, tools and axes labels
- add renderers for our data, with visual customizations like colors,
  legends and widths to the plotself.
- ask bokeh to show() or save() the results.
"""

from bokeh.plotting import figure, output_file, show

x=[1,2,3,4,5]
y=[6,7,2,4,5]

output_file("output.html")

p=figure(title="Simple line example",
            x_axis_label='x', y_axis_label='y')

p.line(x,y,legend="test line", line_width=3)

show(p)
