import siatec as siatec
import hashtec as hashtec
import synthetic_tests as synth_tests
import utils as util
from time import time
from os.path import join
from os import listdir
from tqdm import tqdm
import multiprocessing as mp

from music_parser import XMLParser
import matplotlib.pyplot as plt
import numpy as np


PARKER_ROOT = "./charlie_parker_data/"

def syntheticDataTest(dataset):
    startSia = time()
    siaTecOutput = siatec.siatec(dataset)
    endSia = time()
    startHash = time()
    hashOutput = hashtec.hashTEC(dataset)
    endHash = time()
    # print("Total time for SIATEC: {}\nTotal time for HashTEC: {} seconds".format(endSia - startSia, endHash - startHash))

    # print("HASH OUTPUT: " + str(hashOutput))
    # print("SIA OUTPUT: " + str(siaTecOutput))
    # hashTecOutput = [key for key in hashOutput]

    # equivOutput = util.isEquivTecSets(siaTecOutput, hashTecOutput)
    #
    # if not equivOutput:
    #     util.diagnoseDiff(siaTecOutput, hashTecOutput, dataset)

    # print("HashTEC output:")
    # for tec in hashTecOutput:
    #     print(tec)

    # print("SIATEC and HashTEC outputs are equivalent: {} seconds".format(equivOutput))
    return endSia - startSia, endHash - startHash


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

    # hashTecOutput = [(pat, trans) for pat, trans in hashOutput.items()]
    # equivOutput = util.isEquivTecSets(siaTecOutput, hashTecOutput, dataset)
    # print("SIATEC and HashTEC outputs are equivalent: {}".format(equivOutput))


def pmap(f, xs):
    result = list()
    with mp.Pool(mp.cpu_count()) as p:
        with tqdm(xs) as pbar:
            for i, val in tqdm(enumerate(p.imap(f, xs))):
                result.append(val)
                pbar.update()
    return result


def densityRuntimeTest():
    densities = [0.001, 0.01, 0.1]

    for i, density in enumerate(densities):
        xaxis = np.arange(10, 510, 10)
        datasets = util.randomSampleSetsLinear(10, 500, 10, density=density)

        siaResults = list()
        hashResults = list()
        for dataset in tqdm(datasets, desc="Running for d={}".format(density)):
            siaRes, hashRes = syntheticDataTest(dataset)
            siaResults.append(siaRes)
            hashResults.append(hashRes)

        plt.figure()
        plt.title("Dataset size vs Runtime on Synthetic data with density={}".format(density))
        plt.xlabel("Datasets size")
        plt.ylabel("Runtime in seconds")
        plt.plot(xaxis, siaResults)
        plt.plot(xaxis, hashResults)
        plt.legend(["SIATEC", "HashTEC"])
        plt.savefig("prelim_results_{}.png".format(i))


def multiLengthMusicTest(datasets, xaxis):
    siaResults = list()
    hashResults = list()
    for dataset in tqdm(datasets, desc="Running over datasets"):
        siaRes, hashRes = syntheticDataTest(dataset)
        siaResults.append(siaRes)
        hashResults.append(hashRes)

    return siaResults, hashResults

    # plt.figure()
    # plt.title("Dataset size vs Runtime on Synthetic data on music piece")
    # plt.xlabel("Datasets size")
    # plt.ylabel("Runtime in seconds")
    # plt.plot(xaxis, siaResults)
    # plt.plot(xaxis, hashResults)
    # plt.legend(["SIATEC", "HashTEC"])
    # plt.savefig("music_prelim_results.png")


def main():
    # test1 = sorted(synth_tests.regular_dataset)
    # syntheticDataTest(test1)
    #

    parker_files = list()
    # root_dir = join(DROPBOX_MUSICA_XML_ROOT, "./be_bop/")
    music_files = listdir(PARKER_ROOT)
    for filename in music_files:
        if "Charlie Parker" in filename:
            parker_files.append(join(PARKER_ROOT, filename))

    # filename = join(PARKER_ROOT, "be_bop/Charlie Parker - Donna_Lee.xml")
    # parker_files = parker_files[:2]
    # siaResults = list()
    # hashResults = list()
    # pieceNames = list()
    # numPieces = len(parker_files)
    # for filename in parker_files:
    #     piecename = filename[filename.rfind(" - ") + 3: filename.rfind(".xml")]
    #     pieceNames.append(piecename)
    #     print("Creating note dataset for {}".format(piecename))
    #     parser = XMLParser()
    #     (_, parts) = parser.parse_score(filepath=filename)
    #     dataset = util.pitch_dataset(parts[0]["melody"])
    #     # bounds = np.arange(10, len(dataset) + 10, 10)
    #     # datasets = [dataset[:int(b)] for b in bounds]
    #     # siaRes, hashRes = syntheticDataTest(dataset)
    #     siaTecOutput = siatec.siatec(dataset)
    #     hashOutput = hashtec.hashTEC(dataset)
    #     # sia, hash = multiLengthMusicTest(datasets, bounds)
    #     siaResults.append(len(siaTecOutput))
    #     hashResults.append(len(hashOutput))

    densities = [0.001, 0.01, 0.1]

    siaResults = list()
    hashResults = list()
    for density in densities:
        xaxis = np.arange(10, 510, 10)
        datasets = util.randomSampleSetsLinear(500, 500, 10, density=density)

        for dataset in datasets:
            siaTecOutput = siatec.siatec(dataset)
            hashOutput = hashtec.hashTEC(dataset)
            siaResults.append(len(siaTecOutput))
            hashResults.append(len(hashOutput))

        # plt.figure()
        # plt.title("Dataset size vs Runtime on Synthetic data with density={}".format(density))
        # plt.xlabel("Datasets size")
        # plt.ylabel("Runtime in seconds")
        # plt.plot(xaxis, siaResults)
        # plt.plot(xaxis, hashResults)
        # plt.legend(["SIATEC", "HashTEC"])

    plt.figure()
    plt.title("Patterns found vs density comparison on synthetic data")
    plt.xlabel("Density")
    plt.ylabel("Number of Patterns")
    plt.bar([i - 0.475 for i in range(len(densities))], siaResults, width=0.45)
    plt.bar([i + 0.025 for i in range(len(densities))], hashResults, width=0.45, color="green")
    plt.legend(["SIATEC", "HashTEC"])
    plt.xticks(list(range(len(densities))), densities, rotation=0)
    plt.show()


    # musicDataTest(filename)

    # densityRuntimeTest()
    plt.show()


if __name__ == '__main__':
    main()
