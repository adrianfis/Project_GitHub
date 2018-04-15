#!/usr/bin/env python
import urllib
import os.path

#Since the page is apparently automatically generated we can rely on the distances between variables to be always in the same place. 
#So instead of downloading pages in between, let's just generate the download link from the batgrbcat page.
#Example: https://swift.gsfc.nasa.gov/results/batgrbcat/GRB171011A/data_product/00778154000-results/lc/64ms_lc_ascii.dat
# link = https://swift.gsfc.nasa.gov/results/batgrbcat/ $GRB$ /data_product/ $trigger-number-with-8-digits-zeropadded$ 000-result/lc/64_lc_ascii.dat

browser = urllib.urlopen('https://swift.gsfc.nasa.gov/results/batgrbcat/')
lines = browser.readlines()
browser.close()
# Since this process takes a long time I decided to better prepare the list beforehand to have a progress bar
finalurls = []
for i in range(len(lines)):
  if 'data_product' in lines[i]:
    try: trigger = int(lines[i-2].replace(' ','').replace('<td>','').replace('</td>\n',''))
    except ValueError: continue # GRB060123 GRB070125 GRB160623A don't have a trigger number
    GRB = lines[i-3].replace(' ','').replace('<td>','').replace('</td>\n','')
#    lcfileURL = 'https://swift.gsfc.nasa.gov/results/batgrbcat/{}/data_product/{:08d}000-results/lc/64ms_lc_ascii.dat'.format(GRB,trigger)
    lcfileURL = 'https://swift.gsfc.nasa.gov/results/batgrbcat/{}/data_product/{:08d}000-results/lc/sw{:08d}000b_1chan_raw4ms.lc'.format(GRB,trigger,trigger)
    finalurls.append(lcfileURL)

Total = len(finalurls)
for i in range(Total):
  url = finalurls[i]
  GRB = url[url.index('GRB'):url.index('/data_product')] 
#  if os.path.isfile('{}-64ms_lc_ascii.dat'.format(GRB)): print '{} already exists\n'.format(GRB)
  if os.path.isfile('{}-raw4ms-1chan.lc'.format(GRB)): print '{} already exists\n'.format(GRB)
  else:
    urllib.urlretrieve(url,'{}-raw4ms-1chan.lc'.format(GRB))
  print('{}/{} ({:0.2f}%)\r'.format(i,Total,100*float(i)/Total))

#Example:
#trigger: 785510
#URL: https://swift.gsfc.nasa.gov/results/batgrbcat/GRB171102B/data_product/00785510000-results/lc/sw00785510000b_1chan_raw4ms.lc
