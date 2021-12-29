# Author: Jonathan Armoza
# Created: November 13, 2021
# Purpose: Demonstrate measurement and visualization of data quality metric measurements
# as a rate (e.g. a function of time) over the course of 'text-time' in a text
# The idea here is to demonstrate the simplest example of data quality for humanities

# Example #1: Word frequency distribution by chapter

# Steps
# 1: Ingest text by chapter
# 2: Calculate word frequencies for each chapter
# 3: Create cumulative word frequencies for each chapter
# 4: Visualize the change in word frequencies of the top N words by chapter
# 5: Measure the rate of change of each of those top N words by chapter
# 6: Visualize the rate of change of each of those top N words by chapter
# 7: Perform steps 1-6 on a text variant (different edition, different publisher, etc.)
# 8: Compare the change in word frequencies and the rate of change across text variants
# 9: Write about observations

# Requirements
# 1: A document class
# 2: A Text class that contains documents
# 3: Document functionality that tallies word frequencies
# 4: Text functionality that tallies cumulative word frequencies across documents
# 5: A Visualization class that takes word frequency counts and plots them by chapter
# 6: Text functionality that measures the rate of change for word frequencies across documents
# 7: Visualization functionality that plots the rate of change of word frequencies
# 8: A TextCollection class
# 9: TextCollection functionality that compares word frequencies, cumulative word frequencies,
#    and rates of change in word frequency

# Text(s) for example
# 1: Versions of Mark Twain's Huckleberry Finn on Project Gutenberg

# Idea
# Create a datalad for text versions used in The Art of Literary Modeling

# Imports

# Standard library
from collections import Counter
import glob
import json
import os

# Third parties libraries
import nltk

# Local libraries
from data_quality.core.dq_cleaner import AoLM_TextCleaner
from utilities import aolm_paths
from utilities.aolm_utilities import clean_string
from utilities.aolm_utilities import debug_separator

# 0. Setup code and data paths
aolm_paths.setup_paths()

# huckfinn = HuckleberryFinn(paths["input"] + paths["2021-02-21"], huckfinn_headers)
# output_folder = "{0}{1}data{1}output{1}".format(os.getcwd(), os.sep)
# huckfinn.output(output_folder)


# 1. Read in chapters of Huckleberry Finn editions

# A. Folder where json versions of the Huckleberry Finn editions are output
json_folder = aolm_paths.data_paths["aolm_twain"]["gutenberg_dq"] + "input" + os.sep

# B. Read in each edition json
edition_data = {}
for json_filepath in glob.glob(json_folder + "*.json"):

	# I. Filename without the extension is the edition key
	filename_noext = os.path.splitext(os.path.basename(json_filepath))[0]

	# II. Read json but skip non-"HuckFinn" files in the folder
	if "HuckFinn" in filename_noext and "cleaned" not in filename_noext:
		# print(json_filepath)
		with open(json_filepath, "r") as json_fileobject:
			edition_data[filename_noext] = \
				json.load(json_fileobject)

# 2. Clean each edition
for edition in edition_data:

	# A. Create a clean version of the edition's components
	edition_data[edition]["clean_components"] = {}

	# I. Clean each component in the edition
	for component in edition_data[edition]["components"]:

		# a. Treat body differently since it has subcomponents
		if "body" == component:
			
			edition_data[edition]["clean_components"]["body"] = {}

			for subcomponent in edition_data[edition]["components"]["body"]:
				
				# i. Create an entry for the clean version	
				edition_data[edition]["clean_components"]["body"][subcomponent] = []
			
				# ii. Clean each line in the component
				for line in edition_data[edition]["components"]["body"][subcomponent]:
					edition_data[edition]["clean_components"]["body"][subcomponent].append(
						clean_string(line))
		else:
			# i. Create an entry for the clean version
			edition_data[edition]["clean_components"][component] = []
		
			# ii. Clean each line in the component
			for line in edition_data[edition]["components"][component]:
				edition_data[edition]["clean_components"][component].append(
					clean_string(line))

# 3. Calculate word frequencies for each chapter
for edition in edition_data:

	edition_data[edition]["word_counts"] = {}

	for component in edition_data[edition]["clean_components"]:
		
		if "body" == component:
			edition_data[edition]["word_counts"]["body"] = {}
			for subcomponent in edition_data[edition]["clean_components"]["body"]:
				tokens = nltk.word_tokenize("\n".join(edition_data[edition]["clean_components"]["body"][subcomponent]))
				edition_data[edition]["word_counts"]["body"][subcomponent] = Counter(tokens)
		else:
			tokens = nltk.word_tokenize("\n".join(edition_data[edition]["clean_components"][component]))
			edition_data[edition]["word_counts"][component] = Counter(tokens)

# Write out the json with clean data
for edition in edition_data:
	with open(json_folder + edition + "_cleaned.json", "w") as cleaned_json_fileobj:
		json.dump(edition_data[edition], cleaned_json_fileobj, indent=4)
