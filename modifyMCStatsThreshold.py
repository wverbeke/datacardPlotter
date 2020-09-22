import os
import sys


def yieldDatacardPath( datacard_directory ):
    for path, dirs, files in os.walk( datacard_directory ):
        for f in files:
            if f.endswith( '.txt' ) and 'neural' in f:
                yield os.path.join( path, f )



def modifyThreshold( datacard_path, new_threshold ):
    with open( datacard_path ) as f:
        lines = f.readlines()

    with open( datacard_path, 'w' ) as f:
        for l in lines:
            if 'autoMCStats' in l:
                l = '* autoMCStats {}'.format( new_threshold )
            f.write( l )


if __name__ == '__main__':
    datacard_directory = sys.argv[1]
    new_threshold = int( sys.argv[2] )
    for card in yieldDatacardPath( datacard_directory ):
        modifyThreshold( card, new_threshold )
