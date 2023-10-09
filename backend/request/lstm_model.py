from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


def lstm_model(user_prompt: str) -> str:
    """It uses our pre-trained model to covert english to hindi

    Args:
        user_prompt (str): user_prompt

    Returns:
        str: output based on user_prompt
    """

    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

    tokenizer.src_lang = "en"
    encoded_hi = tokenizer(user_prompt, return_tensors="pt")
    generated_tokens = model.generate(**encoded_hi, forced_bos_token_id=tokenizer.get_lang_id("hi"))

    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
