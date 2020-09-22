
import os
import math


import ROOT
from ROOT import TCanvas, TPad, TGraphAsymmErrors, TLegend, TLine, TLatex


from drawCMSHeader import drawCMSHeader


def colorHistogram( hist, color ):
	
    #black lines between processes
    hist.SetLineColor( ROOT.kBlack )
    hist.SetLineWidth( 1 )
    
    #set the requested histogram color
    hist.SetFillColor( color )
    hist.SetMarkerColor( color )


def colorProcesses( processCollection, color_dict ):
    for p in processCollection:
        if p.isSignal() : continue
        colorHistogram( p.nominal(), color_dict[ p.name() ] )



def blindedData( data ):
    blinded_data = data.Clone()
    for b in range( 1, blinded_data.GetNbinsX() + 1 ):
        blinded_data.SetBinContent( b, 0 )
        blinded_data.SetBinError( b, 0 )
    return blinded_data
        


def prepareData( data ):

    #set poison errors
    data.SetBinErrorOption( ROOT.TH1.kPoisson )

    #build TGraphAsymmErrors for plotting
    data_graph = TGraphAsymmErrors( data )
    for b in range( 1, data.GetNbinsX() + 1 ):
        bin_content = data.GetBinContent( b )
        data_graph.SetPointError( b - 1, 0, 0,  data.GetBinErrorLow( b ) if bin_content >= 0. else 0., data.GetBinErrorUp( b ) if bin_content >= 0. else 0. )

    #hack for not displaying points at zero 
    maximum = ( data.GetBinContent( data.GetMaximumBin() ) + data.GetBinErrorUp( data.GetMaximumBin() ) )
    for b in range( 1, data.GetNbinsX() + 1 ):
        if data.GetBinContent( b ) < 1e-8:
            data_graph.GetY()[b - 1] += ( maximum * 1e8 )

    return data, data_graph
    

def makeAndDivideCanvas( width, height, lower_pad_fraction ):
    c = TCanvas( "", "", width, height )

    upper_pad = TPad( "", "", 0, lower_pad_fraction, 1, 1 )
    upper_pad.SetBottomMargin( 0.03 )

    lower_pad = TPad( "", "", 0, 0, 1, lower_pad_fraction )
    lower_pad.SetTopMargin( 0.01 )
    lower_pad.SetBottomMargin( 0.4 )

    return c, upper_pad, lower_pad


def makeUpperLegend( data, processCollection, bkg_total, legend_names = None ):

    legend = TLegend(0.25, 0.73, 0.87, 0.92, '', 'brNDC');
    legend.SetNColumns( 2 )
    legend.SetFillStyle( 0 ) #avoid box
    legend.SetBorderSize(0)
    
    legend.AddEntry( data, 'Data', 'pe1' )
    for p in processCollection:
        if p.isSignal(): continue
        name = p.name()
        if legend_names is not None:
            try:
                name = legend_names[ p.name () ]
            except KeyError:
                pass
        legend.AddEntry( p.nominal(), name, 'f' )
    legend.AddEntry( bkg_total, 'Total bkg. unc.', 'f' )
    
    return legend


#compute maximum entry to be drawn on plot
def maximum( data, bkg_total ):
	data_max = ( data.GetBinContent( data.GetMaximumBin() ) + data.GetBinErrorUp( data.GetMaximumBin() ) )
	bkg_max = ( bkg_total.GetBinContent( bkg_total.GetMaximumBin() ) + bkg_total.GetBinErrorUp( bkg_total.GetMaximumBin() ) )
	return max( data_max, bkg_max )


#compute minumum entry to be drawn on plot, but ignore zeroes
def minimum( data, bkg_total ):
	total_min = maximum( data, bkg_total )

	assert ( data.GetNbinsX() == bkg_total.GetNbinsX() )
	for b in range( 1, data.GetNbinsX() + 1 ):
		data_bin = data.GetBinContent( b )
		bkg_bin = bkg_total.GetBinContent( b )
		if data_bin != 0 and data_bin < total_min :
			total_min = data_bin
		if bkg_bin != 0 and bkg_bin < total_min :
			total_min = bkg_bin
	return total_min


#compute range of upper plot 
def rangeLinear( data, background ):
	total_max = maximum( data, background )
	return 0, total_max


