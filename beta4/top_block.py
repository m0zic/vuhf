#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Tue Feb 24 20:50:38 2015
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import dvbt
import osmosdr
import time
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=70,
                decimation=64,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "bladerf=0,buffers=128,buflen=32768" )
        self.osmosdr_sink_0.set_sample_rate(10e6)
        self.osmosdr_sink_0.set_center_freq(800e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(19, 0)
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.fft_vxx_0 = fft.fft_vcc(2048, False, (window.rectangular(2048)), True, 10)
        self.dvbt_symbol_inner_interleaver_0 = dvbt.symbol_inner_interleaver(1512, dvbt.T2k, 1)
        self.dvbt_reference_signals_0 = dvbt.reference_signals(gr.sizeof_gr_complex, 1512, 2048, dvbt.QAM16, dvbt.NH, dvbt.C1_2, dvbt.C1_2, dvbt.G1_32, dvbt.T2k, 0, 0)
        self.dvbt_reed_solomon_enc_0 = dvbt.reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, 8)
        self.dvbt_inner_coder_0 = dvbt.inner_coder(1, 1512, dvbt.QAM16, dvbt.NH, dvbt.C1_2)
        self.dvbt_energy_dispersal_0 = dvbt.energy_dispersal(1)
        self.dvbt_dvbt_map_0 = dvbt.dvbt_map(1512, dvbt.QAM16, dvbt.NH, dvbt.T2k, 1)
        self.dvbt_convolutional_interleaver_0 = dvbt.convolutional_interleaver(136, 12, 17)
        self.dvbt_bit_inner_interleaver_0 = dvbt.bit_inner_interleaver(1512, dvbt.QAM16, dvbt.NH, dvbt.T2k)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(2048, 2048+64, 0, "")
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.0022097087, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "test.ts", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.dvbt_energy_dispersal_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.dvbt_bit_inner_interleaver_0, 0), (self.dvbt_symbol_inner_interleaver_0, 0))    
        self.connect((self.dvbt_convolutional_interleaver_0, 0), (self.dvbt_inner_coder_0, 0))    
        self.connect((self.dvbt_dvbt_map_0, 0), (self.dvbt_reference_signals_0, 0))    
        self.connect((self.dvbt_energy_dispersal_0, 0), (self.dvbt_reed_solomon_enc_0, 0))    
        self.connect((self.dvbt_inner_coder_0, 0), (self.dvbt_bit_inner_interleaver_0, 0))    
        self.connect((self.dvbt_reed_solomon_enc_0, 0), (self.dvbt_convolutional_interleaver_0, 0))    
        self.connect((self.dvbt_reference_signals_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.dvbt_symbol_inner_interleaver_0, 0), (self.dvbt_dvbt_map_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
