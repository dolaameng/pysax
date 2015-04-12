import numpy as np 
import pandas as pd 
from fractions import Fraction 
from functools import partial 
from itertools import cycle
from joblib import Parallel, delayed
import joblib, tempfile, os


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
		self.alphabet = list(alphabet or "ABCD")
		self.nlevels = len(self.alphabet)
		
		if not (3 <= self.nlevels <= 10):
			raise ValueError("alphabet size is within 3 and 10 for current impl.")
		self.cutpoints = {3 : [-np.inf, -0.43, 0.43, np.inf],
                            4 : [-np.inf, -0.67, 0, 0.67, np.inf],
                            5 : [-np.inf, -0.84, -0.25, 0.25, 0.84, np.inf],
                            6 : [-np.inf, -0.97, -0.43, 0, 0.43, 0.97, np.inf],
                            7 : [-np.inf, -1.07, -0.57, -0.18, 0.18, 0.57, 1.07, np.inf],
                            8 : [-np.inf, -1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, np.inf],
                            9 : [-np.inf, -1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, np.inf],
                            10: [-np.inf, -1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28, np.inf],
                            11: [-np.inf, -1.34, -0.91, -0.6, -0.35, -0.11, 0.11, 0.35, 0.6, 0.91, 1.34, np.inf],
                            12: [-np.inf, -1.38, -0.97, -0.67, -0.43, -0.21, 0, 0.21, 0.43, 0.67, 0.97, 1.38, np.inf],
                            13: [-np.inf, -1.43, -1.02, -0.74, -0.5, -0.29, -0.1, 0.1, 0.29, 0.5, 0.74, 1.02, 1.43, np.inf],
                            14: [-np.inf, -1.47, -1.07, -0.79, -0.57, -0.37, -0.18, 0, 0.18, 0.37, 0.57, 0.79, 1.07, 1.47, np.inf],
                            15: [-np.inf, -1.5, -1.11, -0.84, -0.62, -0.43, -0.25, -0.08, 0.08, 0.25, 0.43, 0.62, 0.84, 1.11, 1.5, np.inf],
                            16: [-np.inf, -1.53, -1.15, -0.89, -0.67, -0.49, -0.32, -0.16, 0, 0.16, 0.32, 0.49, 0.67, 0.89, 1.15, 1.53, np.inf],
                            17: [-np.inf, -1.56, -1.19, -0.93, -0.72, -0.54, -0.38, -0.22, -0.07, 0.07, 0.22, 0.38, 0.54, 0.72, 0.93, 1.19, 1.56, np.inf],
                            18: [-np.inf, -1.59, -1.22, -0.97, -0.76, -0.59, -0.43, -0.28, -0.14, 0, 0.14, 0.28, 0.43, 0.59, 0.76, 0.97, 1.22, 1.59, np.inf],
                            19: [-np.inf, -1.62, -1.25, -1, -0.8, -0.63, -0.48, -0.34, -0.2, -0.07, 0.07, 0.2, 0.34, 0.48, 0.63, 0.8, 1, 1.25, 1.62, np.inf],
                            20: [-np.inf, -1.64, -1.28, -1.04, -0.84, -0.67, -0.52, -0.39, -0.25, -0.13, 0, 0.13, 0.25, 0.39, 0.52, 0.67, 0.84, 1.04, 1.28, 1.64, np.inf]
                            }

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

	def symbolize(self, xs):
		"""
		Symbolize a PPA
		"""
		alphabet_sz = len(self.alphabet)
		cutpoints = self.cutpoints[alphabet_sz]
		return pd.cut(xs, bins = cutpoints, labels = self.alphabet)

	def symbolize_window(self, window_signal):
		"""
		Symbolize one sliding window signal to a word
		"""
		s = self.whiten(window_signal)
		binsize = Fraction(len(s), self.nbins)
		xs = map(lambda ss: np.sum(ss) / float(binsize), self.binpack(s))
		return "".join(self.symbolize(xs))

	def symbolize_signal(self, signal, parallel = None, n_jobs = -1):
		"""
		Symbolize whole time-series signal to a sentence (vector of words),
		parallel can be {None, "ipython"}
		"""
		window_index = self.sliding_window_index(len(signal))
		if parallel == None:
			return map(lambda wi: self.symbolize_window(signal[wi]), window_index)
		elif parallel == "ipython":
			## too slow
			raise NotImplementedError("parallel parameter %s not supported" % parallel)
			#return self.iparallel_symbolize_signal(signal)
		elif parallel == "joblib":
			with tempfile.NamedTemporaryFile(delete=False) as f:
				tf = f.name
			print "save temp file at %s" % tf 
			tfiles = joblib.dump(signal, tf)
			xs = joblib.load(tf, "r")
			n_jobs = joblib.cpu_count() if n_jobs == -1 else n_jobs 
			window_index = list(window_index)
			batch_size = len(window_index) / n_jobs
			batches = chunk(window_index, batch_size)
			symbols = Parallel(n_jobs)(delayed(joblib_symbolize_window)(self, xs, batch) for batch in batches)
			for f in tfiles: os.unlink(f)
			return sum(symbols, [])
		else:
			raise NotImplementedError("parallel parameter %s not supported" % parallel)

def joblib_symbolize_window(sax, xs, batch):
	return [sax.symbolize_window(xs[i]) for i in batch]
def chunk(xs, chunk_size):
	p = 0
	while p < len(xs):
		yield xs[p:(p+chunk_size)]
		p += chunk_size

# 	def iparallel_symbolize_signal(self, signal):
# 		try:
# 			from IPython.parallel import Client
# 			import joblib, tempfile, os
# 			client = Client()
# 			dv = client[:]
# 			lb_view = client.load_balanced_view()
# 			print "running on %i cores" % len(lb_view)
# 		except IOError, err:
# 			print "please start ipcluster to enable ipython.parallel:",
# 			print " ipcluster start -n [num_cores]"
		
# 		with tempfile.NamedTemporaryFile(delete=False) as f:
# 			tf = f.name
# 			print "save temp file at %s" % tf 
# 		joblib.dump(signal, tf)
# 		#dv.push({"sax_signal_file": tf, "sax_self": self}, block = True)
# 		#return lb_view.map_sync(lambda x: sax_signal_file, range(5))
# 		window_index = self.sliding_window_index(len(signal))
# 		#print zip(window_index, cycle([self]), cycle([tf]))
# 		symbols = lb_view.map_sync(parallel_symbolization, 
# 									zip(window_index, cycle([self]), cycle([tf])))

# 		os.unlink(tf)
# 		return symbols

# def parallel_symbolization(args):
# 	"""
# 	assume global access to sax_signal_file, sax_self
# 	"""
# 	indices, sax_self, sax_signal_file = args
# 	import joblib
# 	signal = joblib.load(sax_signal_file, "r")
# 	s = signal[indices]
# 	return sax_self.symbolize_window(s)