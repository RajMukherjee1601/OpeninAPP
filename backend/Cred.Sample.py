"""
Make a folder name 'cred' and then make a file name 'Cred.py' and copy the following code and add your api key here
"""


class Cred:
    @staticmethod
    def get_details() -> dict:
        """It returns api keys for openai and palm

        Returns:
            str: api key
        """
        details = {"api_key": "<api-key>"}
        return details
