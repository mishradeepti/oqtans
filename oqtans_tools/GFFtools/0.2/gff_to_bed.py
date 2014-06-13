#!/usr/bin/env python
"""
Convert genome annotation data in GFF/GTF to a 12 column BED format. 
BED format typically represents the transcript models. 

Usage: python gff_to_bed.py in.gff > out.bed  

Requirement:
    GFFParser.py: https://github.com/vipints/GFFtools-GX/blob/master/GFFParser.py    

Copyright (C) 
    2009-2012 Friedrich Miescher Laboratory of the Max Planck Society, Tubingen, Germany.
    2012-2014 Memorial Sloan Kettering Cancer Center New York City, USA.
"""

import re
import sys
import GFFParser

def writeBED(tinfo):
    """
    writing result files in bed format 

    @args tinfo: list of genes 
    @args tinfo: numpy object  
    """

    for ent1 in tinfo:
        for idx, tid in enumerate(ent1['transcripts']):
            exon_cnt = len(ent1['exons'][idx])
            exon_len = ''
            exon_cod = '' 
            rel_start = None 
            rel_stop = None 
            for idz, ex_cod in enumerate(ent1['exons'][idx]):#check for exons of corresponding transcript  
                exon_len += '%d,' % (ex_cod[1]-ex_cod[0]+1)
                if idz == 0: #calculate the relative start position 
                    exon_cod += '0,'
                    rel_start = int(ex_cod[0])
                    rel_stop = ex_cod[1]
                else:
                    exon_cod += '%d,' % (ex_cod[0]-rel_start)
                    rel_stop = int(ex_cod[1])
            
            if exon_len:
                score = '0' 
                score = ent1['score'][0] if ent1['score'] else score
                out_print = [ent1['chr'],
                            str(rel_start),
                            str(rel_stop),
                            tid[0],
                            score, 
                            ent1['strand'], 
                            str(rel_start),
                            str(rel_stop),
                            '0',
                            str(exon_cnt),
                            exon_len,
                            exon_cod]
                print '\t'.join(out_print)  
    
def __main__():
    try:
        query_file = sys.argv[1]
    except:
        print __doc__
        sys.exit(-1)

    Transcriptdb = GFFParser.Parse(query_file)  
    writeBED(Transcriptdb)

if __name__ == "__main__": 
    __main__() 
