#!usr/bin/python
import sys, getopt
import ROOT
from ROOT import TFile, TTree, TH1F, TCanvas
from ROOT import gROOT, gPad 
from ROOT import RooRealVar, RooDataHist, RooAddPdf, RooPlot, RooArgList,  RooBernstein, RooCBShape, RooAddPdf, RooFit, RooGenericPdf
from setTDRStyle import setTDRStyle

mass = 0

opts, args = getopt.getopt(sys.argv[1:],'m:',['mass='])

for opt, arg in opts:
  if opt in ('-m','--mass'):
    mass = arg

gROOT.Reset()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')

inf = TFile.Open('root://eoscms//eos/cms/store/cmst3/group/das2014/EXODijetsLE/dijetTree_RS'+str(mass)+'.root')
tr  = inf.Get('dijets/events')
h   = TH1F('h','h',210,800,5000)

x = RooRealVar('mjj','mjj',800,5000)

m = RooRealVar('mean','mean',float(mass),float(mass)-200,float(mass)+200)
s = RooRealVar('sigma','sigma',0.1*float(mass),0,10000)
a = RooRealVar('alpha','alpha',1,-10,10)
n = RooRealVar('n','n',1,0,100)
sig = RooCBShape('sig','sig',x,m,s,a,n)        

p  = RooRealVar('p','p',1,0,5)
x0 = RooRealVar('x0','x0',1000,100,5000)

bkg = RooGenericPdf('bkg','1/(exp(pow(@0/@1,@2))+1)',RooArgList(x,x0,p))

fsig= RooRealVar('fsig','fsig',0.5,0.,1.)
model = RooAddPdf('model','model',sig,bkg,fsig)

can = TCanvas('can_Mjj'+str(mass),'can_Mjj'+str(mass),900,600)
tr.Draw('mjj>>h','jetElf[0]<0.7 && jetElf[1]<0.7 && jetMuf[0]<0.7 && jetMuf[1]<0.7 && jetPt[1]>40 && dEtajj<1.3')
h.Draw()
#gPad.SetLogy() 

roohist = RooDataHist('roohist','roohist',RooArgList(x),h)


model.fitTo(roohist)
frame = x.frame()
roohist.plotOn(frame)
model.plotOn(frame)
model.plotOn(frame,RooFit.Components('bkg'),RooFit.LineColor(ROOT.kRed),RooFit.LineWidth(2),RooFit.LineStyle(ROOT.kDashed))
frame.Draw('same')


#----- keep the GUI alive ------------
if __name__ == '__main__':
  rep = ''
  while not rep in ['q','Q']:
    rep = raw_input('enter "q" to quit: ')
    if 1 < len(rep):
      rep = rep[0]
