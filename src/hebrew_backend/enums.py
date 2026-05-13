from enum import StrEnum


class PartOfSpeech(StrEnum):
    VERB = "verb"
    NOUN = "noun"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PREPOSITION = "preposition"
    PRONOUN = "pronoun"
    OTHER = "other"


class Gender(StrEnum):
    MASCULINE = "masculine"
    FEMININE = "feminine"


class GrammaticalNumber(StrEnum):
    SINGULAR = "singular"
    PLURAL = "plural"
    DUAL = "dual"


class Level(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"


class VocabStatus(StrEnum):
    LEARNING = "learning"
    KNOWN = "known"
    MASTERED = "mastered"


class Binyan(StrEnum):
    PAAL = "פעל"
    PIEL = "פיעל"
    HIFIL = "הפעיל"
    HITPAEL = "התפעל"
    NIFAL = "נפעל"
    PUAL = "פועל"
    HUFAL = "הופעל"
