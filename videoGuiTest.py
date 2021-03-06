import os
import tkFileDialog
from tkinter import Tk,Button,Entry,StringVar,mainloop
from ttk import Combobox

# os.system('ffmpeg')

class VideoGUI():
    def __init__(self):
        self.ENTRY_WITDH = 20
        self.button_width = 6
        self.default_dir = './'
        self.gui()

    def emptyIt(self):
        self.link_contend.set('')
        return 0

    def chooseFile(self):
        self.fname = tkFileDialog.askopenfilename(title=u"Choose File",initialdir=(os.path.expanduser((self.default_dir))))
        self.link_contend.set(self.fname)
        return  self.fname

    def startFFmpeg(self):
        self.result_link_contend.set('convert done!')
        input_path = self.link_contend.get()
        output_type = self.outType.get()
        output_path = input_path.split('.')[0]+'.'+output_type
        if output_type == 'wav':
            cmd =  'ffmpeg -i '+ input_path + ' -y ' +output_path
        elif output_path == 'mp4':
            cmd = 'ffmpeg -i ' + input_path + ' ' + output_path
        else:
            cmd = 'ffmpeg'
        os.system(cmd)
        self.result_link_contend.set(output_path)
        self.link_contend.set('convert done!')
        return 0

    def gui(self):
        self.root = Tk()
        self.root.title('video converter')
        self.entry_link = Entry(self.root,width=self.ENTRY_WITDH,state='disabled')
        self.entry_link.grid(row=0,column=0,columnspan=2)
        self.link_contend = StringVar()
        self.entry_link.config(textvariable=self.link_contend)
        self.link_contend.set('plz choose:')
        self.choose_button = Button(self.root,text='choose',width=self.button_width,command=self.chooseFile)
        self.choose_button.grid(row=1,column=0,columnspan=1)
        self.clear_button = Button(self.root,text='empty',width=self.button_width,command=self.emptyIt)



