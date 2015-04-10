import numpy as np 

class SAXModel(object):
	def __init__(self, window = None, stride = None, 
				nbins = None, alphabet = None):
		"""
		Assume a gapless (fixed freq. no missing value) time series
		window: sliding window length to define the number of words
		stride: stride of sliding, if stride < window, there is overlapping in windows
		nbins: number of bins in each sliding window, defining the length of word 
		alphabet: number of discretization  
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

	def bin(self, window_signal):
		##TODO
		pass

