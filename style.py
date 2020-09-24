import ROOT
from ROOT import gROOT, TStyle

def setStyle():

    style = TStyle( 'style', 'style' ) 
    
    style.SetCanvasBorderMode(0)
    style.SetCanvasColor(ROOT.kWhite)
    style.SetCanvasDefH(600)
    style.SetCanvasDefW(600)
    style.SetCanvasDefX(0)
    style.SetCanvasDefY(0)
    
    style.SetPadBorderMode(0)
    style.SetPadColor(ROOT.kWhite)
    style.SetPadGridX(False)
    style.SetPadGridY(False)
    style.SetGridColor(0)
    style.SetGridStyle(3)
    style.SetGridWidth(1)
    
    style.SetFrameBorderMode(0)
    style.SetFrameBorderSize(1)
    style.SetFrameFillColor(0)
    style.SetFrameFillStyle(0)
    style.SetFrameLineColor(1)
    style.SetFrameLineStyle(1)
    style.SetFrameLineWidth(1)
    
    style.SetHistLineColor(1)
    style.SetHistLineStyle(0)
    style.SetHistLineWidth(1)
    
    style.SetEndErrorSize(2)
    style.SetMarkerStyle(20)
    
    style.SetOptFile(0)
    style.SetOptStat(0)
    style.SetStatColor(ROOT.kWhite)
    style.SetStatFont(42)
    style.SetLegendFont(63) #43 to have the non-bold font
    style.SetStatFontSize(0.08)
    style.SetStatTextColor(1)
    style.SetStatFormat("6.4g")
    style.SetStatBorderSize(1)
    style.SetStatH(0.7)
    style.SetStatW(0.15)
    
    #Margins
    style.SetPadTopMargin(0.05)
    style.SetPadBottomMargin(0.13)
    style.SetPadLeftMargin(0.16)
    style.SetPadRightMargin(0.04)
    
    # For the Global title
    style.SetOptTitle(0)
    
    #For the axis titles:
    style.SetTitleColor(1, "XYZ")
    style.SetTitleFont(42, "XYZ")
    style.SetTitleSize(0.06, "XYZ")
    style.SetTitleXOffset(0.9)
    style.SetTitleYOffset(1.25)
    
    #For the axis labels:
    style.SetLabelColor(1, "XYZ")
    style.SetLabelFont(42, "XYZ")
    style.SetLabelOffset(0.007, "XYZ")
    style.SetLabelSize(0.05, "XYZ")
    
    #For the axis:
    style.SetAxisColor(1, "XYZ")
    style.SetStripDecimals(ROOT.kTRUE)
    style.SetTickLength(0.03, "XYZ")
    style.SetNdivisions(505, "XYZ")
    style.SetPadTickX(1)
    style.SetPadTickY(1)
    
    style.SetLegendBorderSize(0)
    gROOT.SetStyle('style')

    #important to force the style for histograms made before this style was set
    gROOT.ForceStyle()

    return style
