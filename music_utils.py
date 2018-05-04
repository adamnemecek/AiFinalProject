
def enum(**args):
    return type('Enum', (), args)


# =======================================================================================
# Chord Scale Constants

MAJOR_VALUES = (0, 2, 4, 5, 7, 9, 11)
MINOR_VALUES = (0, 2, 3, 5, 7, 8, 9, 10, 11)
AUGMENTED_VALUES = ()
DIMINISHED_VALUES = (0, 3, 6, 9)
# NOTE: All of the above appear in triads

DOMINANT_VALUES = (0, 2, 4, 5, 7, 9, 10)
HALF_DIMINISHED_VALUES = (0, 3, 6, 10)
MINOR_MAJOR_VALUES = ()
AUGMENTED_MAJOR_VALUES = ()
# NOTE: All of the above appear in seventh chords
# =======================================================================================


# =======================================================================================
PENTATONIC_MINOR = (0, 3, 5, 7, 10)
PENTATONIC_MAJOR = (0, 2, 4, 7, 9)
BLUES_SCALE = (0, 3, 5, 6, 7, 10)
# =======================================================================================
PITCHES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
KEYS = ("M", "m", "Mm", "A", "d", "D", "hd", "S4", "M6", "m6", "M7", "m7", "A7", "d7", "M9", "m9", "D9", "m11", "D13", "S2")
# =======================================================================================
# ENUM DEFINITIONS
# =======================================================================================


Duration = enum(
    BRV=2.0,            # Breve (Found in bach chorales)
    WHL=1.0,            # whole note = one measure in 4/4
    DHLF=0.75,          # dotted half
    HLF=0.5,            # half note
    DQTR=0.375,         # dotted quarter
    QTR=0.25,           # quarter note
    DEGT=0.1875,        # dotted eighth
    EGT=0.125,          # eighth note
    DSXT=0.09375,       # dotted sixteenth
    SXT=0.0625,         # sixteenth note
    DTSD=0.046875,      # dotted thirtysecond
    TSD=0.03125,        # thirtysecond note
    SXF=0.015625        # sixty-fourth note
)

KeyType = enum(
    UNSET=-1,           # Unset
    MAJOR=0,            # Major
    MINOR=1,            # Minor
    MAJMIN=2,           # Major-Minor
    AUGMENTED=3,        # Augmented
    DIMINISHED=4,       # Diminished
    DOMINANT=5,         # Dominant
    HALFDIM=6,          # Half-Diminished
    SUS4=7,             # Suspended-fourth
    MAJ6=8,             # Major-sixth
    MIN6=9,             # Minor-sixth
    MAJ7=10,            # Major-seventh
    MIN7=11,            # Minor-seventh
    AUG7=12,            # Augmented-seventh
    DIM7=13,            # Diminished-seventh
    MAJ9=14,            # Major-ninth
    MIN9=15,            # Minor-ninth
    DOM9=16,            # Dominant-ninth
    MIN11=17,           # Minor-eleventh
    DOM13=18,           # Dominant-thirteenth
    SUS2=19             # Suspended-second
)

MusicElement = enum(
    NOTE=0,
    REST=1,
    CHORD=2
)

HOLD = '__'
START = 'START'
END = 'END'

CHORD_SCALES = {
    KeyType.MAJOR: (0, 2, 4, 5, 7, 9, 11),
    KeyType.MINOR: (0, 2, 3, 5, 7, 8, 9, 10, 11),
    KeyType.AUGMENTED: (),
    KeyType.DIMINISHED: (0, 3, 6, 9),
    KeyType.DOMINANT: (0, 2, 4, 5, 7, 9, 10),
    KeyType.HALFDIM: (0, 3, 6, 10),
    KeyType.MAJMIN: ()
}

CHORD_TYPES = {
    KeyType.MAJOR: (0, 4, 7),
    KeyType.MINOR: (0, 3, 7),
    KeyType.AUGMENTED: (0, 4, 8),
    KeyType.DIMINISHED: (0, 3, 6),
    KeyType.DOMINANT: (0, 4, 7, 10),
    KeyType.HALFDIM: (0, 3, 6, 10),
    KeyType.MAJMIN: (0, 3, 7, 11),
    KeyType.SUS2: (0, 2, 7),
    KeyType.SUS4: (0, 5, 7),
    KeyType.MAJ6: (0, 4, 7, 9),
    KeyType.MIN6: (0, 3, 7, 9),
    KeyType.MAJ7: (0, 4, 7, 11),
    KeyType.MIN7: (0, 3, 7, 10),
    KeyType.AUG7: (0, 4, 8, 10),
    KeyType.DIM7: (0, 3, 6, 9),
    KeyType.MAJ9: (0, 4, 7, 11, 2),         # NOTE: 1 note wraps to the next octave
    KeyType.MIN9: (0, 3, 7, 10, 2),         # NOTE: 1 note wraps to the next octave
    KeyType.DOM9: (0, 4, 7, 10, 2),         # NOTE: 1 note wraps to the next octave
    KeyType.MIN11: (0, 3, 7, 10, 2, 5),     # NOTE: 2 notes wrap to the next octave
    KeyType.DOM13: (0, 4, 7, 10, 2, 5, 9),  # NOTE: 3 notes wrap to the next octave
    KeyType.UNSET: ()
}

