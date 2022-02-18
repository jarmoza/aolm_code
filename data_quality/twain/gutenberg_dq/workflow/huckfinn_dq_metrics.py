# Author: Jonathan Armoza
# Created: February 15, 2022
# Purpose: Contains all of the data quality metrics for Art of Literary Modeling's
#          analysis of Mark Twain's 'The Adventures of Huckleberry Finn'

"""
Data quality discussion section

===============================================================================
Intrinsic data quality 

May be a measure of the success of matching an iteration (digitized copy,
alternate edition, etc.) of a text to a physical or digital source that is
considered to be the primary/reputable edition

Intrinsic dimensions include accuracy, objectivity, believability, and reputation

===============================================================================
Contextual data quality

May be whether the metrical characteristics of the data set make it viable for
the selected modeling task to follow. 

Contextual dimensions include amount of value-added, relevancy, timeliness,
completeness and appropriate amount of data

===============================================================================
Representational data quality

May ask several questions. Is the data collected from the text easily
interpretable/understandable? Is it arranged in such a way to make it easily
interpretable/understandable? And for when that metadata is displayed via
interfaces, is it presented in such a way to make it easily interpretable and
understandable?

Representational dimensions include interpretability, ease of understanding,
representational consistency, and representational conciseness

===============================================================================
Accessibility data quality

One can also imagine a whole ranking for accessibility quality via several
avenues and understandings on physical accessibility. Is the consumer of
literary data able to access a literary data set? The answer to this question
represents a well-known but, without a data quality configuration, overlooked
standard for quality when performing computational text analysis. What is the
source of the data set and what are the barriers in place to access it? Is it
on a free site? Free but requires a login? Institutional? Paywalled? Limited to
individual requests? Or maybe even not available at all?

Accessibility dimensions include accessibility and access security

"""

# Imports

# Standard libraries
from abc import abstractmethod
import json
import os

# Local libraries
from data_quality.core.dq_metric import DataQualityMetric
from utilities import aolm_paths


# Classes 

# This object knows how to ingest HuckFinn metadata
class HuckFinnDQMetric(DataQualityMetric):

    # Constructor

    def __init__(self, p_name, p_metadata_json):

        # 1. Call the base data quality class constructor
        super().__init__(p_name, p_metadata_json)

    # HuckFunn-specific properties from its metadata
    @property
    def clean_components(self):
        return self.m_input["clean_components"]
    @property
    def components(self):
        return self.m_input["components"]
    @property
    def cumulative_word_counts(self):
        return self.m_input["cumulative_word_counts"]
    @property
    def flat_components(self):
        return self.m_input["flat_components"]
    @property
    def top_words(self):
        return self.m_input["top_words"]
    @property
    def top_word_counts_by_chapter(self):
        return self.m_input["top_word_counts_by_chapter"]
    @property
    def total_word_frequencies(self):
        return self.m_input["total_word_frequencies"]
    @property
    def word_counts(self):
        return self.m_input["word_counts"]

    # Specialized properties

    @property
    def metadata(self):
        return self.m_input


    # Required interface methods
    @abstractmethod
    def compute(self):
        pass

    def output(self):
        return { "metric": self.m_result }
        


class HuckFinnDQ_IntrinsicOverallMatch(HuckFinnDQMetric):

    # Constructor

    def __init__(self, p_source_metadata_json, p_compared_metadata_json):

        # 1. Call the base Huck Finn data quality class constructor
        super().__init__("IntrinsicOverallMatch", p_compared_metadata_json)

        # 2. Save the source (ground truth) metadata json
        self.m_source_metadata_json = p_source_metadata_json

    # Properties

    @property
    def source_metadata(self):
        return self.m_source_metadata_json

    # Required methods
    def compute(self):
        
        # Data quality metric: Comparing overall word counts
        # Goal: Calculate +/- word counts (and, implicitly, missing words)
        
        # 0. HuckFinn metadata key for comparison
        key = "total_word_frequencies"

        # 1. Calculate the total words in each text
        total_words = sum(self.metadata[key].values())
        source_total_words = sum(self.source_metadata[key].values())

        # 2. Create an overall +/- tally of word counts
        word_match_tally = 0
        for word in self.source_metadata[key]:
            
            # A. Check to see if word in source text is in this text
            if word in self.metadata[key]:
                word_match_tally += self.metadata[key][word] - self.source_metadata[key][word]
            # B. If the word is not in this text, subtract the source text frequency from the tally
            else:
                word_match_tally -= self.source_metadata[key][word]

        # 3. Determine the overall intrinsic, percent match metric
        
        # Let's try the word match tally first
        self.m_result = word_match_tally


def main():

    # 0. Setup code and data paths
    aolm_paths.setup_paths()

    # 0. IO paths
    root_folder = aolm_paths.data_paths["twain"]["huckleberry_finn"]
    sub_folder = "comparisons{0}word_frequency".format(os.sep)
    input_folder = "{0}{2}{1}input{1}json{1}".format(root_folder, os.sep, sub_folder)
    output_folder = "{0}{2}{1}output{1}".format(root_folder, os.sep, sub_folder)
    stopwords_filepath = aolm_paths.data_paths["aolm_general"]["voyant_stopwords"]
    source_text_filename = "2021-02-21-HuckFinn_cleaned_processed.json"
    text_filename = "adventureshuckle00twaiiala_demarcated_processed.json"
    source_text_filepath = input_folder + source_text_filename
    text_filepath = input_folder + text_filename

    # 1. Read in the source text and compared text metadata files
    with open(source_text_filepath, "r") as input_file:
        source_metadata_json = json.load(input_file)
    with open(text_filepath, "r") as input_file:
        text_metadata_json = json.load(input_file)

    # 2. Compute the data quality metric for intrinsic, overall match
    dq_metric = HuckFinnDQ_IntrinsicOverallMatch(
        source_metadata_json,
        text_metadata_json
    )
    dq_metric.compute()

    # 3. Output the metric value
    print("{0} metric between '{1}' and '{2}': {3}".format(
        dq_metric.name,
        source_text_filename,
        text_filename,
        dq_metric.result
    ))





if "__main__" == __name__:
    main()