def rangeLog( data, background ):
	
	total_min = minimum( data, background )
	total_max = maximum( data, background )
	
	#set minimum to be 5 times smaller than the smallest background yield 
	total_min /= 5
	
	#compute the number of axis divisions ( powers of 10 ) between minimum and maximum
	number_of_orders = math.log10( total_max / total_min )
	
	#the plot maximum should be 50% higher in terms of relative canvas size than total_max 
	total_max = total_max * 10**( 0.5 * number_of_orders )
	return total_min, total_max


def setRelativeUncStyle( relative_unc, color ):
	relative_unc.SetFillStyle( 1001 )
	relative_unc.SetMarkerStyle( 1 )
	relative_unc.SetFillColor( color )


def setRatioPlotStyle( first_hist, lower_pad_fraction ):
    scale_factor = ( 1. - lower_pad_fraction ) / lower_pad_fraction 
    first_hist.GetYaxis().SetTitleOffset( 1.25 / scale_factor )
    first_hist.GetYaxis().SetTitleSize( scale_factor * .06 )
    first_hist.GetXaxis().SetTitleSize( scale_factor * .06 )
    first_hist.GetYaxis().SetLabelSize( scale_factor * .05 )
    first_hist.GetXaxis().SetLabelSize( scale_factor * .05 )
    first_hist.GetXaxis().SetLabelOffset( scale_factor * 0.009 )


#make uncertainty band for ratio plot
def relativeUncBand( bkg_hist ):

    for b in range( 1, bkg_hist.GetNbinsX() + 1 ):
    
        #transform total uncertainties to relative uncertainties
        bin_content = bkg_hist.GetBinContent( b )
        if bin_content > 0:
            bkg_hist.SetBinError( b, bkg_hist.GetBinError( b ) / bin_content )
        else:
            bkg_hist.SetBinError( b, 0. )
        
        #center band at 1
        bkg_hist.SetBinContent( b, 1. )
    
    return bkg_hist


#Make TGraphAsymmErrors representing observed/predicted with statistical uncertainties from data 
def obsOverPredWithDataStat( data_hist, bkg_total ):
    obs_over_pred = TGraphAsymmErrors( data_hist )
    for b in range( 1, data_hist.GetNbinsX() + 1 ):
    
        #divide data by background
        bkg_bin = bkg_total.GetBinContent( b )
        if abs( bkg_bin ) > 1e-8:
            obs_over_pred.GetY()[ b - 1] /= bkg_bin
            obs_over_pred.SetPointError( b - 1, 0., 0., data_hist.GetBinErrorLow( b ) / bkg_bin, data_hist.GetBinErrorUp( b ) / bkg_bin )
        else:
            obs_over_pred.GetY()[ b - 1 ] = 0
            obs_over_pred.SetPointError( b - 1, 0., 0., 0, 0 )
    
    #in case we plot just the expected distribution data will be 0
    #in this case we don't want to plot the data points in the ratio
    if data_hist.GetSumOfWeights() <= 0:
        for b in range( 1, data_hist.GetNbinsX() + 1 ):
            obs_over_pred.GetY()[b - 1 ] += 1e30

    return obs_over_pred
 
	
#draw horizontal line with the same range as the plot
def horizontalLine( data, center ):
    line_begin = data.GetBinLowEdge( 1 )
    line_end = data.GetBinLowEdge( data.GetNbinsX() ) + data.GetBinWidth( data.GetNbinsX() )
    line = TLine( line_begin, center, line_end, center )
    line.SetLineStyle(2);
    return line


#make ratio plot legend
def makeLowerLegend( obs_over_pred, relative_bkg_stat_unc, relative_bkg_total_unc ):
    legend = TLegend( 0.18, 0.85, 0.94, 0.98, '', 'brNDC' )
    legend.SetNColumns( 3 )
    legend.SetFillStyle( 0 )
    legend.SetBorderSize( 0 )
    legend.AddEntry( relative_bkg_stat_unc, 'Stat. pred. unc.', 'f' )
    legend.AddEntry( relative_bkg_total_unc, 'Total pred. unc.', 'f' )
    legend.AddEntry( obs_over_pred, 'Obs./Pred.', 'pe12' )
    return legend



def makeLabel( label_text ):
	
    label = TLatex( 0.65, 0.62, label_text )
    label.SetNDC()
    label.SetTextAlign( 21 )
    label.SetTextFont( 42 )
    label.SetTextColor( ROOT.kBlack )
    label.SetTextSize( 0.04 )
    label.SetTextAngle( 0 )
    return label
	

