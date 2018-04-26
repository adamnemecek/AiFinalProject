from os.path import join, expanduser, normpath
from os.path import dirname, realpath


# --------------------------------------------------------------------------------
# Corpora paths
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Path to Dropbox corpus -- should be
ROOT = expanduser('~')
CUR_FILE = dirname(realpath(__file__))
# MUSICA_ROOT = normpath(join(ROOT, "musica/"))
MUSICA_ROOT = normpath(join(CUR_FILE, "../../"))
PICKLE_PATH = normpath(join(MUSICA_ROOT, "pickled_data/"))
DROPBOX_MUSICA_ROOT = normpath(join(ROOT, 'Dropbox/musica'))
DROPBOX_MUSICA_XML_ROOT = normpath(join(DROPBOX_MUSICA_ROOT, 'data/XML_data'))
XML_MUSIC_ROOT = normpath(join(MUSICA_ROOT, "data/XML_data/"))
CLAVIER_PATH = normpath(join(MUSICA_ROOT, "data/well_tempered_clavier/"))
JSON_KEY_DATA_PATH = normpath(join(MUSICA_ROOT, "musica_src/analysis/key_prediction/"))
# Test:
# print listdir(DROPBOX_MUSICA_XML_ROOT)


# --------------------------------------------------------------------------------
# Paths to music_src-relative corpora

EXCERPTS_ROOT = '../../excerpts'

DAVIS_SO_WHAT_ROOT = join(EXCERPTS_ROOT, 'miles_davis-so_what')

TENSION_RELEASE_ROOT = join(EXCERPTS_ROOT, 'tension_release')

CHAROLD_20160304_ROOT = '../../data/cherald_20160304'
auprivave_path = join(CHAROLD_20160304_ROOT, 'Au Privave - Sonny Stitt.xml')


# --------------------------------------------------------------------------------
# Paths for 2015-Nov site visit generation demo

mini_corpus_root = '../../data/mini_corpus/'

# example_model_path = join(corpus_root, 'brown-easy_living.xml')
'Measure 8 Staff 1 incomplete. Expected: 33/32; Found: 5941/5760'
'Measure 11 Staff 1 incomplete. Expected: 4/4; Found: 3065/3072'
# example_model_path = join(corpus_root, 'brown-portrait_of_jenny.xml')
'Fatal error: line 668 column 14 Element stem is not defined in this scope.'

# example_model_path = join(corpus_root, 'brown-september_song.xml')
example_model_path = join(mini_corpus_root, 'hubbard-hammerhead.xml')

# hubbard-hammerhead.xml


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
