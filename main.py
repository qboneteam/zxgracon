import os
import datetime
from tkinter import Tk, Canvas, Frame, BOTH
from array import array


class Example(Frame):
  def __init__(self):
    super().__init__()
    self.initUI()
 
  def initUI(self):
    self.master.title("ZX screen")
    self.pack(fill=BOTH, expand=1)


      
    canvas = Canvas(self)
    pulsar = ["#000000" , "#0000cd" , "#cd0000" , "#cd00cd" , "#00cd00" , "#00cdcd" , "#cdcd00" , "#cdcdcd" , "#000000" , "#0000ff" , "#ff0000" , "#ff00ff" , "#00ff00" , "#00ffff" , "#ffff00" , "#ffffff" ]
    a = binary2array("kish.scr")
    print(str(datetime.datetime.now()),"The lenght of file is -" , len(a) , "bytes")
    if len(a) in (6144,6912):
      typeofscreen = "standart ZX screen"
    else:
      typeofscreen = "unknown type"
    print(str(datetime.datetime.now()), "I think type of screen is")
    print(str(datetime.datetime.now()), "Lets Draw...")
    atroffset=0
    scroffset=0
    bgcolor = 0
    fgcolor = 0
    onebyte = 0
    xcoor = 0
    ycoor = 0
    for x in range (32):
     for y in range (24):
        xcoor = x * 8
        ycoor = y * 8
        scroffset = ((y & 0x18) << 8) | ((y & 7) << 5) | (x & 31)
        atroffset = 6144 + x + y*32
        atribut = a[atroffset]
        bgcolor = pulsar[((atribut >> 3) & 8) | (atribut & 7)]
        fgcolor = pulsar[((atribut >> 3) & 8) | ((atribut >> 3) & 7)]

        for i in range (8):
          onebyte = a[scroffset+i*256]
          for j in range (8):
            cvet = bgcolor if onebyte & 128 else fgcolor
            canvas.create_rectangle(xcoor+j, ycoor+i, xcoor+j, ycoor+i, outline=cvet)
            onebyte = onebyte << 1
    print(str(datetime.datetime.now()),"Painting is over")
    canvas.pack()      
  
def binary2array(nameoffile):
  data = array('B')
  with open(nameoffile, 'rb') as f:
    data.fromfile(f, os.stat(nameoffile).st_size)
  return data
  
def main():
  root = Tk()
  ex = Example()
  root.geometry("256x192")
  root.mainloop()

if __name__ == '__main__':
  main()