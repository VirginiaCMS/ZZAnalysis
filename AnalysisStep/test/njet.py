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
c=TCanvas('c','c',400,400)

n=10
nHi=TH1F("jet_p","nJet",n,0,10)
nHinp=TH1F("jet_np","nJet",n,0,10)
while zztree.GetEntry(i):
    i+=1
    jeteta=zztree.JetEta
    n=0
    for a in jeteta:
        if a>etacut or a<-etacut:continue
        n=n+1
    nHi.Fill(n)

i=0
while zznptree.GetEntry(i):
    i+=1
    jeteta=zznptree.JetEta
    n=0
    for a in jeteta:
        if a>etacut or a<-etacut:continue
        n=n+1
    nHinp.Fill(n)
    
#puHi.GetXaxis().SetRange(0,300)
#puHi.Draw()
#ptHi.Scale(puHi.GetMaximum()/ptHi.GetMaximum())
#puHi.SetLineColor(2)
nHinp.SetLineColor(3)
c.cd(1)
nHi.Draw()
nHi.SetTitle('n_jet Distribution;n_jet;events')
nHinp.Draw('same')

leg=TLegend(.55,.85,1,.95)
#leg.AddEntry(puHi,'Puppi Jets')
leg.AddEntry(nHi,'Puppi Jets after ZZAna')
leg.AddEntry(nHinp,'nonPuppi Jets after ZZAna')

leg.Draw('same')
c.Print('njet.png')

