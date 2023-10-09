import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)

from scripts.stitchers.confidence_score import ConfidenceScore
from scripts.stitchers.language_convertor import LanguageConvertor


def main(user_prompt, type):
    print("\n---------------------------------------------------------------------------\n")

    if type == "conf":
        print(ConfidenceScore.stitch_confidence_score_context(), user_prompt, "\n")
    else:
        print(LanguageConvertor.stitch_language_convertor_context(), user_prompt, "\n")
    print("\n---------------------------------------------------------------------------\n")


if __name__ == "__main__":

    type = "conf"  # Conf or Lang
    user_prompt = "Alola Malola"
    main(user_prompt, type)
