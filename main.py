import siatec as siatec
import hashtec as hashtec
import synthetic_tests as synth_tests
import utils as util
from time import time


def main():
    test1 = sorted(synth_tests.geometric_data)
    startSia = time()
    siaTecOutput = siatec.siatec(test1)
    endSia = time()
    startHash = time()
    hashOutput = hashtec.hashTEC(test1)
    endHash = time()
    hashTecOutput = [(pat, trans) for pat, trans in hashOutput.items()]

    equivOutput = util.isEquivTecSets(siaTecOutput, hashTecOutput)
    print("SIATEC and HashTEC outputs are equivalent: {}".format(equivOutput))
    print("Total time for SIATEC: {}\nTotal time for HashTEC: {}".format(endSia - startSia, endHash - startHash))


if __name__ == '__main__':
    main()
