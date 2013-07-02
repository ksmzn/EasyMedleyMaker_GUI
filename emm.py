#! /usr/bin/env python
#-*- encoding:utf-8 -*-

import wx
from wx import xrc
from create_movie import Make_file as mf

XRC_FILE = "noname.xrc"

class EMMApp(wx.App):
    def OnInit(self):
        self.res = xrc.XmlResource(XRC_FILE)
        self.init_frame()
        return True

    def init_frame(self):
        self.frm_main = self.res.LoadFrame(None,'mainFrame')
        #self.file01 = xrc.XRCCTRL(self.frm_main, 'file01')
        files = ["file%02d" % i for i in xrange(1,11)]
        self.output_dir = xrc.XRCCTRL(self.frm_main, "output_dir")
        self.files = [xrc.XRCCTRL(self.frm_main, i) for i in files]
        self.btn_submit = xrc.XRCCTRL(self.frm_main, "run_btn")
        self.btn_submit.Bind(wx.EVT_BUTTON, self.MakeMovie)
        self.frm_main.SetTitle("EasyMedleyMaker")
        self.frm_main.SetSize((500, 700))
        self.frm_main.Show()

    def MakeMovie( self, event ):
        #print [i.GetPath() for i in self.files if i.GetPath()]
        self.output_dir = self.output_dir.GetPath()
        #self.frm_main.SetTitle(self.output_dir)
        self.names = [i.GetPath() for i in self.files if i.GetPath()]
        self.movie = mf(self.names, self.output_dir)
        self.movie.get_music_info()
        self.movie.make_jpg()
        self.movie.convert2mpg()
        self.movie.create_mpg()
        self.movie.mpg2mp4()

if __name__ == "__main__":
    app =EMMApp(False)
    app.MainLoop()
