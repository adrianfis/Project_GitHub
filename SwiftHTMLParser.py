#!/usr/bin/env python
import re
import astropy.time as time

inputfile = open('SwiftGRBTable-FullView-20180116.html','r')
inputlines = inputfile.read().split('<tr>')
inputfile.close()

headersHTML = inputlines[1].split('</th>')
headers = [re.compile('>.*').findall(re.compile('width.*').findall(x)[0])[0][1:] for x in headersHTML[:-1]] # hehe

#headers = ['GRB',
# 'Time<br>[UT]',
# 'Trigger<br>Number',
# 'BAT RA<br>(J2000)',
# 'BAT Dec<br>(J2000)',
# 'BAT 90%<br>Error Radius<br>[arcmin]',
# 'BAT T90<br>[sec]',
# 'BAT Fluence<br>(15-150 keV)<br>[10<sup>-7</sup> erg/cm<sup>2</sup>]',
# 'BAT Fluence<br>90% Error<br>(15-150 keV)<br>[10<sup>-7</sup> erg/cm<sup>2</sup>]',
# 'BAT 1-sec Peak<br>Photon Flux<br>(15-150 keV)<br>[ph/cm<sup>2</sup>/sec]',
# 'BAT 1-sec Peak<br>Photon Flux<br>90% Error<br>(15-150 keV)<br>[ph/cm<sup>2</sup>/sec]',
# 'BAT Photon Index<br>(15-150 keV)<br>(PL = simple power-law,<br>CPL = cutoff power-law)',
# 'BAT Photon Index<br>90% Error<br>(15-150 keV)',
# 'XRT RA<br>(J2000)',
# 'XRT Dec<br>(J2000)',
# 'XRT 90%<br>Error Radius<br>[arcsec]',
# 'XRT Time to First<br>Observation<br>[sec]',
# 'XRT Early Flux<br>(0.3-10 keV)<br>[10<sup>-11</sup> erg/cm<sup>2</sup>/s]',
# 'XRT 11 Hour Flux<br>(0.3-10 keV)<br>[10<sup>-11</sup> erg/cm<sup>2</sup>/s]',
# 'XRT 24 Hour Flux<br>(0.3-10 keV)<br>[10<sup>-11</sup> erg/cm<sup>2</sup>/s]',
# 'XRT Initial<br>Temporal<br>Index',
# 'XRT<br>Spectral Index<br>(Gamma)',
# 'XRT Column Density<br>(NH)<br>[10<sup>21</sup> cm<sup>-2</sup>]',
# 'UVOT RA<br>(J2000)',
# 'UVOT Dec<br>(J2000)',
# 'UVOT 90%<br>Error Radius<br>[arcsec]',
# 'UVOT Time to<br>First Observation<br>[sec]',
# 'UVOT Magnitude',
# 'UVOT Other Filter<br>Magnitudes',
# 'Other Observatory Detections',
# 'Redshift',
# 'Host Galaxy',
# 'Comments',
# 'References',
# 'Burst Advocate']

#Note every 11th row is a header row otherwise all rows have 11 </td> elements
badrefs = 0

outfile = open('GRBtable.tsv','w')
outfile.write('#GRB\tTrigger Julian Date\tT90\tRedshift\tRedshift reference\n')
HTMLreplace = {'&lt;':'<','&#126;':'~','&amp;':'&','&#34;':'\"','&gt;':'>'}
def replaceHTML(StringToChange):
  for HTMLcode in HTMLreplace.keys():
    StringToChange = StringToChange.replace(HTMLcode,HTMLreplace[HTMLcode])
  return StringToChange

for i in range(len(inputlines))[1:]:
  if i % 11 != 1:
    columns = inputlines[i].split('</td>')
    if len(columns) != 36: print i, len(columns)
    GRB = re.compile('>[0-9]*[A-Z]?[^<]').findall(columns[0])[0][1:]
    try: T90 = float(columns[6].split('>')[1])
    except ValueError: continue
    Year = 2000 + int(GRB[:2])
    Month = GRB[2:4]
    Day = GRB[4:6]
    Time = columns[1].split('>')[1]
    FITSformatTime = '{}-{}-{}T{}'.format(Year,Month,Day,Time)
    try: JD = time.Time(FITSformatTime,format='fits').jd
    except ValueError: continue
    Redshift = re.compile('>.*').findall(columns[30])[0][1:]
    if Redshift == '&nbsp;': 
      Redshift = '--'
      RedshiftRef = '--'
    else:
      try: RedshiftRef = re.compile('Redshift:</strong>.*[^<br>]').findall(columns[-3])[0][18:]
      except IndexError: 
        RedshiftRef = '#Problem parsing ref#'
        badrefs += 1
#        print columns[-3]
#      print '{}\t{}\t{}'.format(GRB,Redshift,RedshiftRef) 
    outfile.write(replaceHTML('{}\t{}\t{}\t{}\t{}\n'.format(GRB,JD,T90,Redshift,RedshiftRef)))

print 'bad refs = ',badrefs # just 2 bad refs, one for UVOT estimate of z and another for a VLT radio GCN
