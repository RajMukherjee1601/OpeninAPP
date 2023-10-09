import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "0"  # Turns off, caching warning in LSTM model

import time

from request.layer_one_models import ModelLayerOne
from request.layer_two_confidence import ConfidenceLayerTwo


class Requests:
    start_time: time
    confidence_score: str
    layer_one: object

    def __init__(self, user_request):

        self.start_time = time.time()
        self.time_taken_gpt = 0
        self.time_taken_google_trans = 0
        self.layer_one = ModelLayerOne(user_request)

    def handler(self) -> str:
        """It takes user's english text and converts to hindi text

        Returns:
        str: Best converted output
        """

        layer_one_response = self.layer_one.models()
        if not layer_one_response["is_internet"]:
            return layer_one_response["lstm"]

        confidence_score = ConfidenceLayerTwo.confidence_score(layer_one_response)

        self.print_for_BE(layer_one_response, confidence_score)

        if type(confidence_score) == dict:
            if (
                confidence_score["two"] >= confidence_score["one"]
                and confidence_score["two"] >= confidence_score["three"]
            ):
                return layer_one_response["gpt"]

            elif (
                confidence_score["one"] >= confidence_score["two"]
                and confidence_score["one"] >= confidence_score["three"]
            ):
                return layer_one_response["lstm"]

            elif (
                confidence_score["three"] >= confidence_score["one"]
                and confidence_score["three"] >= confidence_score["two"]
            ):
                return layer_one_response["google"]

            return "Something is wrong"

        return layer_one_response["google"]

    def print_for_BE(self, layer_one_response: dict, confidence_score: dict):

        print(
            "\n\n\n----------------------------------------------------------------------------\n\n"
            + f"[Query]: {layer_one_response['user_input']} \n\n"
            + "[LSTM Model Response]: "
            + str(layer_one_response["lstm"])
            + f"\n[Time Taken by LSTM Model]: {round(layer_one_response['time_gpt'],3)} Seconds\n\n"
            + "[ChatGPT Response]: "
            + str(layer_one_response["gpt"])
            + f"\n[Time Taken by GPT]: {round(layer_one_response['time_gpt'],3)} Seconds\n"
            + "\n[Google API Response]: "
            + str(layer_one_response["google"])
            + f"\n[Time Taken by Google Translator]: {round(layer_one_response['time_google'],3)} Seconds\n\n"
            + f"[Confidence Score]: {confidence_score}"
            + f"\n\n[Total Time Taken]: {round(time.time() - self.start_time, 3)} Seconds"
            + "\n\n----------------------------------------------------------------------------\n\n\n"
        )

        with open("testing_result.txt", "w", encoding="utf-8") as file:
            file.write(
                "----------------------------------------------------------------------------\n\n"
                + f"[Query]: {layer_one_response['user_input']} \n\n"
                + "[LSTM Model Response]: "
                + str(layer_one_response["lstm"])
                + f"\n[Time Taken by LSTM Model]: {round(layer_one_response['time_gpt'],3)} Seconds\n\n"
                + "[ChatGPT Response]: "
                + str(layer_one_response["gpt"])
                + f"\n[Time Taken by GPT]: {round(layer_one_response['time_gpt'],3)} Seconds\n"
                + "\n[Google API Response]: "
                + str(layer_one_response["google"])
                + f"\n[Time Taken by Google Translator]: {round(layer_one_response['time_google'],3)} Seconds\n\n"
                + f"[Confidence Score]: {confidence_score}"
                + f"\n\n[Total Time Taken]: {round(time.time() - self.start_time, 3)} Seconds"
                + "\n\n----------------------------------------------------------------------------"
            )
