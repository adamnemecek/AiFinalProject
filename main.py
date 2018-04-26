import siatec as siatec
import hashtec as hashtec
import synthetic_tests as synth_tests
import utils as util


def main():
    test1 = sorted(synth_tests.geometric_data)
    siaTecOutput = siatec.siatec(test1)
    hashOutput = hashtec.hashTEC(test1)
    hashTecOutput = [(pat, trans) for pat, trans in hashOutput.items()]

    print(siaTecOutput)
    print(hashTecOutput)

    equivOutput = util.isEquivTecSets(siaTecOutput, hashTecOutput)
    print("SIATEC and HashTEC outputs are equivalent: {}".format(equivOutput))


if __name__ == '__main__':
    main()