# =============================================================================


def get_pitch_val(pitch, octave=-1, alt=0):
    """
    :param pitch: [String] A single character representing the root pitch
    :param octave: [Integer] A numerical representation of the octave at which a pitch occurs
    :param alt: [Integer] Representation of a sharp or flat on a notes pitch
    :return: [Integer] a numerical representation of the pitch value in the range [0 - 11]
    """
    increase = (octave + 1) * 12
    offset = alt
    if pitch == 'C':
        offset += 0
    elif pitch == 'D':
        offset += 2
    elif pitch == 'E':
        offset += 4
    elif pitch == 'F':
        offset += 5
    elif pitch == 'G':
        offset += 7
    elif pitch == 'A':
        offset += 9
    elif pitch == 'B':
        offset += 11
    return int(increase + (offset % 12))


def assign_dur_label(num, denom):
    frac = float(num) / float(denom)
    if frac == 2.0:
        return Duration.BRV
    elif frac == 1.0:
        return Duration.WHL
    elif frac == 0.5:
        return Duration.HLF
    elif frac == 0.375:
        return Duration.DQTR
    elif frac == 0.25:
        return Duration.QTR
    elif frac == 0.1875:
        return Duration.DEGT
    elif frac == 0.125:
        return Duration.EGT
    elif frac == 0.09375:
        return Duration.DSXT
    elif frac == 0.0625:
        return Duration.SXT
    elif frac == 0.046875:
        return Duration.DTSD
    elif frac == 0.03125:
        return Duration.TSD
    elif frac == 0.015625:
        return Duration.SXF
    else:
        # NOTE: This allows Unrecognized dur values to be returned from the function
        return frac


def determine_duration(d_label):
    if d_label == 'breve':
        return Duration.BRV
    elif d_label == "whole":
        return Duration.WHL
    elif d_label == "half":
        return Duration.HLF
    elif d_label == "quarter":
        return Duration.QTR
    elif d_label == "eighth":
        return Duration.EGT
    elif d_label == "16th":
        return Duration.SXT
    elif d_label == "32nd":
        return Duration.TSD
    elif d_label == "64th":
        return Duration.SXF
    else:
        raise ValueError("Duration value not found for {0}".format(d_label))


def get_key_type(identifier):
    if identifier == "major":
        return KeyType.MAJOR
    elif identifier == "minor":
        return KeyType.MINOR
    elif identifier == "major-minor":
        return KeyType.MAJMIN
    elif identifier == "augmented":
        return KeyType.AUGMENTED
    elif identifier == "diminished":
        return KeyType.DIMINISHED
    elif identifier == "dominant":
        return KeyType.DOMINANT
    elif identifier == "half-diminished":
        return KeyType.HALFDIM
    elif identifier == "suspended-fourth":
        return KeyType.SUS4
    elif identifier == "major-sixth":
        return KeyType.MAJ6
    elif identifier == "minor-sixth":
        return KeyType.MIN6
    elif identifier == "major-seventh":
        return KeyType.MAJ7
    elif identifier == "minor-seventh":
        return KeyType.MIN7
    elif identifier == "augmented-seventh":
        return KeyType.AUG7
    elif identifier == "diminished-seventh":
        return KeyType.DIM7
    elif identifier == "major-ninth":
        return KeyType.MAJ9
    elif identifier == "minor-ninth":
        return KeyType.MIN9
    elif identifier == "dominant-ninth":
        return KeyType.DOM9
    elif identifier == "minor-11th":
        return KeyType.MIN11
    elif identifier == "dominant-13th":
        return KeyType.DOM13
    elif identifier == "suspended-second":
        return KeyType.SUS2
    elif identifier == "none":
        return KeyType.UNSET
    else:
        raise ValueError("Key type value not found for {0}".format(identifier))


def get_bpm(scale, base):
    if scale == "quarter":
        return int(base / 4)
    elif scale == "half":
        return int(base / 2)
    else:
        print("Unidentified beat-scale --> {0}".format(scale))
        return base


def get_key_root(fifths, mode):
    return (fifths + (3 * mode)) % 12


