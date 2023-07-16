import simbench as sb

sb_code = "1-HV-mixed--2-sw" ##What network to use
net = sb.get_simbench_net(sb_code)

#print(net.load)

print(net.bus_geodata)