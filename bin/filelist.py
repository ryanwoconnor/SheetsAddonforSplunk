import splunk.Intersplunk 

# get the previous search results
results,unused1,unused2 = splunk.Intersplunk.getOrganizedResults()
# for each results, add a 'shape' attribute, calculated from the raw event text
for result in results:
	result["shape"] = 'test'
	# output results
splunk.Intersplunk.outputResults(results)