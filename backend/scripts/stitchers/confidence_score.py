import json

from scripts.schema import Confidence_Score


class ConfidenceScore:
    @classmethod
    def stitch_confidence_score_context(cls) -> str:
        """It makes context for Confidence_Score

        Returns:
            str: context for Confidence_Score
        """
        confidence_score_json = cls.get_confidence_score_json()
        context = confidence_score_json.role + "\n"
        for description in confidence_score_json.description:
            context += description + "\n"

        context += "[Instructions]: " + confidence_score_json.instructions + "\n\n" + "[Examples]->\n\n"

        for example in confidence_score_json.examples:
            context += "[English Query]: " + example.input.query + "\n" "[Hindi Translations]:\n"
            if example.input.one:
                context += "    [one]: " + example.input.one + "\n"

            if example.input.two:
                context += "    [two]: " + example.input.two + "\n"

            if example.input.three:
                context += "    [three]: " + example.input.three + "\n"

            context += "Confidence Score]: " + str(example.confidence_score) + "\n\n"

        return context

    @staticmethod
    def get_confidence_score_json() -> object:
        """It makes schema for english_to_hindi.json

        Returns:
            object: schema
        """
        file = open("backend\scripts\prompts\confidence_score.json", "r", encoding="utf-8")
        confidence_score_json = Confidence_Score.model_validate(json.load(file))
        file.close()

        return confidence_score_json
