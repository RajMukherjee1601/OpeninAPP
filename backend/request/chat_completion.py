import openai
from cred.Cred import Cred


def completion_api_call(context: str) -> str:
    """It makes API call to OpenAI's ChatGPT

    Args:
        context (str): context

    Returns:
        str: output based on context
    """
    cred = Cred()
    details = cred.get_details()
    openai.api_key = details["api_key"]
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613", messages=[{"role": "user", "content": context}]
        )
        ans = completion.choices[0].message.content

    except:
        ans = "GPT is not working. Please Check."

    return ans
