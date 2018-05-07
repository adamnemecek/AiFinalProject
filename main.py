import siatec as siatec
import hashtec as hashtec
import synthetic_tests as synth_tests
import utils as util
from time import time
from os.path import join
from os import listdir

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
    return endSia - startSia, endHash - startHash


def densityRuntimeTest():
    densities = [0.001, 0.01, 0.1]

    for i, density in enumerate(densities):
        xaxis = np.arange(10, 510, 10)
        datasets = util.randomSampleSetsLinear(10, 500, 10, density=density)

        siaResults = list()
        hashResults = list()
        for dataset in datasets:
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


def musicCompTest():
    parker_files = list()
    music_files = listdir(PARKER_ROOT)
    for filename in music_files:
        if "Charlie Parker" in filename:
            parker_files.append(join(PARKER_ROOT, filename))

    filename = join(PARKER_ROOT, "be_bop/Charlie Parker - Donna_Lee.xml")
    parker_files = parker_files[:2]
    siaResults = list()
    hashResults = list()
    pieceNames = list()
    numPieces = len(parker_files)
    parser = XMLParser()
    for filename in parker_files:
        piecename = filename[filename.rfind(" - ") + 3: filename.rfind(".xml")]
        pieceNames.append(piecename)
        print("Creating note dataset for {}".format(piecename))

        (_, parts) = parser.parse_score(filepath=filename)
        dataset = util.pitch_dataset(parts[0]["melody"])
        siaTecOutput = siatec.siatec(dataset)
        hashOutput = hashtec.hashTEC(dataset)
        siaResults.append(len(siaTecOutput))
        hashResults.append(len(hashOutput))


def compDensityTest():
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


def main():
    test1 = sorted(synth_tests.regular_dataset)
    syntheticDataTest(test1)

    # musicCompTest()
    # compDensityTest()


if __name__ == '__main__':
    main()
