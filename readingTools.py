import os
from ROOT import TFile, TH1
from Process import Process
from Datacard import Datacard
from ProcessCollection import ProcessCollection


#given a root file, return a dictionary of all TH1 objects it contains
#this is used for reading out the histograms in shape files
def buildHistogramDictionary( root_file_path ):
    root_file = TFile( root_file_path )
    histogram_dict = {}
    for entry in root_file.GetListOfKeys():
        name = entry.GetName()
        hist = root_file.Get( name )
        hist.SetDirectory( 0 )
        if isinstance( hist, TH1 ) :
            histogram_dict[ name ] = hist
    return histogram_dict


def processCollectionFromCard( datacard, histogram_dict ):
	process_list = []
	for p in datacard.processNames():
		process_list.append( Process( p, histogram_dict, datacard, 'TChi' in p ) )
	return ProcessCollection( process_list )


#given several datacards, construct the merged ProcessCollection and data
def buildProcessCollectionAndData( datacard_paths ):
	datacards = [ Datacard( path ) for path in datacard_paths ]
	total_process_collection = None
	total_data = None
	for card in datacards:
		histogram_dict = buildHistogramDictionary( card.shapeFilePath() )

		#merge process collections
		proc_col = processCollectionFromCard( card, histogram_dict )
		if total_process_collection is None:
			total_process_collection = proc_col
		else:
			total_process_collection += proc_col

		#merge data
		if total_data is None:
			total_data = histogram_dict[ 'data_obs' ]
		else:
			total_data.Add( histogram_dict[ 'data_obs' ] )
	return total_data, total_process_collection


if __name__ == '__main__':
    pass
