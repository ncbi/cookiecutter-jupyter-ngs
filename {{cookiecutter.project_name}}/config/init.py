import os
import re
import json
import pandas
import math
import pickle
import zipfile
import distutils.spawn
import numpy as np
import scipy.stats as stats
import seaborn as sns

from IPython.display import display

import matplotlib
import matplotlib.pyplot as plt

from IPython.display import HTML
from IPython.display import display, Markdown, Latex

from jupyterngsplugin.utils.errors import check_errors_from_logs

###############################################################
#
#    Update cutoff values
#
###############################################################

# log2(FoldChange)
fc = {{ cookiecutter.fold_change }}

# max FDR (adjusted P-Value)
fdr = {{ cookiecutter.fdr }}

###############################################################
#
#    Project global paths
#
###############################################################

WORKDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
CONFIG = os.path.join(WORKDIR,'config')
DATA = os.path.join(WORKDIR,'data')
BIN = os.path.join(WORKDIR,'bin')
RESULTS = os.path.join(WORKDIR,'results')
NOTEBOOKS = os.path.join(WORKDIR,'notebooks')
SRC = os.path.join(WORKDIR,'src')
TMP = os.path.join(WORKDIR,'tmp')

###############################################################
#
#    Update genome files and indexes path
#
# If indexes and reference bed files does not exist can be created using 
# the notebooks but you need to have writing permission in the GENOME dir
#
###############################################################

GENOME = '{{ cookiecutter.genome_dir }}'
GENOME_NAME = '{{ cookiecutter.genome_name }}'
ALIGNER_INDEX = '{{ cookiecutter.aligner_index_dir }}'
GENOME_FASTA = '{{ cookiecutter.genome_fasta }}'
GENOME_GTF = '{{ cookiecutter.genome_gtf }}'
GENOME_GFF = '{{ cookiecutter.genome_gff }}'
GENOME_GFF3 = '{{ cookiecutter.genome_gff3 }}'
GENOME_BED = '{{ cookiecutter.genome_bed }}'
GENOME_MAPPABLE_SIZE = '{{ cookiecutter.genome_mappable_size }}'
GENOME_BLACKLIST = os.path.join(GENOME, 'mm9-blacklist.bed')

###############################################################
#
#    Dataset (experiment) to analyze
#
# The path is $WORKDIR/data/$DATASET
#
# To use multiple datasets (experiments) this variable should be overwritten
# in the notebooks
#
###############################################################

DATASET = '{{ cookiecutter.dataset_name }}'
IS_DEMO = True if '{{ cookiecutter.is_data_in_SRA }}' == 'y' and '{{ cookiecutter.create_demo }}' == 'y' else False

###############################################################
#
#    Docker configuration
#
###############################################################

DOCKER = True if '{{ cookiecutter.use_docker }}' == 'y' else False

###############################################################
#
#    cwl-runner with absolute path if necesary 
#
###############################################################

CWLRUNNER_TOOL = '{{ cookiecutter.cwl_runner }}'
CWLRUNNER_TOOL_PATH = distutils.spawn.find_executable(CWLRUNNER_TOOL)
if not CWLRUNNER_TOOL_PATH:
    print('WARNING: %s not in path' % (CWLRUNNER_TOOL))
    print('Install:')
    print('pip install cwltool')
    print('pip install cwl-runner')
else:
    CWLRUNNER = CWLRUNNER_TOOL_PATH
if not DOCKER:
    CWLRUNNER = CWLRUNNER + ' --no-container '

###############################################################


CWLURL = '{{ cookiecutter.cwl_workflow_repo }}'
CWLTOOLS = os.path.join(CWLURL, 'tools')
CWLWORKFLOWS = os.path.join(CWLURL, 'workflows')

CWLRUNNER = CWLRUNNER + ' --rm-tmpdir --tmp-outdir-prefix=' + TMP + '/ --tmpdir-prefix=' + TMP + '/ '
