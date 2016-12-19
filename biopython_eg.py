#!bin/usr/python

from Bio import Entrez
import time
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2


Entrez.email = "patricklong010@gmail.com"

search_results = Entrez.read(Entrez.esearch(db="pmc",
                                            term="anxiety",
                                            reldate=365,
                                            usehistory="y"))
count = int(search_results["Count"])
print("Found %i results" % count)

batch_size = 10

out_handle = open("recent_anxiety.xml", "w")


for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Going to download record %i to %i" % (start+1, end))
    attempt = 1
    while attempt <= 3:
        try:
            fetch_handle = Entrez.efetch(db="pmc", retmode="xml",
                                         retstart=start,
                                         retmax=batch_size,
                                         webenv=search_results["WebEnv"],
                                         query_key=search_results["QueryKey"])
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 3" % attempt)
                attempt += 1
                time.sleep(15)
            else:
                raise

    data = fetch_handle.read()
    fetch_handle.close()
    out_handle.write(data)


out_handle.close()
