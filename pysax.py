import numpy as np 
from fractions import Fraction 

class SAXModel(object):
	def __init__(self, window = None, stride = None, 
				nbins = None, alphabet = None):
		"""
		Assume a gapless (fixed freq. no missing value) time series
		window: sliding window length to define the number of words
		stride: stride of sliding, if stride < window, there is overlapping in windows
		nbins: number of bins in each sliding window, defining the length of word 
		alphabet: alphabet for symbolization, also determines number of value levels  
		Not all parameters are used if only partial functions of the class is needed
		"""
		self.window = window
		self.stride = stride
		self.nbins = nbins
		self.alphabet = alphabet or "ABCD"
		self.nlevels = len(self.alphabet)
		
		if not (3 <= self.nlevels <= 10):
			raise ValueError("alphabet size is within 3 and 10 for current impl.")

	def sliding_window_index(self, signal_length):
		"""
		Takes length of signal and returns list of indices, each of which 
		defines a sliding window 
		"""
		start = 0
		while (start+self.window) <= signal_length:
			yield slice(start, start+self.window)
			start += self.stride

	def whiten(self, window_signal):
		"""
		Perform whitening - it should be local to a sliding window 
		"""
		s = np.asarray(window_signal)
		mu, sd = np.mean(s), np.std(s)
		return (s - mu) / (sd + 1e-10)

	def binpack(self, xs):
		"""
		for a singal of length 5, nbins = 3, 
		it generates (p1, 2*p2/3), (p2/3, p3, p4/3), (2*p4/3, p5)
		"""
		xs = np.asarray(xs)
		binsize = Fraction(len(xs), self.nbins)
		wts = [1 for _ in xrange(int(binsize))] + [binsize-int(binsize)]
		pos = 0
		while pos < len(xs):
			n = len(wts) - 1 if wts[-1] == 0 else len(wts)
			yield xs[pos:(pos+n)] * wts[:n]
			pos += len(wts) - 1
			rest_wts = binsize-(1-wts[-1])
			wts = [1-wts[-1]] + [1 for _ in xrange(int(rest_wts))] + [rest_wts-int(rest_wts)]

