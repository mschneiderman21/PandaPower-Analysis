import simbench as sb
import plotting as plot
import plotly as plt




sb_code = "1-MVLV-urban-5.303-0-sw" ##    Network to use
net = sb.get_simbench_net(sb_code)
load = 14                           ##    Index of load to be scale
scale = 1.2                         ##    Amount to sclae

file_name = f"{sb_code}_load_{load}_scaled_{scale}"
with open('Data/' + file_name, "w") as file:
    scaled = False
    fig1 = plot.plotting(load, net, scaled, file, scale) ## Plotting function
    scaled = True
    fig2 = plot.plotting(load, net, scaled, file, scale) ## Plotting function
    fig = plot.combine_plots(fig1, fig2, net, load) ## Combine the two figures

    plt.offline.plot(fig, filename="Plots/" + file_name +'.html', auto_open=False)
    fig.show()

