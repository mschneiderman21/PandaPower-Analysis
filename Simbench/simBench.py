import simbench as sb
import matplotlib.pyplot as plt
from Plotting import graphing


##Black Box
sb_code = "1-MVLV-semiurb-3.202-1-no_sw" ##What network to use
net = sb.get_simbench_net(sb_code)
load = 14 ##index of what load to be changed
file = f"{sb_code}_load_{load}"
with open(file, "w") as file:
    scaled = False
    graphing(load, net, scaled, file)
    scaled = True
    graphing(load, net, scaled, file)
    plt.show()