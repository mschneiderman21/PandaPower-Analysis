from pandapower.plotting.plotly import pf_res_plotly
import simbench as sb
import plotly.io as pio

sb_code = "1-MVLV-semiurb-3.202-1-no_sw" ##What network to use
net = sb.get_simbench_net(sb_code)

#net.bus_geodata.drop(net.bus_geodata.index, inplace=True)
#net.line_geodata.drop(net.line_geodata.index, inplace=True)

def custom_plotting():
    fig = pf_res_plotly(net, auto_open=False)

    x_coords = net.bus_geodata.x
    y_coords = net.bus_geodata.y

    bus = net.load.loc[12, 'bus']  ##Bus with scaled load attached to it
    bus_index = 0
    for x, y in zip(x_coords, y_coords):
        if(bus_index == bus):
            fig.add_annotation(
                x=x,
                y=y,
                text=str(bus_index),
                showarrow=False,
                font=dict(color='red', size=12)
            )
        else:
            fig.add_annotation(
                x=x,
                y=y,
                text=str(bus_index),
                showarrow=False,
                font=dict(color='black', size=8)
            )
        bus_index += 1
    fig.update_layout(showlegend=False)
    fig.show()


custom_plotting()


