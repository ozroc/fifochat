from bokeh.embed import file_html
from bokeh.resources import CDN
import bokeh.plotting
import numpy.fft.fftpack as fftpack



def generate_dashboard(data):
    if len(data) == 0:
        return 'Empty data set'
    data.sort(key=lambda x: x['timestamp'])
    x=map(lambda x: x['timestamp'], data)
    # this base_plot is just for xrange synchronization
    base_plot = bokeh.plotting.figure(width=800, height=250,x_axis_type="datetime")
    base_plot.circle(x, x)
    figures=[]
    for key in data[0]['data'].keys():
        figure=bokeh.plotting.figure(
            width=800, 
            height=250,
            title=key,
            x_axis_type="datetime",
            x_range=base_plot.x_range)
        y=map(lambda x: x['data'][key], data)
        figure.circle(x,y)
        figure2=bokeh.plotting.figure(
            width=800, 
            height=250,
            title='FFT: %s' % key)
        y2 = fftpack.fft(y)
        x2=range(len(y))
        figure2.line(x2,y2)
        figures.append(bokeh.plotting.hbox(figure,figure2))
    
    return file_html(bokeh.plotting.vplot(*figures), CDN, "my plot")
