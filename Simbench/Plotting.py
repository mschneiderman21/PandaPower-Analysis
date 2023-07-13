import pandapower.plotting as plot
import pandapower as pp
import matplotlib.pyplot as plt

def graphing(index, net, scaled, file):

    ##adjust load
    if scaled:
        net.load.loc[index, 'scaling'] = 1.2 ##scaled active power of the load
    else:
        net.load.loc[index, 'scaling'] = 1  ##scaled active power of the load
    ##run PP
    pp.runpp(net, numba=False)
    if scaled:
        file.write("\n\nScaled Power Flow Results")
        file.write("\n\tLoad:\n")
        file.write(str(net.load.loc[index]) + "\n")
        file.write("\n\tResults\n")
        file.write(str(net.res_bus))
    else:
        file.write("Unscaled Power Flow Results")
        file.write("\n\tLoad:\n")
        file.write(str(net.load.loc[index]) + "\n")
        file.write("\n\tResults\n")
        file.write(str(net.res_bus))

    sizes = plot.get_collection_sizes(net)
    collections = list()
    buses = net.bus.index.tolist()
    print(net.res_line)

    ##collection for lines
    cmap_list=[(0, "green"), (50, "yellow"), (65, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)
    collections.append(plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2, use_bus_geodata=True))

    ##collections for buses
    cmap_list=[(0.98, "blue"), (1.0, "green"), (1.02, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)
    collections.append(plot.create_bus_collection(net, net.bus.index, size=sizes["bus"],
                                                  zorder=2, cmap=cmap, norm=norm))
    ##plotting collections
    plot.draw_collections(collections, figsize=(10, 7), set_aspect=True) #plot lines and bus

    ##Trafo Collections
    cmap_list = [(0, "green"), (50, "yellow"), (100, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)
    collections.append(plot.create_trafo_collection(net, net.trafo.index, size=0.15, zorder=1, cmap=cmap, norm=norm))

    plt.subplots_adjust(top=.925, right=.925)
    if scaled:
        ##Title
        plt.title("Load " + str(index) + " Scaled by 20% at Bus " + str(net.load.loc[index, "bus"]))
        plt.savefig('Scaled')
    else:
        plt.title("Load " + str(index) + " Baseline at Bus " + str(net.load.loc[index, "bus"]))
        plt.savefig('Baseline')