import ROOT

from style import setStyle
from drawPlot import drawPlot

from readingTools import buildProcessCollectionAndData


if __name__ == '__main__':

    #set plotting style
    setStyle()

    datacard_path_2016 = 'exampleDatacards/2016/datacard_SR_new_TChiWZ_mChi2_600_mChi1_100_2016.txt'
    datacard_path_2017 = datacard_path_2016.replace( '2016', '2017' )
    datacard_path_2018 = datacard_path_2016.replace( '2016', '2018' )

    datacard_paths = [ datacard_path_2016, datacard_path_2017, datacard_path_2018 ]

    total_data, process_collection = buildProcessCollectionAndData( datacard_paths )

    ewkino_colors = { 'Nonprompt' : ROOT.kAzure + 1, 'WZ' : ROOT.kOrange, 'ZZH' : ROOT.kGreen + 1, 'TTX' : ROOT.kViolet - 3, 'Multiboson' : ROOT.kRed + 1, 'Xgamma' : ROOT.kOrange + 7 }
    legend_names = { 'Nonprompt' : 'Nonprompt', 'WZ' : 'WZ', 'ZZH' : 'ZZ/H', 'TTX' : 't#bar{t}/t + X', 'Multiboson' : 'Multiboson', 'Xgamma' : 'X + #gamma' }
    drawPlot( total_data, process_collection, 'test_plot', ewkino_colors, legend_names = legend_names )
