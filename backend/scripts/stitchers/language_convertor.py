import json

from scripts.schema import English_To_Hindi_Convertor


class LanguageConvertor:
    @classmethod
    def stitch_language_convertor_context(cls) -> str:
        """It makes context for language convertor

        Returns:
            str: context for language convertor
        """
        english_to_hindi_json = cls.get_english_to_hindi_json()
        context = english_to_hindi_json.role + "\n"

        for description in english_to_hindi_json.description:
            context += description + "\n"

        context += "[Instructions]: " + english_to_hindi_json.instructions + "\n\n" + "[Examples]->\n\n"

        for example in english_to_hindi_json.examples:
            context += "[Input]: " + example.user_prompt + "\n"
            context += "[Output]:" + example.completion + "\n"

        context += "\n[Query]: "

        return context

    @staticmethod
    def get_english_to_hindi_json() -> object:
        """It makes schema for english_to_hindi.json

        Returns:
            object: schema
        """
        file = open("backend\scripts\prompts\english_to_hindi.json", "r", encoding="utf-8")
        english_to_hindi_json = English_To_Hindi_Convertor.model_validate(json.load(file))
        file.close()

        return english_to_hindi_json
