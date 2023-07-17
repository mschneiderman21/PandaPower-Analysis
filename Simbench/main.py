import simbench as sb
import plotting as plot
import plotly as plt



sb_code = ["1-MVLV-semiurb-5.220-2-sw"] ## Networks to use
load = 10                            ##    Index of load to be scale
scale = 2                            ##    Amount to scale the p_mw of the load
labels = False                       ##    Show the bus labels
figures = []
for i in range(len(sb_code)):
    net = sb.get_simbench_net(sb_code[i])
    file_name = f"{sb_code[i]}_load_{load}_scaled_{scale}"
    with open('Data/' + file_name, "w") as file:
        scaled = False
        fig1 = plot.plotting(index=load, net=net, scaled=scaled, file=file, scale=scale) ## Plotting function
        scaled = True
        fig2 = plot.plotting(index=load, net=net, scaled=scaled, file=file, scale=scale) ## Plotting function
        fig = plot.combine_plots(fig1=fig1, fig2=fig2, net=net, index=load, scale=scale, labels=labels) ## Combine the two figures
        fig.update_layout(title_text=sb_code[i])

        figures.append(fig)
        plt.offline.plot(fig, filename="Plots/" + file_name + '.html', auto_open=False)

for i in range(len(figures)):
    figures[i].show()