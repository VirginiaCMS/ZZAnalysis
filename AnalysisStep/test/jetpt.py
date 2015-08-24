from ROOT import *
from sys import argv
if len(argv)!=3:
    print 'wrong argv'
    exit()
#pufile=TFile('/afs/cern.ch/user/y/yanchu/work/puppi/CMSSW_7_4_7/src/JMEAnalysis/JetToolbox/test/testJTB.root')
#puHi=pufile.Get('hJetsPt')
#n=int(300/puHi.GetXaxis().GetBinWidth(0))
zztree=TChain('ZZTree/candTree')
zznptree=TChain('ZZTree/candTree')

zztree.Add(argv[1])
zznptree.Add(argv[2])
i=0
c=TCanvas('c','c',800,400)
c.Divide(2,1)
n=30
ptHi=TH1F("jetpt","Jet_pt",n,0,300)
ptHinp=TH1F("jetptnp","Jet_pt",n,0,300)
while zztree.GetEntry(i):
    i+=1
    jetpt=zztree.JetPt
    for a in jetpt:
        ptHi.Fill(a)
i=0
while zznptree.GetEntry(i):
    i+=1
    jetpt=zznptree.JetPt
    for a in jetpt:
        ptHinp.Fill(a)
#puHi.GetXaxis().SetRange(0,300)
#puHi.Draw()

#ptHi.Scale(puHi.GetMaximum()/ptHi.GetMaximum())
#puHi.SetLineColor(2)
ptHinp.SetLineColor(3)
c.cd(1)
ptHinp.Draw()
ptHinp.SetTitle('Pt Distribution;Pt/GeV;event')
ptHi.Draw('same')

ptHinp1=ptHinp.Clone()
ptHi1=ptHi.Clone()
ptHinp1.Scale(1/ptHinp1.GetEntries())
ptHi1.Scale(1/ptHi1.GetEntries())
c.cd(2)
ptHinp1.Draw()
ptHinp1.SetTitle('Pt Distribution Normalized;Pt/GeV;A.U.')
ptHi1.Draw('same')
#ptHinp.Draw('same')
leg=TLegend(.55,.85,1,.95)
#leg.AddEntry(puHi,'Puppi Jets')
leg.AddEntry(ptHi,'Puppi Jets after ZZAna')
leg.AddEntry(ptHinp,'nonPuppi Jets after ZZAna')
c.cd(1)
leg.Draw('same')
c.cd(2)
leg.Draw('same')
c.Print('jetpt.png')

