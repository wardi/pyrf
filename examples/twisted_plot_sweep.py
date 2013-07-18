#!/usr/bin/env python

from pyrf.devices.thinkrf import WSA4000
from pyrf.connectors.twisted_async import TwistedConnector
from pyrf.sweep_device import SweepDevice

import sys
import time
import math

from matplotlib.pyplot import plot, figure, axis, xlabel, ylabel, show
import numpy as np

from twisted.internet import reactor, defer
import twisted.python.log

done = []

def plot_sweep(fstart, fstop, bins):
    # setup my graph
    fig = figure(1)
    xvalues = np.linspace(fstart, fstop, len(bins))

    xlabel("Frequency")
    ylabel("Amplitude")

    # plot something
    plot(xvalues, bins, color='blue')

    # show graph
    show()
    done.append(1)
    if len(done) > 3:
        reactor.callLater(2 ** -4, reactor.stop)

def start_sweep(v):
    global sd
    sd = SweepDevice(dut, plot_sweep)
    sd.capture_power_spectrum(0e9, 10e9, 2000,
        {'gain': 'high', 'antenna': 1}, continuous=True)

# connect to wsa
dut = WSA4000(connector=TwistedConnector(reactor))
d = dut.connect(sys.argv[1])
d.addCallbacks(start_sweep, twisted.python.log.err)
reactor.run()

print 'context_bytes_received', sd.context_bytes_received
print 'data_bytes_received', sd.data_bytes_received
print 'data_bytes_processed', sd.data_bytes_processed
print 'martian_bytes_discarded', sd.martian_bytes_discarded
print 'past_end_bytes_discarded', sd.past_end_bytes_discarded
print 'fft_calculation_seconds', sd.fft_calculation_seconds
print 'bin_collection_seconds', sd.bin_collection_seconds

