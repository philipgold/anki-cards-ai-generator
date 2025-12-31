import logging
import time

from generator.api_calls import openai_image, openai_text, openai_audio, openai_image_prompt, replicate_image
from generator.dictionaries import dictionaries
from generator.config import Config, OPENAI, REPLICATE
from generator.entities import WordWithContext, CardRawDataV1, CardRawDataV2, serialize_to_json
from generator.input.file_operations import save_text, generate_image_path, generate_card_data_path, download_and_save_image, generate_audio_path
from generator.input.confirm import confirm_action

def generate_text_and_image(input_words: list[WordWithContext]) -> dict[WordWithContext, CardRawDataV2]:
    words_total = len(input_words)
    words_remaining = words_total

    logging.info(f"Starting generation of text and images for {words_total} words {list(map(lambda entry: entry.word, input_words))}")
    words_cards: dict[WordWithContext, CardRawDataV2] = {}

    for word_with_context in input_words:
        try:
            card_raw = create_card_for_word_v2(word_with_context)
            words_cards[word_with_context] = card_raw
            logging.info(f"Word [{word_with_context.word}] processed")
        except Exception as e:
            logging.error(f"Failed to process word [{word_with_context.word}] due to [{e}]")
            abort = confirm_action("Do you want to abort processing? If no, the processing will be resumed and this card will be skipped")
            if abort:
                raise Exception(f"Aborting processing after error: [{e}]")
            else:
                logging.warning(f"Word [{word_with_context.word}] will be skipped")
        words_remaining -= 1
        if words_remaining > 0:
            wait_after_word_processing()
    return words_cards


def create_card_for_word(word_with_context) -> CardRawDataV1:
    card_text = openai_text.chat_generate_text(word_with_context)
    logging.info("Card text is created")

    image_prompt = openai_image_prompt.chat_generate_dalle_prompt(word_with_context, card_text)
    image_url = get_image_url_depending_on_image_generation_mode(image_prompt)

    logging.info("Card Image is created")
    logging.info(f"Image url: {image_url}")

    image_path = generate_image_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    download_and_save_image(image_url, image_path)
    logging.info(f"Card image is saved as [{image_path}]")

    audio_path = generate_audio_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    openai_audio.chat_generate_and_save_audio(word_with_context.word, audio_path)
    logging.info(f"Card audio is saved as [{audio_path}]")

    dictionary_url = dictionaries.create_dictionary_url_if_website_exists(word_with_context.word)
    if dictionary_url:
        logging.info(f"Dictionary url is created")
    else:
        logging.warning(f"Dictionary url is not created")

    card_raw: CardRawDataV1 = CardRawDataV1(word=word_with_context.word, card_text=card_text,
                                            image_prompt=image_prompt, image_url=image_url, image_path=image_path,
                                            audio_path=audio_path,
                                            dictionary_url=dictionary_url)
    card_data_path = generate_card_data_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    save_text(serialize_to_json(card_raw), card_data_path)
    logging.info(f"Card data is saved as [{card_data_path}]")
    return card_raw


def create_card_for_word_v2(word_with_context: WordWithContext) -> CardRawDataV2:
    """
    Create a vocabulary card using structured JSON output (v2 format).
    Returns CardRawDataV2 with definition, context_sentences, and notes.
    """
    # Generate structured card content (definition, context_sentences, notes)
    structured_content = openai_text.chat_generate_structured_text(word_with_context)
    logging.info("Structured card content created")

    # Generate image prompt based on definition and context
    image_prompt = openai_image_prompt.chat_generate_dalle_prompt(
        word_with_context,
        structured_content["definition"]
    )
    image_url = get_image_url_depending_on_image_generation_mode(image_prompt)
    logging.info("Card Image is created")
    logging.info(f"Image url: {image_url}")

    # Download and save image
    image_path = generate_image_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    download_and_save_image(image_url, image_path)
    logging.info(f"Card image is saved as [{image_path}]")

    # Generate and save audio
    audio_path = generate_audio_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    openai_audio.chat_generate_and_save_audio(word_with_context.word, audio_path)
    logging.info(f"Card audio is saved as [{audio_path}]")

    # Get dictionary URL
    dictionary_url = dictionaries.create_dictionary_url_if_website_exists(word_with_context.word)
    if dictionary_url:
        logging.info(f"Dictionary url is created")
    else:
        logging.warning(f"Dictionary url is not created")

    # Create CardRawDataV2 object
    card_raw: CardRawDataV2 = CardRawDataV2(
        word=word_with_context.word,
        definition=structured_content["definition"],
        russian_translation=structured_content["russian_translation"],
        context_sentences=structured_content["context_sentences"],
        notes=structured_content["notes"],
        image_prompt=image_prompt,
        image_url=image_url,
        image_path=image_path,
        audio_path=audio_path,
        russian_speaker_tips=structured_content.get("russian_speaker_tips"),
        dictionary_url=dictionary_url
    )

    # Save card data
    card_data_path = generate_card_data_path(Config.PROCESSING_DIRECTORY_PATH, word_with_context)
    save_text(serialize_to_json(card_raw), card_data_path)
    logging.info(f"Card data is saved as [{card_data_path}]")

    return card_raw


def get_image_url_depending_on_image_generation_mode(image_prompt):
    if Config.IMAGE_GENERATION_MODE == OPENAI:
        return openai_image.chat_generate_image(image_prompt)
    elif Config.IMAGE_GENERATION_MODE == REPLICATE:
        return replicate_image.replicate_generate_image(image_prompt)
    else:
        raise Exception(f"Unsupported image generation mode: [{Config.IMAGE_GENERATION_MODE}]")


def wait_after_word_processing():
    sleep_seconds = Config.SECONDS_WAIT_BETWEEN_DALLE_CALLS
    logging.info(f"Waiting [{sleep_seconds}] seconds after word processing (API RPM)")
    time.sleep(sleep_seconds)
