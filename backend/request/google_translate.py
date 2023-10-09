from googletrans import Translator


def translator_api_call(user_prompt: str) -> str:
    """It makes API call to google translator api

    Args:
        user_prompt (str): user_prompt

    Returns:
        str: output based on user_prompt
    """
    translator = Translator()
    translated_text = translator.translate(user_prompt, src="en", dest="hi")
    return translated_text.text
