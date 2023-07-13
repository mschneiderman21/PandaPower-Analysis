import simbench as sb
import plotting as plot



##Black Box
sb_code = "1-MVLV-urban-5.303-0-sw" ##What network to use
net = sb.get_simbench_net(sb_code)
load = 14 ##index of what load to be changed
scale = 1.2 ##How much to scale the load
file = f"{sb_code}_load_{load}_scaled_{scale}"
with open('Results/' + file, "w") as file:
    scaled = False
    fig1 = plot.plotting(load, net, scaled, file, scale)
    scaled = True
    fig2 = plot.plotting(load, net, scaled, file, scale)
    plot.combine_plots(fig1, fig2, net, load)