def pitch_to_name(pitch):
    if pitch == 0:
        return "C"
    elif pitch == 1:
        return "C#"
    elif pitch == 2:
        return "D"
    elif pitch == 3:
        return "Eb"
    elif pitch == 4:
        return "E"
    elif pitch == 5:
        return "F"
    elif pitch == 6:
        return "F#"
    elif pitch == 7:
        return "G"
    elif pitch == 8:
        return "Ab"
    elif pitch == 9:
        return "A"
    elif pitch == 10:
        return "Bb"
    elif pitch == 11:
        return "B"
    else:
        return "NONE"
        # raise ValueError("Out of bounds key root of value {}".format(pitch))


def name_to_pitch(name):
    if "C" in name:
        root = 0
    if "D" in name:
        root = 2
    if "E" in name:
        root = 4
    if "F" in name:
        root = 5
    if "G" in name:
        root = 7
    if "Ab" in name:
        root = 8
    if "A" in name:
        root = 9
    if "B" in name:
        root = 11

    if "b" in name:
        root -= 1
    elif "#" in name:
        root += 1

    return root


def key_to_name(key):
    (root, mode) = key
    if root == 0:
        result = "C"
    elif root == 1:
        result = "C#"
    elif root == 2:
        result = "D"
    elif root == 3:
        result = "Eb"
    elif root == 4:
        result = "E"
    elif root == 5:
        result = "F"
    elif root == 6:
        result = "F#"
    elif root == 7:
        result = "G"
    elif root == 8:
        result = "Ab"
    elif root == 9:
        result = "A"
    elif root == 10:
        result = "Bb"
    elif root == 11:
        result = "B"
    else:
        raise ValueError("Out of bounds key root of value {}".format(root))

    if mode == KeyType.MAJOR:
        result += "Maj"
    elif mode == KeyType.MINOR:
        result += "min"
    elif mode == -1:
        result += "?"
    else:
        raise ValueError("Unsupported Key mode of value {}".format(mode))

    return result


def name_to_key(name):
    root, mode = -1, -1

    if "min" in name:
        mode = 1
    elif "Maj" in name:
        mode = 0

    if "C" in name:
        root = 0
    if "D" in name:
        root = 2
    if "E" in name:
        root = 4
    if "F" in name:
        root = 5
    if "G" in name:
        root = 7
    if "Ab" in name:
        root = 8
    if "A" in name:
        root = 9
    if "B" in name:
        root = 11

    if "b" in name:
        root -= 1
    elif "#" in name:
        root += 1

    return (root, mode)


def num_to_pitch(num):
    return "RST" if num == -1 else PITCHES[int(num % 12)]


def num_to_key(num, mtype):
    return PITCHES[int(num % 12)] + KEYS[mtype]


# def seqToTupleList(seq):
#     result = list()
#     data = seq.trees
#
#     for eci_obj in data:
#         onset = (eci_obj.onset.measure, eci_obj.onset.beat)
#         if isinstance(eci_obj, eci.Note):
#             pitch = eci_obj.pitch.midiValue()
#             dur = eci_obj.dur.beat
#             result.append((MusicElement.NOTE, pitch, dur, onset))
#         elif isinstance(eci_obj, eci.Rest):
#             dur = eci_obj.dur.beat
#             result.append((MusicElement.REST, -1, dur, onset))
#         else:
#             print("Unknown ECI object while creating tuple list")
#             print(eci_obj)
#
#     return result


def determine_pitch_set(chord):
    """
    Given a chord, return a set of pitch values based upon whether the chord is major,
    minor, dominant, diminished, etc.

    TODO: rewrite to rely upon the data of chord scale given in XML file
    """

    def pitch_difference(lower, higher):
        """
        Return the adjusted difference between a higher and lower pitch
        """
        return (((higher + 12) - lower) % 12)

    if len(chord) >= 3:
        first = pitch_difference(chord[0], chord[1])
        second = pitch_difference(chord[1], chord[2])
        if len(chord) == 3:
            if first == 4 and second == 3:
                return MAJOR_VALUES
            elif first == 3 and second == 4:
                return MINOR_VALUES
            elif first == 4 and second == 4:
                return AUGMENTED_VALUES
            elif first == 3 and second == 3:
                return DIMINISHED_VALUES
        else:
            third = pitch_difference(chord[2], chord[3])
            if first == 3 and second == 3 and third == 3:
                return DIMINISHED_VALUES
            elif first == 3 and second == 3 and third == 4:
                return HALF_DIMINISHED_VALUES
            elif first == 3 and second == 4 and third == 3:
                return MINOR_VALUES
            elif first == 3 and second == 4 and third == 4:
                return MINOR_MAJOR_VALUES
            elif first == 4 and second == 4 and third == 2:
                return AUGMENTED_VALUES
            elif first == 4 and second == 3 and third == 3:
                return DOMINANT_VALUES
            elif first == 4 and second == 3 and third == 4:
                return MAJOR_VALUES
            elif first == 4 and second == 4 and third == 3:
                return AUGMENTED_MAJOR_VALUES
    return None
