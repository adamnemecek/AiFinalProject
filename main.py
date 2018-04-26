import siatec as siatec
import hashtec as hashtec
import synthetic_tests as synth_tests
import utils as util
from time import time
from os.path import join

from music_management.paths import DROPBOX_MUSICA_XML_ROOT
from music_management.music_parser import XMLParser


def syntheticDataTest(dataset):
    startSia = time()
    siaTecOutput = siatec.siatec(dataset)
    endSia = time()
    startHash = time()
    hashOutput = hashtec.hashTEC(dataset)
    endHash = time()
    print("Total time for SIATEC: {}\nTotal time for HashTEC: {} seconds".format(endSia - startSia, endHash - startHash))
    hashTecOutput = [(pat, trans) for pat, trans in hashOutput.items()]
    equivOutput = util.isEquivTecSets(siaTecOutput, hashTecOutput, dataset)
    print("SIATEC and HashTEC outputs are equivalent: {} seconds".format(equivOutput))


def musicDataTest(filename):
    piecename = filename[filename.rfind("/") + 1: filename.rfind(".xml")]
    print("Creating note dataset for {}".format(piecename))
    parser = XMLParser()
    (_, parts) = parser.parse_score(filepath=filename)
    dataset = util.pitch_dataset(parts[0]["melody"])
    print("Finished note dataset for {}".format(piecename))
    startSia = time()
    siaTecOutput = siatec.siatec(dataset)
    endSia = time()
    startHash = time()
    hashOutput = hashtec.hashTEC(dataset)
    endHash = time()
    print("Test results for music data from {}".format(piecename))
    print("Total time for SIATEC: {} seconds\nTotal time for HashTEC: {} seconds".format(endSia - startSia, endHash - startHash))

    hashTecOutput = [(pat, trans) for pat, trans in hashOutput.items()]
    equivOutput = util.isEquivTecSets(siaTecOutput, hashTecOutput, dataset)
    print("SIATEC and HashTEC outputs are equivalent: {}".format(equivOutput))



def main():
    test1 = sorted(synth_tests.geometric_data)
    syntheticDataTest(test1)

    scoreName = join(DROPBOX_MUSICA_XML_ROOT, "be_bop/Charlie Parker - Donna_Lee.xml")
    musicDataTest(scoreName)


if __name__ == '__main__':
    main()
