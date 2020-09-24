import ROOT

from style import setStyle
from drawPlot import drawPlot

from readingTools import buildProcessCollectionAndData, buildSignalProcessCollection


if __name__ == '__main__':

    #set plotting style
    setStyle()

    datacard_path_2016 = 'exampleDatacards/2016/datacard_SR_new_TChiWZ_mChi2_600_mChi1_100_2016.txt'
    datacard_path_2017 = datacard_path_2016.replace( '2016', '2017' )
    datacard_path_2018 = datacard_path_2016.replace( '2016', '2018' )

    datacard_paths = [ datacard_path_2016, datacard_path_2017, datacard_path_2018 ]

    total_data, process_collection = buildProcessCollectionAndData( datacard_paths )


    #datacards for additional signals to be plotted 
    #new process collections are made with just signals, which are then added to the process collection above
    for signal_point in ['TChiSlepSnu_x0p5_mChi2_1200_mChi1_300', 'TChiSlepSnu_x0p5_mChi2_400_mChi1_350' ]:
        datacard_path_extra_signal_2016 = 'exampleDatacards/2016/datacard_SR_new_{}_2016.txt'.format( signal_point )
        datacard_path_extra_signal_2017 = datacard_path_extra_signal_2016.replace( '2016', '2017' )
        datacard_path_extra_signal_2018 = datacard_path_extra_signal_2016.replace( '2016', '2018' )

        signal_datacard_paths = [ datacard_path_extra_signal_2016, datacard_path_extra_signal_2017, datacard_path_extra_signal_2018 ]

        signal_process_collection = buildSignalProcessCollection( signal_datacard_paths )
        process_collection.addSignalCollection( signal_process_collection )

    #naming and coloring of backgrounds
    ewkino_colors = { 'Nonprompt' : ROOT.kAzure + 1, 'WZ' : ROOT.kOrange, 'ZZH' : ROOT.kGreen + 1, 'TTX' : ROOT.kViolet - 3, 'Multiboson' : ROOT.kRed + 1, 'Xgamma' : ROOT.kOrange + 7 }
    legend_names = { 'Nonprompt' : 'Nonprompt', 'WZ' : 'WZ', 'ZZH' : 'ZZ/H', 'TTX' : 't#bar{t}/t + X', 'Multiboson' : 'Multiboson', 'Xgamma' : 'X + #gamma' }

    #naming and coloring of signals
    ewkino_signal_name = '#tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0}#rightarrow'
    signal_legend_names = { 'TChiWZ_mChi2_600_mChi1_100' : ewkino_signal_name + 'WZ (600/100)', 'TChiSlepSnu_x0p5_mChi2_1200_mChi1_300' : ewkino_signal_name + 'sleptons (1200/300)', 'TChiSlepSnu_x0p5_mChi2_400_mChi1_350' : ewkino_signal_name + 'sleptons (400/350)' }
    signal_colors = { 'TChiWZ_mChi2_600_mChi1_100' : ROOT.kGreen , 'TChiSlepSnu_x0p5_mChi2_1200_mChi1_300' : ROOT.kBlue, 'TChiSlepSnu_x0p5_mChi2_400_mChi1_350' : ROOT.kBlack }


    drawPlot( total_data, process_collection, 'test_plot', ewkino_colors, legend_names = legend_names, draw_signal = True, signal_legend_names = signal_legend_names, signal_color_dict = signal_colors )
