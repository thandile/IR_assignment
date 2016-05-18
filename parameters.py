# simple extended boolean search engine: configurable parameters
# Hussein Suleman
# 21 April 2016


normalization = False
stemming = True
case_folding = True
log_tf = True
use_idf = True
log_idf = True

#*** Feedback Parameters ***#
feedback = True
feedback_terms = 10
feedback_documents = 5
feedback_weight = 1

incremental_feedback = True
feedback_iterations = 3

positional_feedback = True
term_position_radius = 2
