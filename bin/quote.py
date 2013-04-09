#!/usr/bin/env python
import urllib
import urllib2
import json
import argparse
import re
import csv
import StringIO
import tempfile
import os
import os.path
import stat
import glob

class Quote:
    """Retrives stock quote from Yahoo! finance service"""
    FIELDS = (
        { 'id': 's', 'name': 'symbol' },
        { 'id': 'l1', 'name': 'last trade' },
        { 'id': 'p2', 'name': 'change percent' },
        { 'id': 'c1', 'name': 'change' }
    )

    URL = 'http://download.finance.yahoo.com/d/quotes.csv';
    TEMP_DIR = '/tmp'

    def __init__( self, symbol ):
        self.symbol = symbol
        f = ''
        for field in self.FIELDS:
            f += field['id']
            
        self.query_fields = {
            's': symbol,
            'f': f
        }
        
        query_string = urllib.urlencode( self.query_fields )
        self.uri = self.URL + '?' + query_string


    def format( self, format ):

        fmt = format
        map = []
        for index in range(0, len(self.FIELDS)):

            pattern = re.compile( "#({id})".format( id = self.FIELDS[index]['id'] ) )
            iterator = pattern.finditer( format )
            for match in iterator:
                #map.append( match.start() ) = index
                pattern.sub( '%s', format )

            print
            
        
    def get_quote( self ):

        
        prefix = "{script}-{user}-{symbol}".format(
            script = os.path.basename( __file__ ),
            user = os.getlogin(),
            symbol = self.symbol.lower()
        )

        files = glob.glob( "{dir}/{prefix}-*".format( dir = self.TEMP_DIR, prefix = prefix ) )

        cache = {}
        for file in files:
            if os.access( file, os.W_OK ):
                cache[ 'file' ] = file
                cache[ 'mtime' ] = os.stat( file ).st_mtime
                break

        if len( cache ) == 0:
            temp = tempfile.NamedTemporaryFile(
                delete = False,
                prefix = "{prefix}-".format( prefix = prefix ),
                dir = self.TEMP_DIR
            )
            cache[ 'file' ] = temp.name
            cache[ 'mtime' ] = 0

        
        response = urllib2.urlopen( self.uri )
        content = StringIO.StringIO( response.read() )
        data = csv.reader( content, delimiter=',' ).next()



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Script to fetch stock quotes'
    )

    parser.add_argument(
        '-s', '--symbol',
        help='ticker symbol',
        type=str,
        default='YHOO'
    )

    parser.add_argument(
        '-f', '--format',
        help='output format',
        type=str,
        default='"#s:#l1 #c1'
    )
    
    args = parser.parse_args()
    quote = Quote( args.symbol )
    quote.get_quote()

