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
n=10
nHi=TH1F("jet_p","nJet",n,0,10)
nHinp=TH1F("jet_np","nJet",n,0,10)
while zztree.GetEntry(i):
    i+=1
    jeteta=zztree.JetEta
    nHi.Fill(len(jeteta))
i=0
while zznptree.GetEntry(i):
    i+=1
    jeteta=zznptree.JetEta
    nHinp.Fill(len(jeteta))
#puHi.GetXaxis().SetRange(0,300)
#puHi.Draw()
#ptHi.Scale(puHi.GetMaximum()/ptHi.GetMaximum())
#puHi.SetLineColor(2)
nHinp.SetLineColor(3)
c.cd(1)
nHi.Draw()
nHi.SetTitle('n_jet Distribution;n_jet;events')
nHinp.Draw('same')

nHi1=nHi.Clone()
nHinp1=nHinp.Clone()
nHi1.Scale(1/nHi1.GetEntries())
nHi1.SetTitle('n_jet Distribution Normalized;n_jet;A.U.')
nHinp1.Scale(1/nHinp1.GetEntries())
c.cd(2)
nHi1.Draw()
nHinp1.Draw('same')

leg=TLegend(.55,.85,1,.95)
#leg.AddEntry(puHi,'Puppi Jets')
leg.AddEntry(nHi,'Puppi Jets after ZZAna')
leg.AddEntry(nHinp,'nonPuppi Jets after ZZAna')
c.cd(1)
leg.Draw('same')
c.cd(2)
leg.Draw('same')
c.Print('njet.png')

