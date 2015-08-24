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
ptHi=TH2F("jetpt","Jet_pt",n,0,300,50,-5,5)
ptHinp=TH2F("jetpt_np","Jet_pt",n,0,300,50,-5,5)
while zztree.GetEntry(i):
    i+=1
    jetpt=zztree.JetPt
    jeteta=zztree.JetEta
    if len(jetpt)!=len(jeteta):
        print 'ERROR: Puppi length differ!!!'
        continue
    for a in range(len(jetpt)):
        ptHi.Fill(jetpt[a],jeteta[a])
i=0
while zznptree.GetEntry(i):
    i+=1
    jetpt=zznptree.JetPt
    jeteta=zznptree.JetEta
    if len(jetpt)!=len(jeteta):
        print 'ERROR: nonPuppi length differ!!!'
        continue
    for a in range(len(jetpt)):
        ptHinp.Fill(jetpt[a],jeteta[a])
#puHi.GetXaxis().SetRange(0,300)
#puHi.Draw()

#ptHi.Scale(puHi.GetMaximum()/ptHi.GetMaximum())
#puHi.SetLineColor(2)
c.cd(1)
ptHinp.Draw('colz')
ptHinp.SetTitle('nonPuppi Eta vs Pt;Pt/GeV;eta')
c.cd(2)
ptHi.Draw('colz')
ptHi.SetTitle('Puppi Eta vs Pt;Pt/GeV;eta')
c.Print('pteta.png')

