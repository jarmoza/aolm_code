# Author: Jonathan Armoza
# Creation date: October 15, 2021
# Purpose: Demonstrate the different ways to count Richard's speech from the
#		   beginning of Richard III

# Imports

# Built-ins
import argparse
import os

# Custom
from dq_cleaner import AoLM_TextCleaner


# Globals

# Filepaths
paths = {
	
	"richards_speech": os.getcwd() + os.sep + "richards_speech.txt",
	"richards_speech_1s": os.getcwd() + os.sep + "richards_speech_1s.txt",
}


# Script functions

def main(p_args):

	# 0. Text is selected manually for this script here
	text_filepath = paths["richards_speech_1s"]

	# 1. Show what different cleaning and tokenization methods do to the speech

	# A. Create the text cleaner object
	text_cleaner = AoLM_TextCleaner(text_filepath, p_args.stopwords_type,
		p_args.tokenization_type)

	# B. Get tokens and frequencies of the speech
	tokens = text_cleaner.tokenize()
	frequencies = text_cleaner.token_frequencies
	
	print("Richard's speech cleaned by {0} string cleaning:".format(p_args.tokenization_type))
	print("\n".join(text_cleaner.clean_text_no_sw))
	print("Word counts:\n{0}".format(frequencies))

if "__main__" == __name__:

	# 0. Create the argument parse
	parser = argparse.ArgumentParser()

	# 1. Set up valid flag arguments
	parser.add_argument("tokenization_type", default="aolm")
	parser.add_argument("stopwords_type", default="voyant")

	# 2. Get the arguments from the command line
	args = parser.parse_args()

	main(args)