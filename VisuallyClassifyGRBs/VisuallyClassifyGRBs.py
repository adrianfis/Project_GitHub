import matplotlib as mpl
import matplotlib.pyplot as plt
import Image
import glob

#remove all of matplotlib's key bindings
for param in mpl.rcParams:
  if 'keymap' in param:
    for i in mpl.rcParams[param]:
      mpl.rcParams[param].remove(i)
#mpl.rcParams['keymap.fullscreen'].remove('f')

fig, ax = plt.subplots(figsize=(850.0/80,680.0/80),dpi=80)
Images = sorted(glob.glob('AllGifsByTrigger/*gif'))
CurrentImage = 0
NumberOfImages = len(Images)
#States = ['Main','FREDs','Goto'] 
State = 'Main'

Tooltexts = {
'Main':u'Keys:[\u2190]Prev [\u2192]:Next\t [F]RED\t [O]dd\t [W]aveform-like\t [B]ulky\t [T]rash\t[G]oto\t[Q]uit',
'FREDs':'Which type of FRED: [C]lean\t [N]oisy\t [M]ultipeak\t[S]uperhigh',
'Goto':'[F]irst\t[L]ast\t[C]ontinue where last classified'
}

def ReadClassificationDatabase():
  global Classification
  try:
    DBfile = open('Classification.db','r')
    DBlines = DBfile.readlines()
    DBfile.close()
    if len(DBlines) != NumberOfImages:
      raise ValueError('DBfile is not equal to number of images')
    Classification = []
    for line in DBlines:
      Classification.append(line[:-1]) 
  except IOError: #Create if nonexistent
    DBfile = open('Classification.db','w')
    DBfile.write('Unclassified\n'*NumberOfImages)
    DBfile.close()
    Classification = ['Unclassified' for x in range(NumberOfImages)]

def WriteClassificationDatabase(event='whatever'):
  DBfile = open('Classification.db','w')
  DBfile.write('\n'.join(Classification))
  DBfile.close()

def press(event):
  global CurrentImage, State, Classification
  if State == 'Main':
    if event.key == 'right' and CurrentImage < NumberOfImages:
      CurrentImage +=1
      loadnewimage(Images[CurrentImage])
    if event.key == 'left' and CurrentImage > 0:
      CurrentImage -=1
      loadnewimage(Images[CurrentImage])
    if event.key == 'f' and CurrentImage:
      State='FREDs'
      fig.canvas.toolbar.set_message(Tooltexts[State])
    if event.key == 'g' and CurrentImage:
      State='Goto'
      fig.canvas.toolbar.set_message(Tooltexts[State])
    if event.key == 'o':
      Classification[CurrentImage] = 'Odd'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
    if event.key == 'w':
      Classification[CurrentImage] = 'Waveform-like'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
    if event.key == 'b':
      Classification[CurrentImage] = 'Bulky'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
    if event.key == 't':
      Classification[CurrentImage] = 'Trash'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
    if event.key == 'q':
      WriteClassificationDatabase()
      plt.close()
#'FREDs':'Which type of FRED: [C]lean\t [N]oisy\t [M]ultipeak\t[S]uperhigh',
  if State == 'FREDs':
    if event.key == 'c':
      Classification[CurrentImage] = 'FRED:Clean'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
      State='Main'
      fig.canvas.toolbar.set_message(Tooltexts[State])
    if event.key == 'n':
      Classification[CurrentImage] = 'FRED:Noisy'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
      State='Main'
      fig.canvas.toolbar.set_message(Tooltexts[State])
    if event.key == 'm':
      Classification[CurrentImage] = 'FRED:Multipeak'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
      State='Main'
      fig.canvas.toolbar.set_message(Tooltexts[State])
    if event.key == 's':
      Classification[CurrentImage] = 'FRED:Superhigh'
      fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],Images[CurrentImage]))
      State='Main'
      fig.canvas.toolbar.set_message(Tooltexts[State])
#'Goto':'[F]irst\t[L]ast\t[C]ontinue where last classified'
  if State == 'Goto':
    if event.key == 'f':
      CurrentImage =0
      loadnewimage(Images[CurrentImage])
      State='Main'
      fig.canvas.toolbar.set_message(Tooltexts[State])
    if event.key == 'l':
      CurrentImage =NumberOfImages
      loadnewimage(Images[CurrentImage])
      State='Main'
      fig.canvas.toolbar.set_message(Tooltexts[State])
    if event.key == 'c':
      for i in range(len(Classification)):
        if Classification[i] =='Unclassified': break
      CurrentImage =i
      loadnewimage(Images[CurrentImage])
      State='Main'
      fig.canvas.toolbar.set_message(Tooltexts[State])

def loadnewimage(imagefile):
  global Classification
  ax.cla()
  img = Image.open(imagefile).convert('RGB')
  ax.imshow(img)
  fig.canvas.set_window_title('{}/{}:[{}]{}'.format(CurrentImage,NumberOfImages,Classification[CurrentImage],imagefile))
  fig.canvas.draw()

ReadClassificationDatabase()
loadnewimage(Images[0])
fig.canvas.mpl_connect('key_press_event',press)
fig.canvas.mpl_connect('close_event',WriteClassificationDatabase)
fig.subplots_adjust(0,0,1,1)
fig.canvas.toolbar.set_message(Tooltexts['Main'])
plt.axis('off')
plt.show()
