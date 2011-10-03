# Basic USRP setup and control.
# It's only ever been tried with a basic rx daughter card.
#
# Imagine that the gnuradio boilerplate is here.
#
# M. Revnell 2005-Dec
 
from gnuradio import gr
from gnuradio import uhd

class uhd_input(gr.hier_block2):
    def __init__( self, address, samp_rate):
        gr.hier_block2.__init__(self, "uhd_input",
                                gr.io_signature(0,0,0),
                                gr.io_signature(1,1,gr.sizeof_gr_complex))
        
        self.src = uhd.usrp_source(device_addr=address,
                                   io_type=uhd.io_type.COMPLEX_FLOAT32,
                                   num_channels=1)

        self.src.set_samp_rate(samp_rate)
        self.usrp_rate = self.src.get_samp_rate()

        self.connect(self.src, self)

    def set_freq(self, target_freq):
        """
        Set the center frequency.

        @param target_freq: frequency in Hz
        @type: bool
        """
        r = self.src.set_center_freq(target_freq, 0)

        if r:
            self.freq = target_freq
     	    return True
        else:
            return False

    def get_freq(self):
        return self.src.get_center_freq(0)

    def set_gain(self, gain):
        self.gain = gain
        self.src.set_gain(gain, 0)

    def add_options(parser):        
        parser.add_option("-a", "--address", type="string",
                          default="addr=192.168.10.2",
                          help="Address of UHD device, [default=%default]")
        parser.add_option("-A", "--antenna", type="string", default=None,
                          help="select Rx Antenna where appropriate")
        parser.add_option("-f", "--freq", type="eng_float", default=None,
                          help="set frequency to FREQ", metavar="FREQ")
        parser.add_option("-g", "--gain", type="eng_float", default=None,
                          help="set gain in dB (default is midpoint)")
    add_options = staticmethod(add_options)
