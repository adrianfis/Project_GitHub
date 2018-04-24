import glob,re

HTMLTableFile = open('../SwiftGRBTable-FullView-20180116.html','r')
HTMLlines = HTMLTableFile.read().split('<tr>')
HTMLTableFile.close()

HTMLreplace = {'&lt;':'<','&#126;':'~','&amp;':'&','&#34;':'\"','&gt;':'>'}
def replaceHTML(StringToChange):
  for HTMLcode in HTMLreplace.keys():
    StringToChange = StringToChange.replace(HTMLcode,HTMLreplace[HTMLcode])
  return StringToChange

TriggerNumbers = [int(x[21:27]) for x in sorted(glob.glob('AllGifsByTrigger/*gif'))]

ClassificationFile = open('Classification.db','r')
Classifications = [x[:-1] for x in ClassificationFile.readlines()]
ClassificationFile.close()

outputfile = open('GRBvisualClassification.list','w')

for i in range(len(HTMLlines))[2:]:
  if i % 11 != 1:
    columns = HTMLlines[i].split('</td>')
    if len(columns) != 36: print i, len(columns)
    GRB = re.compile('>[0-9]*[A-Z]?[^<]').findall(columns[0])[0][1:]
    TriggerHTML = columns[2].replace('\n<td class="nowrap">','')
    try:
      Trigger = int(TriggerHTML[:6])
    except ValueError: continue
    if Trigger in TriggerNumbers:
      outputfile.write('{},{}\n'.format(GRB,Classifications[TriggerNumbers.index(Trigger)]))

outputfile.close()
