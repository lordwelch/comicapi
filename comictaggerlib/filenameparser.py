"""
Functions for parsing comic info from filename 

This should probably be re-written, but, well, it mostly works!

"""

"""
Copyright 2012  Anthony Beville

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


# Some portions of this code were modified from pyComicMetaThis project
# http://code.google.com/p/pycomicmetathis/

import re
import os
from urllib import unquote

class FileNameParser:
	def fixSpaces( self, string, remove_dashes=True ):
		if remove_dashes:
			placeholders = ['[-_]','  +']
		else:
			placeholders = ['[_]','  +']			
		for ph in placeholders:
			string = re.sub(ph, ' ', string )
		return string.strip()

	# check for silly .1 or .5 style issue strings
	# allow up to 5 chars total
	def isPointIssue( self, word ):
		ret = False
		try:
			float(word)
			if (len(word) < 5 and not word.isdigit()):
				ret = True
		except ValueError:
			pass
		return ret


	def getIssueCount( self,filename ):

		count = ""
		# replace any name seperators with spaces
		tmpstr = self.fixSpaces(filename)
		found = False
		
		match = re.search('(?<=\sof\s)\d+(?=\s)', tmpstr, re.IGNORECASE)
		if match:
			count = match.group()
			found = True

		if not found:
			match = re.search('(?<=\(of\s)\d+(?=\))', tmpstr,  re.IGNORECASE)
			if match:
				count = match.group()
				found = True
			

		count = count.lstrip("0")

		return count
		
		
	def getIssueNumber( self, filename ):

		found = False
		issue = ''
		
		# first, look for multiple "--", this mean's it's formatted differently from most:
		if "--" in filename:
			# the pattern seems to be that anything to left of the first "--" is the series name followed by issue
			filename = filename.split("--")[0]
		elif "___" in filename:
			# the pattern seems to be that anything to left of the first "__" is the series name followed by issue
			filename = filename.split("__")[0]

		filename = filename.replace("+", " ")
			
		# remove parenthetical phrases
		filename = re.sub( "\(.*\)", "", filename)
		filename = re.sub( "\[.*\]", "", filename)
		
		# guess based on position

		# replace any name seperators with spaces
		tmpstr = self.fixSpaces(filename)
		word_list = tmpstr.split(' ')
		
		#before we search, remove any kind of likely "of X" phrase
		for i in range(0, len(word_list)-2):
			if ( word_list[i].isdigit() and
				word_list[i+1] == "of"  and
				word_list[i+2].isdigit() ):
				word_list[i+1] ="XXX"
				word_list[i+2] ="XXX"
				
				
		# first look for the last "#" followed by a digit in the filename. this is almost certainly the issue number
		#issnum = re.search('#\d+', filename)
		matchlist = re.findall("#[-+]?([0-9]*\.[0-9]+|[0-9]+)", filename)
		if len(matchlist) > 0:
			#get the last item
			issue = matchlist[ len(matchlist) - 1]
			found = True

		# assume the last number in the filename that is under 4 digits is the issue number
		if not found:
			for word in reversed(word_list):
				if len(word) > 0 and word[0] == "#":
					word = word[1:]
				if ( 
					 (word.isdigit() and len(word) < 4) or
					 (self.isPointIssue(word))
					):
					issue = word
					found = True
					#print 'Assuming issue number is ' + str(issue) + ' based on the position.'
					break

		if not found:
			# try a regex
			issnum = re.search('(?<=[_#\s-])(\d+[a-zA-Z]|\d+\.\d|\d+)', filename)
			if issnum:
				issue = issnum.group()
				found = True
				#print 'Got the issue using regex. Issue is ' + issue 
		
		return issue.strip()

	def getSeriesName(self, filename, issue ):

		# use the issue number string to split the filename string
		# assume first element of list is the series name, plus cruft
		#!!! this could fail in the case of small numerics in the series name!!!

		# TODO:  we really should pass in the *INDEX* of the issue, that makes 
		# finding it easier
		
		filename = filename.replace("+", " ")
		tmpstr = self.fixSpaces(filename, remove_dashes=False)
		
		#remove pound signs.  this might mess up the series name if there is a# in it.
		tmpstr = tmpstr.replace("#", " ")

		if issue != "":	
			# assume that issue substr has at least one space before it
			issue_str = " " + str(issue)
			series = tmpstr.split(issue_str)[0]
		else:
			# no issue to work off of
			#!!! TODO we should look for the year, and split from that
			# and if that doesn't exist, remove parenthetical phrases
			series = tmpstr
			series = re.sub( "\(.*\)", "", tmpstr)
			
		volume = ""
		
		series = series.rstrip("#")
			
		# search for volume number
		match = re.search('(.+)([vV]|[Vv][oO][Ll]\.?\s?)(\d+)\s*$', series)
		if match:
			series = match.group(1)
			volume = match.group(3)
		
		return series.strip(), volume.strip()

	def getYear( self,filename):

		year = ""
		# look for four digit number with "(" ")" or "--" around it
		match = re.search('(\(\d\d\d\d\))|(--\d\d\d\d--)', filename)
		if match:
			year = match.group()
			# remove non-numerics
			year = re.sub("[^0-9]", "", year)
		return year

	def parseFilename( self, filename ):

		# remove the path
		filename = os.path.basename(filename)

		# remove the extension
		filename = os.path.splitext(filename)[0]

		#url decode, just in case
		filename = unquote(filename)

		# sometimes archives get messed up names from too many decodings
		# often url encodings will break and leave "_28" and "_29" in place
		# of "(" and ")"  see if there are a number of these, and replace them
		if filename.count("_28") > 1 and filename.count("_29") > 1:
			filename = filename.replace("_28", "(")
			filename = filename.replace("_29", ")")
		
		# ----HACK  
		# remove the first word that word is a 3 digit number.
		# some story arcs collection packs do this, but it's ugly
		# this will probably break something, i.e. "100 bullets"
		#word = filename.split(' ')[0]
		#if len(word) == 3 and word[0] =='0' and word.isdigit():
		#	filename = filename[4:]
		# ----HACK  -
					
		self.issue = self.getIssueNumber(filename)
		self.series, self.volume = self.getSeriesName(filename, self.issue)
		self.year = self.getYear(filename)
		self.issue_count = self.getIssueCount(filename)
	
		if self.issue != "":
			# strip off leading zeros
			self.issue = self.issue.lstrip("0")
			if self.issue == "":
				self.issue = "0"
			if self.issue[0] == ".":
				self.issue = "0" + self.issue

