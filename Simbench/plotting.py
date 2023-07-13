from pandapower.plotting.plotly import pf_res_plotly
import pandapower as pp
import plotly.subplots as splt


def plotting(index, net, scaled, file):
    ##adjust load
    if scaled:
        net.load.loc[index, 'scaling'] = 1.2  ##scaled active power of the load
    else:
        net.load.loc[index, 'scaling'] = 1  ##scaled active power of the load

    ##run PP
    pp.runpp(net, numba=False)
    if scaled:
        file.write("\n\nScaled Power Flow Results")
        file.write("\n\tLoad " + str(index) + ":\n")
        file.write(str(net.load.loc[index]) + "\n")
        file.write("\n\tResults\n")
        file.write(str(net.res_bus.loc[index]))
    else:
        file.write("Unscaled Power Flow Results")
        file.write("\n\tLoad " + str(index) + ":\n")
        file.write(str(net.load.loc[index]) + "\n")
        file.write("\n\tResults\n")
        file.write(str(net.res_bus.loc[index]))

    fig = pf_res_plotly(net, auto_open=False)
    return fig


def combine_plots(fig1, fig2, net, index):
    fig = splt.make_subplots(rows=1, cols=2)
    fig1.update_layout(title="Load " + str(index) + " Scaled by 20% at Bus " + str(net.load.loc[index, "bus"]))
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

    fig2.update_layout(title="Load " + str(index) + " Baseline at Bus " + str(net.load.loc[index, "bus"]))
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    fig = set_notations(fig, net, index)
    fig.update_layout(showlegend=False)
    fig.show()


def set_notations(fig, net, index):
    x_coords = net.bus_geodata.x
    y_coords = net.bus_geodata.y

    bus = net.load.loc[index, 'bus']  ##Bus with scaled load attached to it
    subplot = ""
    for i in range(1, 3):
        bus_index = 0
        for x, y in zip(x_coords, y_coords):
            if bus_index == bus:
                fig.add_annotation(
                    xref='x' + subplot,
                    yref='y',
                    x=x,
                    y=y,
                    text=str(bus_index),
                    showarrow=False,
                    font=dict(color='red', size=12)
                )
            else:
                fig.add_annotation(
                    xref='x' + subplot,
                    yref='y',
                    x=x,
                    y=y,
                    text=str(bus_index),
                    showarrow=False,
                    font=dict(color='black', size=8)
                )
            bus_index += 1
        subplot = "2"
    return fig

