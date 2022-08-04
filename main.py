import os
import datetime
from tkinter import Tk, Canvas, Frame, BOTH
from array import array
#import pygame


def tohex(ciferka):
    vozvrat = "#"
    for x in range(len(ciferka)):
        dobavka = str(hex(ciferka[x])[2:])
        if len(dobavka) < 2:
            dobavka = "0" + dobavka
        vozvrat += dobavka
    return vozvrat


def nextline(someaddr):
    if someaddr & 0x700 != 0x700:
        someaddr += 0x100
    elif someaddr & 0xe0 == 0xe0:
        someaddr += 0x20
    else:
        someaddr -= 0x6e0
    return someaddr


class ZXScreen(object):
    def __init__(self, palette):
        if palette == "pulsar":
            self.palette = [[0x00, 0x00, 0x00], [0x00, 0x00, 0xcd],
                            [0xcd, 0x00, 0x00], [0xcd, 0x00, 0xcd],
                            [0x00, 0xcd, 0x00], [0x00, 0xcd, 0xcd],
                            [0xcd, 0xcd, 0x00], [0xcd, 0xcd, 0xcd],
                            [0x00, 0x00, 0x00], [0x00, 0x00, 0xff],
                            [0xff, 0x00, 0x00], [0xff, 0x00, 0xff],
                            [0x00, 0xff, 0x00], [0x00, 0xff, 0xff],
                            [0xff, 0xff, 0x00], [0xff, 0xff, 0xff]]
        elif palette == "ortodox":
            self.palette = [[0x00, 0x00, 0x00], [0x00, 0x00, 0xcd],
                            [0xa7, 0x00, 0x00], [0xa7, 0x00, 0xcd],
                            [0x00, 0xb7, 0x00], [0x00, 0xb7, 0xcd],
                            [0xa7, 0xb7, 0x00], [0xa7, 0xb7, 0xcd],
                            [0x00, 0x00, 0x00], [0x00, 0x00, 0xff],
                            [0xd0, 0x00, 0x00], [0xd0, 0x00, 0xff],
                            [0x00, 0xe4, 0x00], [0x00, 0xe4, 0xff],
                            [0xd0, 0xe4, 0x00], [0xd0, 0xe4, 0xff]]
        elif palette == "alonecoder":
            self.palette = [[0x00, 0x00, 0x00], [0x00, 0x00, 0xa0],
                            [0xa0, 0x00, 0x00], [0xa0, 0x00, 0xa0],
                            [0x00, 0xa0, 0x00], [0x00, 0xa0, 0xa0],
                            [0xa0, 0xa0, 0x00], [0xa0, 0xa0, 0xa0],
                            [0x00, 0x00, 0x00], [0x00, 0x00, 0xff],
                            [0xff, 0x00, 0x00], [0xff, 0x00, 0xff],
                            [0x00, 0xff, 0x00], [0x00, 0xff, 0xff],
                            [0xff, 0xff, 0x00], [0xff, 0xff, 0xff]]
        else:  #rescale
            self.palette = [[0x3e, 0x41, 0x4c], [0x4e, 0x51, 0x5f],
                            [0x5e, 0x62, 0x73], [0x6e, 0x73, 0x86],
                            [0x7e, 0x83, 0x9a], [0x8e, 0x94, 0xad],
                            [0x9e, 0xa4, 0xc1], [0xae, 0xb5, 0xd4],
                            [0x3e, 0x41, 0x4c], [0x52, 0x55, 0x64],
                            [0x66, 0x6a, 0x7c], [0x7a, 0x7f, 0x94],
                            [0x8e, 0x93, 0xad], [0xa2, 0xa8, 0xc5],
                            [0xb5, 0xbc, 0xdd], [0xc9, 0xd1, 0xf5]]


class Example(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("GraCon")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)

        a = binary2array("kish.scr")
        print("GraCon ver.20220804 by rasmer/q-bone team. http://q-bone.ru\n")
        print(str(datetime.datetime.now()), "The lenght of file is -", len(a),
              "bytes")
        if len(a) == 6912:
            typeofscreen = "Colored standart ZX screen"
        elif len(a) == 6144:
            typeofscreen = "Black and white standart ZX screen"
        elif len(a) == 13824:
            typeofscreen = "Colored gigascreen"
        else:
            typeofscreen = "unknown type"
        print(str(datetime.datetime.now()), "I think type of screen is",
              typeofscreen)

        # Генерируем таблицу смещений
        print(str(datetime.datetime.now()), "Generate offset table...")
        addroffsetarray = []
        currentaddr = 0
        for y in range(192):
            line = []
            for x in range(32):
                line.append(currentaddr + x)
            addroffsetarray.append(line)
            currentaddr = nextline(currentaddr)


# Генерируем таблицу
#    print(str(datetime.datetime.now()),"Generate screen table...")
#    attrayarray = []
#    for bit in range (128):
#      x = bit
#      stroka = []
#      for i in range (8):
#        if x & 128:
#          stroka.append("1")
#        else:
#          stroka.append("0")
#        x = x << 1
#      print(stroka)

# Рисуем картинку
        z = ZXScreen("pulsar")

        print(str(datetime.datetime.now()), "Lets draw something...")
        for y in range(192):
            for x in range(32):
                onebyte = a[addroffsetarray[y][x]]
                atribut = a[6144 + x + y // 8 * 32]
                bgcolor = z.palette[((atribut >> 3) & 8) | (atribut & 7)]
                fgcolor = z.palette[((atribut >> 3) & 0x0f)]

                for i in range(8):
                    cvet = tohex(bgcolor) if onebyte & 128 else tohex(fgcolor)
                    canvas.create_rectangle(x * 8 + i,
                                            y,
                                            x * 8 + i,
                                            y,
                                            outline=cvet)
                    onebyte = onebyte << 1

        print(str(datetime.datetime.now()), "Painting is over")
        canvas.pack()


def binary2array(nameoffile):
    data = array('B')
    with open(nameoffile, 'rb') as f:
        data.fromfile(f, os.stat(nameoffile).st_size)
    return data


def main():
    root = Tk()
    root.geometry("256x192")
    ex = Example()
    root.mainloop()


if __name__ == '__main__':
    main()
