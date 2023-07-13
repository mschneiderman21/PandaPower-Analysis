import simbench as sb

sb_code = "1-MVLV-urban-5.303-0-sw" ##What network to use
net = sb.get_simbench_net(sb_code)

print(net.load)


print(net.load.loc[14, 'bus'])
