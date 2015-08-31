from ROOT import *
from sys import argv
if len(argv)<3:
    print 'wrong argv'
    exit()
if len(argv)<4:
    etacut=4.7
else:
    etacut=float(argv[3])
zztree=TChain('ZZTree/candTree')
zznptree=TChain('ZZTree/candTree')
zztree.Add(argv[1])
zznptree.Add(argv[2])
i=0
c=TCanvas('c','c',800,400)
c.Divide(2,1)
n=50
etaHi=TH1F("jeteta_p","Jet_eta",n,-5,5)
etaHinp=TH1F("jetetanp","Jet_eta",n,-5,5)
while zztree.GetEntry(i):
    i+=1
    jeteta=zztree.JetEta
    for a in jeteta:
        if a>etacut or a<-etacut:continue
        etaHi.Fill(a)
i=0
while zznptree.GetEntry(i):
    i+=1
    jeteta=zznptree.JetEta
    for a in jeteta:
        if a>etacut or a<-etacut:continue
        etaHinp.Fill(a)
#puHi.GetXaxis().SetRange(0,300)
#puHi.Draw()
#ptHi.Scale(puHi.GetMaximum()/ptHi.GetMaximum())
#puHi.SetLineColor(2)
etaHinp.SetLineColor(3)
c.cd(1)
a=etaHinp.GetMaximum()
if a<etaHi.GetMaximum():
    a=etaHi.GetMaximum()
a=a*1.1
etaHinp.Draw()
etaHinp.SetTitle('Eta Distribution;Eta;event')
etaHinp.SetMaximum(a)
etaHi.Draw('same')

etaHinp1=etaHinp.Clone()
etaHi1=etaHi.Clone()
etaHinp1.Scale(1/etaHinp1.GetEntries())
etaHi1.Scale(1/etaHi1.GetEntries())
c.cd(2)
a=etaHinp1.GetMaximum()
if a<etaHi1.GetMaximum():
    a=etaHi1.GetMaximum()
a=a*1.1
etaHinp1.Draw()
etaHinp1.SetTitle('Eta Distribution Normalized;Eta;A.U.')
etaHinp1.SetMaximum(a)
etaHi1.Draw('same')
leg=TLegend(.55,.85,1,.95)
#leg.AddEntry(puHi,'Puppi Jets')
leg.AddEntry(etaHi,'Puppi Jets after ZZAna')
leg.AddEntry(etaHinp,'nonPuppi Jets after ZZAna')
c.cd(1)
leg.Draw('same')
c.cd(2)
leg.Draw('same')
c.Print('jeteta.png')

