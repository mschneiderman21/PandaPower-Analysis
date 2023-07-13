import pandapower.networks as nw
import simbench as sb

sb_code = "1-MVLV-semiurb-3.202-1-no_sw" ##What network to use
net = sb.get_simbench_net(sb_code)

print(net.load.loc[261])
print(net.bus.loc[394])
print(net.bus_geodata.loc[394])