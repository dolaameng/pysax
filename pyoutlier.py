## time series outlier detection based on grammar-based compression
## implementation based on the paper "Time series anomaly discovery with grammar-based compression"
## by Pavel Senin, Lessica Lin, Xing Wang, Tim Oates, Sunil Gandhi, Arnold P. Boedihardjo, Crystal Chen and Susan Frankenstein
## which can be found at file:///home/chenlin/Downloads/14-05.pdf

import pysax
import pysequitur
from itertools import groupby
import numpy as np

class TSOutlierDetection(object):

	################################ main interface ################################3
	def __init__(self, sax_params, sequitur_params):
		self.sax_params = sax_params
		self.sequitur_params = sequitur_params
		self.sax_model = pysax.SAXModel(**self.sax_params)
		self.sequitur_model = pysequitur.SequiturModel(**self.sequitur_params)

	def fit(self, ts):
		"""build necessary strucuture for a time series for later query
		self.symbols: SAX reprsentation of time series
		reduced_symbols: symbols after numerosity_reduce
		self.reduced_symbols_indices: range(slices) of reduced_symbols in original symbols 
		self.word_occurrences: word occurrences (in rules) from reduced_symbols
		"""
		self.symbols = self.sax_symbolize(ts)
		reduced_symbols, self.reduced_symbols_indices = self.numerosity_reduce(self.symbols)
		self.word_occurrences = self.grammar_induce(reduced_symbols)
		return self

	def timeseries_density(self):
		ts_indices = self.sax_model.convert_index([s.start for s in self.reduced_symbols_indices])
		return ts_indices, self.word_occurrences

	def detect_outliers(self, occurrence_thr = 0):
		if type(occurrence_thr) is float: ## percentile, occurrence_thr [0, 1]
			occurrence_thr = max(np.percentile(self.word_occurrences, occurrence_thr*100), 0)
		tswindow_index, tswindow_occurrence = self.timeseries_density()
		outlier_index = np.where(np.asarray(tswindow_occurrence) <= occurrence_thr)[0]
		return [slice(s, s+self.sax_model.window) for s in np.asarray(tswindow_index)[outlier_index]], np.asarray(tswindow_occurrence)[outlier_index]

	############################ helper function #########################################

	def sax_symbolize(self, ts):
		return self.sax_model.symbolize_signal(ts, parallel="joblib")

	def numerosity_reduce(self, symbols, method = "exact"):
		if method is "exact":
			reduced_symbols = []
			indices = []
			grps = groupby(enumerate(symbols), lambda (k,v): v)
			for (s, grp) in grps:
				grp = list(grp)
				reduced_symbols.append(s)
				indices.append(slice(grp[0][0], grp[-1][0]+1))
		else:
			raise NotImplementedError("method %s for numerosity reduction is not supported yet" % method)
		return (reduced_symbols, indices)

	def grammar_induce(self, reduced_symbols):
		self.sequitur_model.fit(reduced_symbols)
		return self.sequitur_model.tag(reduced_symbols)

	def mine_infrequent_segments(self, word_occurrences, threshold = None):
		threshold = threshold if threshold is not None else min(word_occurrences)
		outliers = np.where(np.asarray(word_occurrences) <= threshold)
		return outliers[0]
