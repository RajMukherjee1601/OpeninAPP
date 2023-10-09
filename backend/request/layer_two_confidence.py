import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)

import json

from request.chat_completion import completion_api_call
from scripts.stitchers.confidence_score import ConfidenceScore


class ConfidenceLayerTwo:
    @staticmethod
    def confidence_score(layer_one_response) -> dict:
        """It takes user's english text and convered to hindi text by all models and gives them confidence score

        Returns:
        dict: Confidence score
        """

        context_confidence_score = ConfidenceScore.stitch_confidence_score_context()
        context_confidence_score += "[User Input]->\n[Query]: " + layer_one_response["user_input"] + "\n"

        if layer_one_response["lstm"]:
            context_confidence_score += "   [one]: " + layer_one_response["lstm"] + "\n"

        if layer_one_response["gpt"]:
            context_confidence_score += "   [two]: " + layer_one_response["gpt"] + "\n"

        if layer_one_response["google"]:
            context_confidence_score += "   [three]: " + layer_one_response["google"] + "\n\n"

        context_confidence_score += "[confidence score]:"

        confidence_score_response = completion_api_call(context_confidence_score)

        try:
            confidence_score = json.loads(confidence_score_response.replace("'", '"'))

        except:
            return confidence_score_response

        return confidence_score
