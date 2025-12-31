import json
import logging
from openai import OpenAI

from ..config import Config
from ..entities import WordWithContext
from .text_prompt_by_language import prompt_by_language



def chat_generate_text(word_with_context: WordWithContext) -> str:
    logging.info(f"ChatGPT card text: processing word [{word_with_context.word}] with context [{word_with_context.context}] in language [{Config.LANGUAGE}]")

    system_prompt = prompt_by_language.get_system_prompt_by_language()

    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"WORD: [{word_with_context.word}]; CONTEXT: [{word_with_context.context}]"},
    ]

    client = OpenAI(
        api_key=Config.OPENAI_API_KEY
    )

    logging.debug(f"ChatGPT card generation messages {messages}")

    response = client.chat.completions.create(
        # input prompt
        messages=messages,
        # model parameters
        model="gpt-4o",
        temperature=0.2,  # keep low for conservative answers
        max_tokens=512,
        n=1,
        presence_penalty=0,
        frequency_penalty=0.1,
    )

    generated_text = response.choices[0].message.content
    logging.debug(f"ChatGPT generated card text for word {word_with_context.word}")
    logging.debug(f"ChatGPT card text: {generated_text}")
    return generated_text


def chat_generate_structured_text(word_with_context: WordWithContext) -> dict:
    """
    Generate structured vocabulary card data using OpenAI with JSON output.
    Returns a dictionary with: definition, context_sentences, notes
    """
    logging.info(f"ChatGPT structured card generation: processing word [{word_with_context.word}] with context [{word_with_context.context}] in language [{Config.LANGUAGE}]")

    system_prompt = prompt_by_language.get_system_prompt_by_language()

    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"WORD: [{word_with_context.word}]; CONTEXT: [{word_with_context.context}]"},
    ]

    client = OpenAI(
        api_key=Config.OPENAI_API_KEY
    )

    logging.debug(f"ChatGPT structured card generation messages: {messages}")

    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        temperature=0.2,
        max_tokens=512,
        n=1,
        presence_penalty=0,
        frequency_penalty=0.1,
        response_format={"type": "json_object"}  # Enable structured JSON output
    )

    generated_text = response.choices[0].message.content
    logging.debug(f"ChatGPT raw JSON response: {generated_text}")

    # Parse JSON response
    try:
        structured_data = json.loads(generated_text)

        # Validate required fields
        required_fields = ["definition", "russian_translation", "context_sentences", "notes"]
        for field in required_fields:
            if field not in structured_data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(structured_data["context_sentences"], list):
            raise ValueError("context_sentences must be a list")

        if len(structured_data["context_sentences"]) < 2:
            raise ValueError("At least 2 context sentences required")

        # Ensure russian_speaker_tips exists (can be null)
        if "russian_speaker_tips" not in structured_data:
            structured_data["russian_speaker_tips"] = None

        # Handle cloze_sentences if present (optional field)
        if "cloze_sentences" in structured_data:
            if not isinstance(structured_data["cloze_sentences"], list):
                raise ValueError("cloze_sentences must be a list")
            # Validate each cloze sentence has required fields
            for i, cloze in enumerate(structured_data["cloze_sentences"]):
                if not isinstance(cloze, dict):
                    raise ValueError(f"cloze_sentences[{i}] must be an object")
                if "sentence" not in cloze or "hint" not in cloze:
                    raise ValueError(f"cloze_sentences[{i}] must have 'sentence' and 'hint' fields")
        else:
            structured_data["cloze_sentences"] = None

        logging.info(f"Successfully generated structured card for word [{word_with_context.word}]")
        return structured_data

    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response for word [{word_with_context.word}]: {e}")
        logging.error(f"Raw response: {generated_text}")
        raise ValueError(f"Invalid JSON response from OpenAI: {e}")
    except ValueError as e:
        logging.error(f"Validation error for word [{word_with_context.word}]: {e}")
        raise
