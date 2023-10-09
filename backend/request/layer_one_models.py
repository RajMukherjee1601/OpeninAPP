import time

import requests
from request.chat_completion import completion_api_call
from request.google_translate import translator_api_call
from request.lstm_model import lstm_model
from request.pdf_convertor import pdf_convertor
from scripts.enums import InputType
from scripts.stitchers.language_convertor import LanguageConvertor


class ModelLayerOne:
    user_request: dict
    lstm_response: str
    chatgpt_response: str
    google_trans_response: str
    time_taken_lstm: time
    time_taken_gpt: time
    time_taken_google_trans: time

    def __init__(self, user_request):

        self.user_request = user_request
        self.chatgpt_response = "You are not connected to a network"
        self.google_trans_response = "You are not connected to a network"
        self.time_taken_lstm = 0
        self.time_taken_gpt = 0
        self.time_taken_google_trans = 0

    def models(self) -> dict:
        """It takes user's english text and converts to hindi text

        Returns:
            dict: {
            "google_translator" : google translator response,
            "chatgpt" : chatgpt response
        }
        """

        context_language_convertor = LanguageConvertor.stitch_language_convertor_context()
        if self.user_request["mode"] == InputType.PDF.value:
            user_input = pdf_convertor(self.user_request["user_prompt"])

        else:
            user_input = self.user_request["user_prompt"]

        # ----------------------- LSTM Model Response --------------------

        self.time_taken_lstm = time.perf_counter()
        try:
            context_language_convertor += user_input
            self.lstm_response = lstm_model(user_input)

        except:
            self.lstm_response = None
        self.time_taken_gpt = time.perf_counter() - self.time_taken_lstm

        is_internet = self.is_connected_to_internet()
        if is_internet:

            # ----------------------- ChatGPT Response --------------------
            self.time_taken_gpt = time.perf_counter()
            try:
                context_language_convertor += user_input
                self.chatgpt_response = completion_api_call(context_language_convertor)

            except:
                self.chatgpt_response = None
            self.time_taken_gpt = time.perf_counter() - self.time_taken_gpt

            # ----------------------- Google Translator Response ----------
            self.time_taken_google_trans = time.perf_counter()
            try:
                self.google_trans_response = translator_api_call(user_input)

            except Exception:
                self.google_trans_response = None
            self.time_taken_google_trans = time.perf_counter() - self.time_taken_google_trans

        return {
            "is_internet": is_internet,
            "lstm": self.lstm_response[0],
            "gpt": self.chatgpt_response,
            "google": self.google_trans_response,
            "time_lstm": self.time_taken_lstm,
            "time_gpt": self.time_taken_gpt,
            "time_google": self.time_taken_google_trans,
            "user_input": user_input,
        }

    def is_connected_to_internet(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            return True

        except requests.ConnectionError:
            return False
