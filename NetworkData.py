import pandapower.networks as nw



net = nw.create_cigre_network_mv(with_der="pv_wind")


print(net.line)
print(net.switch)
print(net.load)
print(net.bus_geodata)