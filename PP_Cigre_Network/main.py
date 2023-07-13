import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import numpy as np
import time



def main():
    net = nw.create_cigre_network_mv(with_der=False)

    ## File Generation
    timestamp = int(time.time())
    file = f"Main_{timestamp}.txt"

    with open(file, "w") as file:
        ## Label the switches from bus 0 to each feeder
        net.switch.loc[6, 'name'] = 'F1'
        net.switch.loc[7, 'name'] = 'F2'

        ##Print the buses
        file.write(str(net.bus))

        ##Switch control
        net.switch.loc[0, 'closed'] = True
        net.switch.loc[1, 'closed'] = True ##S2
        net.switch.loc[2, 'closed'] = True ##S3
        net.switch.loc[3, 'closed'] = True
        net.switch.loc[4, 'closed'] = True ##S1
        net.switch.loc[5, 'closed'] = True
        net.switch.loc[6, 'closed'] = True ##F1
        net.switch.loc[7, 'closed'] = True ##F2

        #Bus Control
        net.bus.loc[0, 'vn_kv'] = 110.0  ##rated voltage of the bus
        net.bus.loc[0, 'in_service'] = True  ##In services

        ##Line Control
        net.line.loc[0, 'in_service'] = True  ##In services


        file.write('\n\n Switch - Status\n')
        file.write(str(net.switch))

        file.write('\n\nBus_geodata\n')
        file.write(str(net.bus_geodata))

        ##Run OPP
        pp.runopp(net, numba=False)
        file.write("\n\n Run OPP:")

        ##Write Results to Output File
        file.write('\n\nBus - result\n')
        file.write(str(net.res_bus))

        file.write('\n\nLoads - result\n')
        file.write(str(net.res_load))

        file.write('\n\nTransformer - result\n')
        file.write(str(net.res_trafo))

        file.write('\n\nSwitch - result\n')
        file.write(str(net.res_switch))

        file.write('\n\nLine - result\n')
        file.write(str(net.res_line))
    load = 1 ##what load to be displayed
    scaled = True
    graphing(load, net, scaled)
    scaled = False
    graphing(load, net, scaled)
    plt.show()

def graphing(index, net, scaled):

    ##adjust load
    if scaled:
        net.load.loc[index, 'scaling'] = 1.2 ##scaled active power of the load
    else:
        net.load.loc[index, 'scaling'] = 1  ##scaled active power of the load
    ##run OPP
    pp.runopp(net, numba=False)

    ##collection for lines
    cmap_list=[(0, "green"), (50, "yellow"), (100, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)
    lc = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap, norm=norm, linewidths=2)

    ##collections for buses
    cmap_list=[(0.9, "blue"), (1.0, "green"), (1.1, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)
    bc = plot.create_bus_collection(net, net.bus.index, size=0.25, zorder=2, cmap=cmap, norm=norm)

    ##collection for transformers
    cmap_list=[(0, "green"), (50, "yellow"), (100, "red")]
    cmap, norm = plot.cmap_continuous(cmap_list)
    tc = plot.create_trafo_collection(net, net.trafo.index, size=0.15, zorder= 1, cmap=cmap, norm=norm) ##create transformer

    ##Add labels to buses
    data = net.res_bus.vm_pu.tolist() #bus_voltages
    buses = net.bus.index.tolist() #bus_indicies
    rounded_data = []
    for num in data:
        rounded_data.append(round(num, 3))

    ##coords for bus volatage
    coords = zip(net.bus_geodata.x.loc[[0, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14]].values + 0.2,
                 net.bus_geodata.y.loc[[0, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14]].values + 0.2) # tuples of all bus coords
    bv1 = plot.create_annotation_collection(size=0.45, texts=np.char.mod('%s', [rounded_data[0], rounded_data[2],
                                                                                rounded_data[3], rounded_data[6],
                                                                                rounded_data[7], rounded_data[8],
                                                                                rounded_data[9], rounded_data[10],
                                                                                rounded_data[11], rounded_data[12],
                                                                                rounded_data[13], rounded_data[14]]),
                                            coords=coords, zorder=3, color="black")

    ##Bus 4 and 5
    coords = zip(net.bus_geodata.x.loc[[4, 5]].values + 0.45, net.bus_geodata.y.loc[[4, 5]].values + 0.05)  # tuples of all bus coords
    bv2 = plot.create_annotation_collection(size=0.45, texts=np.char.mod('%s', [rounded_data[4], rounded_data[5]]),
                                            coords=coords, zorder=3, color="black")

    ##Bus 1
    coords = zip(net.bus_geodata.x.loc[[1]].values + 0.45, net.bus_geodata.y.loc[[1]].values - 0.5)  # tuples of all bus coords
    bv3 = plot.create_annotation_collection(size=0.45, texts=np.char.mod('%s', [rounded_data[1]]),
                                            coords=coords, zorder=3, color="black")
    ##coords for bus index
    #Bus 1-2, 5-10, 14
    coords = zip(net.bus_geodata.x.loc[[1, 2, 5, 6, 7, 8, 9, 10, 14]].values - 1.5,
                 net.bus_geodata.y.loc[[1, 2, 5, 6, 7, 8, 9, 10, 14]].values - 0.8)  # tuples of all bus coords
    bic1 = plot.create_annotation_collection(size=0.45, texts=np.char.mod('Bus %d', [1, 2, 5, 6, 7, 8, 9, 10, 14]), coords=coords, zorder=3, color="grey")

    ##Bus 11 - 13
    coords = zip(net.bus_geodata.x.loc[[11, 12, 13]].values - 1.75,
                 net.bus_geodata.y.loc[[11, 12, 13]].values - 0.8)  # tuples of all bus coords
    bic2 = plot.create_annotation_collection(size=0.45, texts=np.char.mod('Bus %d', [11, 12, 13]),
                                             coords=coords, zorder=3,  color="grey")

    ##Bus 3 and 4
    coords = zip(net.bus_geodata.x.loc[[3, 4]].values - 1.75, net.bus_geodata.y.loc[[3, 4]].values)  # tuples of all bus coords
    bic3 = plot.create_annotation_collection(size=0.45, texts=np.char.mod('Bus %d', [3, 4]),
                                             coords=coords, zorder=3, color="grey")

    #Bus 0
    coords = zip(net.bus_geodata.x.loc[[0]].values - 0.8,
                 net.bus_geodata.y.loc[[0]].values - 0.8)  # tuples of all bus coords
    bic4 = plot.create_annotation_collection(size=0.45, texts=np.char.mod('Bus %d', [0]),
                                             coords=coords, zorder=3, color="grey")

    ##Cirlce around BUS with Load
    coords = zip(net.bus_geodata.x.loc[[net.load.loc[index, "bus"]]].values - 0.485,
                 net.bus_geodata.y.loc[[net.load.loc[index, "bus"]]].values - 0.45)  # tuples of all bus coords
    cc = plot.create_annotation_collection(size = 1.25, texts="O",
                                             coords=coords, zorder=1, color="red")

    ##plotting collections
    plot.draw_collections([lc, bc, bv1, bv2, bv3, bic1, bic2, bic3, bic4, tc, cc], figsize=(8, 7)) #plot lines and buses

    ##Adjust zoom
    plt.subplots_adjust(top=.925, right=.925)
    if scaled:
        ##Title
        plt.title("Load " + str(index) + " Scaled by 20% at Bus " + str(net.load.loc[index, "bus"]))
        plt.savefig('Scaled')
    else:
        plt.title("Load " + str(index) + " Baseline at Bus " + str(net.load.loc[index, "bus"]))
        plt.savefig('Baseline')

if __name__ == "__main__":
    main()