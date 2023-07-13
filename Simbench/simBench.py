import simbench as sb
import plotting as plot



##Black Box
sb_code = "1-MVLV-urban-5.303-0-sw" ##What network to use
net = sb.get_simbench_net(sb_code)
load = 14 ##index of what load to be changed
file = f"{sb_code}_load_{load}"
with open(file, "w") as file:
    scaled = False
    fig1 = plot.plotting(load, net, scaled, file)
    scaled = True
    fig2 = plot.plotting(load, net, scaled, file)
    plot.combine_plots(fig1, fig2, net, load)
