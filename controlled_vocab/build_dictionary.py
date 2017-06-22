#!/usr/bin/python

##########################################################################################

# This pipeline is used to build a dictionary out of the metadata from the DEEP project

##########################################################################################

import os
import codecs
import sys
import pickle
import functions

####################################################################################################


#get directory either from arguments or from user
arguments = sys.argv
if len(arguments) == 1:
	directory = raw_input("Please give the path to the directory containing the metadata you want to build the dictionary for:")
else:
	directory = sys.argv[1]


if not directory.endswith("/"):		#adding a slash to the directory name in case it was forgotten
	directory = directory + "/"


if os.path.exists(directory):	#check the path
	experiment_data_files = []
	sample_data_files = []
	for root, dirs, files in os.walk(directory):	#Checking the directory and sub direcotory recursively and make a list of files
		for f in files:
			if f.endswith("emd.tsv"):
				experiment_data_files.append(os.path.join(root, f))	#joining the name of the file with the path
			elif f.endswith("smd.txt"):
				sample_data_files.append(os.path.join(root, f))		#joining the name of the file with the path
else:
	print "The path you gave does not exist, please check it and try again"
	sys.exit()


regex_keys = ['ChromatinAccessibility_CHROMATIN_AMOUNT',
'BIOLOGICAL_REPLICATE_ID',
'EXTRACTION_PROTOCOL_STARTING_NR_CELLS',
'SAMPLE_ID',
'SEQUENCING_DATE',
'EXTRACTION_PROTOCOL_SONICATION_FRAGMENT_SIZE_RANGE',
'RNA_cDNA_PREPARATION_INITIAL_RNA_QNTY',
'RNA_cDNA_PREPARATION_PCR_NUMBER_CYCLES',
'CHIP_PROTOCOL_CHROMATIN_AMOUNT',
'EXPERIMET_DATE',
'LIBRARY_GENERATION_INITIAL_INPUT_QNTY',
'TECHNICAL_REPLICATE_ID',
'EXPERIMENT_ID',
'ChromatinAccessibility_ENZYME_AMOUNT',
'LIBRARY_GENERATION_PCR_NUMBER_CYCLES',
'CHIP_PROTOCOL_DURATION_CROSSLINKING',
'LIBRARY_GENERATION_FRAGMENT_SIZE_SELECTION']


black_keys = ['TECHNICAL_REPLICATE_ID',
'BIOLOGICAL_REPLICATE_ID',
'EXTRACTION_PROTOCOL',
'LIBRARY_GENERATION_ADAPTOR_LIGATION_PROTOCOL',
'LIBRARY_GENERATION_ADAPTOR_SEQUENCE',
'LIBRARY_GENERATION_PCR_F_PRIMER_SEQUENCE',
'LIBRARY_GENERATION_PCR_POLYMERASE_TYPE',
'LIBRARY_GENERATION_PCR_PRIMER_CONC',
'LIBRARY_GENERATION_PCR_R_PRIMER_SEQUENCE',
'LIBRARY_GENERATION_PCR_TEMPLATE_CONC',
'LIBRARY_GENERATION_PCR_THERMOCYCLING_PROGRAM',
'LIBRARY_GENERATION_cDNA_FRAGMENTATION',
'CHIP_PROTOCOL',
'CHIP_PROTOCOL_BEAD_TYPE',
'CHIP_PROTOCOL_PERC_CH2O_CROSSLINKING',
'CHIP_PROTOCOL_SHEARING_METHOD',
'CHIP_PROTOCOL_SHEARING_CYCLES',
'CHIP_PROTOCOL_SHEARING_FREQUENCY',
'CHIP_PROTOCOL_IPSTAR_CONDITIONS',
'FULL_LENGTH_PROTOCOL_LINK',
'EXTRACTION_PROTOCOL_SONICATION_CYCLES',
'EXTRACTION_PROTOCOL_TYPE_OF_SONICATOR',
'DNA_PREPARATION_FRAGMENT_SIZE_RANGE',
'DNA_PREPARATION_INITIAL_DNA_QNTY',
'SEQUENCING_PLATFORM_VERSION',
'SEQUENCING_CYCLES',
'SEQUENCING_LANE',
'SEQUENCING_FC_ID',
'SEQUENCING_RUN_TYPE',
'SEQUENCING_CONTROL_SOFTWARE_VERSION',
'RNA_cDNA_PREPARATION_REVERSE_TRANSCRIPTION_PROTOCOL',
"RNA_PREPARATION_3'_RNA_ADAPTER_LIGATION_PROTOCOL",
"RNA_PREPARATION_3'_RNA_ADAPTER_SEQUENCE",
"RNA_PREPARATION_5'_DEPHOSPHORYLATION",
"RNA_PREPARATION_5'_PHOSPHORYLATION",
"RNA_PREPARATION_5'_RNA_ADAPTER_LIGATION_PROTOCOL",
"RNA_PREPARATION_5'_RNA_ADAPTER_SEQUENCE",
'METADATA_TAG']


#Get a list of all keys using list_keys from functions
experiment_keys = functions.list_keys(experiment_data_files, regex_keys, black_keys)
sample_keys = functions.list_keys(sample_data_files, regex_keys, black_keys)



#make the dictionry using make_dic from functions
experiments_dictionary = functions.build_dic(experiment_keys, experiment_data_files)
f = open("experiments_dictionary.txt", "w+")
pickle.dump(experiments_dictionary, f)
f.close()



samples_dictionary = functions.build_dic(sample_keys, sample_data_files)
f = open("samples_dictionary.txt", "w+")
pickle.dump(samples_dictionary, f)
f.close()