def drawPlot( data, processCollection, plot_name, color_dict = None, log = True, lower_pad_fraction = 0.25, legend_names = None, lumi_text = '137 fb^{-1} (13 TeV)', width = 1000, height = 600, additional_label = None, expected = False ):

    #order background processes by yield
    processCollection.orderByYield()
    
    #color the histograms
    if color_dict is not None:
        colorProcesses( processCollection, color_dict )

    #blind data for expected plot
    if expected:
        data = blindedData( data )
    
    #Replace data by TGRaphAsymmErrors for plotting
    data, data_graph = prepareData( data )
    
    
    stack = processCollection.backgroundStack()
    bkg_total_syst = processCollection.totalBkgWithAllErrors()
    bkg_total_syst.SetFillStyle( 3244 )
    bkg_total_syst.SetFillColor( ROOT.kGray + 2 )
    bkg_total_syst.SetMarkerStyle( 0 )
    
    
    c, upper_pad, lower_pad = makeAndDivideCanvas( width, height, lower_pad_fraction )
    
    
    #draw data and backgrounds on upper pad
    upper_pad.Draw()
    upper_pad.cd()
    if log:
        upper_pad.SetLogy()
    
    legend = makeUpperLegend( data_graph, processCollection, bkg_total_syst, legend_names )
    
    #determine plot range 
    if log:
        range_min, range_max = rangeLog( data, bkg_total_syst )
    else:
        range_min, range_max = rangeLinear( data, bkg_total_syst )
    bkg_total_syst.SetMinimum( range_min )
    bkg_total_syst.SetMaximum( range_max )
    
    #only draw labels in bottom pad
    bkg_total_syst.GetXaxis().SetLabelSize(0);
    
    bkg_total_syst.Draw( 'e2' )
    stack.Draw( 'histsame' )
    legend.Draw( 'same' )
    
    #redraw total background uncertainty so it overlays the stack
    bkg_total_syst.Draw( 'e2same' )
    data_graph.Draw( 'pe1same' )
    upper_pad.RedrawAxis()
    drawCMSHeader( upper_pad, lumi_text, 'Preliminary' )
    
    upper_pad.RedrawAxis()
    
    if additional_label is not None:
    	label = makeLabel( additional_label )
    	label.Draw( 'same' )
    
    c.cd()
    
    #make ratio plot in lower pad 
    lower_pad.Draw()
    lower_pad.cd()
    
    #make separate histograms containing total and statistical background uncertainty which will be used to plot uncertainty bands
    relative_bkg_stat_unc = relativeUncBand( processCollection.totalBkgWithStatErrors() )
    setRelativeUncStyle( relative_bkg_stat_unc, ROOT.kCyan - 4 )
    relative_bkg_total_unc = relativeUncBand( bkg_total_syst.Clone() )
    setRelativeUncStyle( relative_bkg_total_unc, ROOT.kOrange - 4 )
    
    
    #make TGraphAsymmErrors representing observed/predicted yields with statistical uncertainties from data
    obs_over_pred = obsOverPredWithDataStat( data, bkg_total_syst )
    
    #set name and range of ratio plot 
    relative_bkg_total_unc.GetYaxis().SetRangeUser( 0.,1.999 )
    relative_bkg_total_unc.GetYaxis().SetTitle( 'Obs./Pred.' )
    
    #set label sizes for ratio plot 
    setRatioPlotStyle( relative_bkg_total_unc, lower_pad_fraction )
    
    #make legend for ratio plot
    lower_legend = makeLowerLegend( obs_over_pred, relative_bkg_stat_unc, relative_bkg_total_unc )
    
    relative_bkg_total_unc.Draw( 'e2' )
    relative_bkg_stat_unc.Draw( 'e2same' )
    obs_over_pred.Draw( 'pe01same' )
    lower_legend.Draw( 'same' )
    
    #draw horizontal line at 1 on ratio plot
    line = horizontalLine( data, 1. )
    line.Draw('same')
    
    lower_pad.RedrawAxis();
    
    #remove possible file extension from plot name and print it as pdf and png
    plot_name = os.path.splitext( plot_name )[0]
    c.SaveAs( plot_name + '.pdf' )
    c.SaveAs( plot_name + '.png' )
