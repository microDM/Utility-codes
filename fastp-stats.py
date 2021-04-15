import json
import glob
import csv

out = open('stats.csv','w')
csvwriter = csv.writer(out)
csvwriter.writerow(['Sample','Total reads','Q20 rate','Q30 rate','Total reads','Q20 rate','Q30 rate'])

for i in glob.glob('*.json'):
    sample = i.split('.')[0]
    x = open(i,'r').read()
    x = json.loads(x)['summary']
    before_filtering = x['before_filtering']
    after_filtering = x['after_filtering']
    bf_total_reads = before_filtering['total_reads']
    bf_q20 = before_filtering['q20_rate']
    bf_q30 = before_filtering['q30_rate']
    af_total_reads = after_filtering['total_reads']
    af_q20 = after_filtering['q20_rate']
    af_q30 = after_filtering['q30_rate']
    csvwriter.writerow([sample,bf_total_reads,bf_q20,bf_q30,af_total_reads,af_q20,af_q30])


