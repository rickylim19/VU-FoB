# Fundamentals of Bioinformatics
# Exercise 5
# Get matching sequences using NCBI BLAST

from time import sleep
import re
import urllib2 

def blast(protein_id):
        baseUrl = 'http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Put&QUERY='
        url = baseUrl + protein_id + '&DATABASE=swissprot&PROGRAM=blastp&FILTER=T&EXPECT=100&FORMAT_TYPE=Text'
        fh = urllib2.urlopen(url)
	query = fh.read() 
	fh.close() 
        
        # Find a comment with request id (RID) and estimated time of completion
        # (RTOE). It looks like this:
        # <!--QBlastInfoBegin
        #     RID = 7WS3FMZW01P
        #     RTOE = 11
        # QBlastInfoEnd
        # -->
	m = re.search("^<\!--QBlastInfoBegin\s*RID = (.*)\s*RTOE = (.*)$", query, re.MULTILINE)
	rid = m.groups()[0]
	rtoe = int(m.groups()[1])

        status = ""
        wait_time = rtoe + 1
        while (status != "READY"): 
            print "Waiting for: {0:d} seconds".format(wait_time)
            sleep(wait_time)
            baseurl = 'http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID='
            url = baseurl + rid + '&FORMAT_OBJECT=Alignment&ALIGNMENT_VIEW=Tabular&FORMAT_TYPE=Text&ALIGNMENTS=5'
            fh = urllib2.urlopen(url)
            result = fh.read() 
            fh.close()

            # Find a comment with the request status. It looks like this:
            # <!--
            # QBlastInfoBegin
            #     Status=WAITING
            # QBlastInfoEnd
            # -->
            m = re.search("<\!--\s*QBlastInfoBegin\s*Status=(.*)", result, re.MULTILINE)
            status = m.groups()[0]
            wait_time = 60

        m = re.search("^<PRE>(.*)^</PRE>", result, re.MULTILINE + re.DOTALL)
        return m.groups()[0]

f = open('proteins.txt', 'r') 
for line in f:
    protein_id = line.strip("\n")
    output = protein_id + "_BLASTR.txt" 
    o = open(output, 'w') 
    o.write(blast(protein_id)) 
    o.close() 
