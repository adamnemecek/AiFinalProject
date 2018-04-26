from xml.etree.ElementTree import parse
from os.path import join
# from pickle import dump, load
from zipfile import ZipFile
from tqdm import tqdm
from os import walk
# import sys

from music_management.music_utils import get_pitch_val, get_key_type, get_key_root, get_bpm
from music_management.music_utils import assign_dur_label   # determine_duration
from music_management.music_utils import KeyType, MusicElement
from music_management.paths import DROPBOX_MUSICA_XML_ROOT


class XMLParser(object):
    def __init__(self):
        pass

    def check_filepath(self, fp):
        """
        This function checks to see if the filepath provided is an XML or compressed
        MusicXML file. If the file is compressed then this function expands the file into
        regular MusicXML form. The new expanded file is stored at musica/extracted_xml/

        :param fp: [String] Filepath to check for XML or MXL file
        :return: [String] Filepath of new XML music file

        NOTE: This function does not check that the contents of the file are properly
        formatted MusicXML, the only check performed is that the filepath returns points
        to a decompressed .xml file
        """
        if fp.endswith(".mxl"):
            zipper = ZipFile(fp, "r")
            files = list(filter(lambda x: x.endswith(".xml") and "/" not in x, zipper.namelist()))
            return zipper.extract(files[0], path="../../extracted_xml/")
        elif not fp.endswith(".xml"):
            raise ParserError("unkonwn filetype found --> {0}".format(fp))
            return None
        return fp

    def parse_music_scores(self, music_path=DROPBOX_MUSICA_XML_ROOT, save_name="jazz_data"):
        """
        This function creates a dictionary of all the scores found in a recursive search
        of the directory passed in as the music_path argument. All scores found are parsed
        and returned with the filename of the piece as the key to access the respective
        scores part-list

        :param music_path: [String] path to a directory which contains MusicXML files
        :return: [Dictionary] Hash-map of scores parser

        FIXME: Currently an error in parsing a score is fatal
        """
        files = [join(root, elm) for root, dirs, files in walk(music_path) for elm in files]
        xml_files = filter(lambda x: x.endswith((".xml", ".mxl")), files)
        scores = {fp[fp.rfind("/") + 1:]: self.parse_score(fp) for fp in tqdm(xml_files, desc="Parsing Music XML")}
        return scores

    def parse_measure(self, measure, m_num):
        """
        This function parses a MusicXML measure and transforms the datacontained into it
        into three separate temporal lists. The lists represent the melody, harmony and
        key-signature as found in the measure. The lists are returned in a dictionary.
        This function contains subroutines that are used to parse the musical features
        that will be found in the XML for a measure.

        :param measure: [List] Data from MusicXML representing a musical measure
        :param m_num: [Integer] The number of the current measure for use in setting offsets
        :return: [Dictionary] lists of all musical objects found, spearated into melody, harmony, and key-signature
        """
        result = {"key": list(), "harmony": list(), "melody": list()}
        sum_dur = 0

        def parse_attribute(attrib):
            """
            This function parses out a key-signature object from MusicXML.

            :param attrib: [List] Data from MusicXML representing a attribute tag
            :return: [Tuple] key-signature tuple of the form (root-pitch, key-mode, key-onset)
            """
            for att in attrib:
                # print(len(att))
                if att.tag == "key":
                    if len(att) >= 2:
                        key_type = get_key_type(att[1].text)
                        root = get_key_root(int(att[0].text), key_type)
                        return (root, key_type, (m_num, sum_dur))
                    else:
                        return (-1, -1, (m_num, sum_dur))

        def parse_harmony(harmony):
            """
            This function parses out a harmony object from MusicXML.

            :param harmony: [List] Data from MusicXML representing a harmony tag
            :return: [Tuple] harmony tuple of the form (root-pitch, Harm-mode, Harm-onset)
            """
            alteration = int(harmony[0][1].text) if len(harmony[0]) > 1 else 0
            root_pitch = get_pitch_val(harmony[0][0].text, alt=alteration)
            kind = get_key_type(harmony[1].text)
            return (root_pitch, kind, (m_num, sum_dur))

        def parse_music_element(music_el):
            """
            This function parses out a musical object from MusicXML. The musical object
            can be either the representation of a Note, Rest, or Chord.

            :param music_el: [List] Data from MusicXML representing a note tag
            :return: [Tuple] music object of the form (type, pitch, duration, note-onset)
            """
            mtype, midi, duration, tied = -1, -1, 0, "none"
            for item in music_el:
                if item.tag == "chord":
                    mtype = MusicElement.CHORD
                elif item.tag == "pitch":
                    if mtype != MusicElement.CHORD:
                        mtype = MusicElement.NOTE
                    has_alt = len(item) > 2
                    alteration = float(item[1].text) if has_alt else 0
                    octave = int(item[2].text) if has_alt else int(item[1].text)
                    midi = get_pitch_val(item[0].text, octave, alteration)
                    if not isinstance(midi, int):
                        print("Midi pitch value returned {0} of type {1}".format(midi, type(midi)))
                elif item.tag == "rest":
                    mtype = MusicElement.REST
                elif item.tag == "duration":
                    duration = int(item.text)
                elif item.tag == "notations":
                    for child in item:
                        if child.tag == "tied":
                            tied = child.attrib["type"]
                            break
            return (mtype, midi, duration, tied)

        for music_el in measure:
            if music_el.tag == "note":
                element = parse_music_element(music_el)
                if element[0] == MusicElement.CHORD:    # guards the increment for sum_dur
                    last = result["melody"].pop()
                    pitches = (last[1],) + (element[1],) if not isinstance(last[1], tuple) else last[1] + (element[1],)
                    element = (element[0], pitches, element[2], element[3])
                else:
                    sum_dur += element[2]
                result["melody"].append(element)
            elif music_el.tag == "harmony":
                chord = parse_harmony(music_el)
                if len(result["harmony"]) == 0 and m_num == 1 and chord[2][1] != 0:
                    result["harmony"].append((-1, KeyType.UNSET, (m_num, 0)))
                result["harmony"].append(chord)
            elif music_el.tag == "attributes":
                attribute = parse_attribute(music_el)
                if attribute is not None:
                    if len(result["key"]) == 0 and m_num == 1 and attribute[2][1] != 0:
                        result["key"].append((-1, KeyType.UNSET, (m_num, 0)))
                    result["key"].append(attribute)

        measure_dur = 0
        melody = list()
        for (mtype, pitch, dur, tied) in result["melody"]:
            onset = (m_num, measure_dur / sum_dur)
            measure_dur += dur
            dur_label = assign_dur_label(dur, sum_dur)
            melody.append((mtype, pitch, dur_label, onset, tied))
        key = [(r, k, (m, o / sum_dur)) for (r, k, (m, o)) in result["key"]]
        harmony = [(r, k, (m, o / sum_dur)) for (r, k, (m, o)) in result["harmony"]]

        return {"melody": melody, "harmony": harmony, "key": key}

    def parse_part(self, music_part):
        """
        This function parses a part from MusicXML. Each part consists of a melody,
        harmony, and key-signature list. These lists are created by parsing MusicXML
        data from a list of measures.

        :param music_part: [List] Data from MusicXML in the form of a list of measures
        :return: [Dictionary] container for melody, harmony, and key-signature lists
        """
        result = {"key": list(), "harmony": list(), "melody": list()}

        for i, measure in enumerate(music_part):
            temp_results = self.parse_measure(measure, i+1)
            result["key"].extend(temp_results["key"])
            result["harmony"].extend(temp_results["harmony"])
            result["melody"].extend(temp_results["melody"])

        new_melody = list()
        i = 0
        while i < len(result["melody"]):
            nor = result["melody"][i]
            if nor[4] == "start":
                sum_dur = nor[2]
                while True:
                    i += 1
                    if i >= len(result["melody"]):
                        break
                    sum_dur += result["melody"][i][2]

                    if result["melody"][i][4] == "stop":
                        break
                new_melody.append((nor[0], nor[1], sum_dur, nor[3]))
                # continue
            else:
                new_melody.append(nor[:4])
            i += 1

        result["melody"] = new_melody
        return result

    def parse_score(self, filepath=join(DROPBOX_MUSICA_XML_ROOT, "Barney Bigard - Tiger Rag solo 1.xml")):
        """
        This function parses a MusicXML score into a list of parts found in the score.

        :param filepath: [String] The MusicXML file to be parsed
        :return: [Tuple] (beats-per-minute, partl-list) found in the MusicXML file
        """

        def parse_direction(part):
            """
            This function parses through the first part in a MusicXML file to find the
            beats-per-minute of the whole piece. NOTE: This function assumes that the
            beats-per-minute can only be found in the first part and that the
            beats-per-minute is constant for every part in a given piece.

            :param part: [List] Data from MusicXML to be used to find a direction tag
            :return: [Integer] Numerical representation of the beats-per-minute or None

            Implementation Note: This function can return None
            """
            for music_el in part[0]:
                if music_el.tag == "direction" and music_el[0].tag == "direction-type" and music_el[0][0].tag == "metronome":
                    metronome = music_el[0][0]
                    beat_std = metronome[0].text
                    unscaled_bpm = int(metronome[1].text)
                    return get_bpm(beat_std, unscaled_bpm)
        safe_path = self.check_filepath(filepath)
        root = parse(safe_path).getroot()
        part_list = [el for el in root if el.tag == "part"]
        score = [self.parse_part(part) for part in part_list]
        beat = parse_direction(part_list[0])
        return (beat, score)


class ParserError(ValueError):
    pass
