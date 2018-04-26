import siatec as siatec
import hashtec as hashtec
import synthetic_tests as synth_tests


def main():
    test1 = sorted(synth_tests.geometric_data)
    siaTecOutput = siatec.siatec(test1)
    hashTecOutput = hashtec.hashTEC(test1)
    print(siaTecOutput)
    print(hashTecOutput)


if __name__ == '__main__':
    main()
