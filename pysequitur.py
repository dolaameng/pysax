from subprocess import Popen, PIPE
import numpy as np 
import string
from collections import Counter

class SequiturModel(object):
	def __init__(self, sequitur_path):
		self.sequitur_path = sequitur_path
		self.command = [self.sequitur_path, "-p", "-r", "-k", "2"]
		self.charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&*+,-.:;<=>?@[]"
	
	def fit(self, words):
		"""
		words are expected to be list of strings
		it generates self.rule0 (rule for whole string) and self.rules(from 1 to n)
		"""
		unique_words = list(set(words))
		if len(unique_words) > len(self.charset):
			raise NotImplementedError("the number of unique words %i is too large for mapping" % len(unique_words))
		self.word_length = len(words[0])
		self.words2chars = dict(zip(unique_words, self.charset))
		self.chars2words = dict(zip(self.charset, unique_words))
		mapped_chars = map(self.words2chars.get, words)
		
		raw_rules = Popen(self.command, stdin = PIPE, stdout = PIPE).communicate("".join(mapped_chars))[0].strip()
		## raw rule string from sequitur
		self.raw_rules = "".join([self.chars2words.get(c, c) for c in raw_rules])
		
		rules = [r for r in self.raw_rules.split("\n") if r]
		delim = " -> "
		## first level rule from sequitur
		self.rule0 = rules[0].split(delim)[1]
		## non-root rules from sequitur
		self.rules = dict([(i, rule.split(delim)[1].split(" \t"))
						for i, rule in enumerate(rules[1:], 1)])
		for ruleid, rule in self.rules.items():
			self.rules[ruleid] = dict(body = rule[0].split(), 
				expansion = [rule[1][i:i+self.word_length] for i in xrange(0, len(rule[1]), self.word_length)])
		c = Counter()
		for rule in self.rules.values(): c.update(rule["body"])
		## occurrences of each word in all non-root rules (rule 1 to n)
		self.word2rule_occurrences = dict(c)
		return self

	def tag(self, words):
		"""
		tag each word with their rule_occurances
		"""
		return [self.word2rule_occurrences.get(w, 0) for w in words]

	def get_printable_rules(self):
		"""
		get printable version of rules 
		"""
		rulestr = "0 -> %s" % self.rule0
		for i in xrange(1, len(self.rules)+1):
			rulestr += "\n%i -> %s" % (i, " ".join(self.rules[i]["body"]))
		return rulestr