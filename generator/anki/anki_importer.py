import json
import logging

from .anki_operations import invoke
from ..anki import card_formatter
from ..config import Config, RECOGNITION, PRODUCTION, BOTH, INCLUDE_CLOZE
from ..entities import CardRawDataV1, CardRawDataV2, WordWithContext
from ..input.confirm import confirm_action
from ..input.file_operations import copy_to_media_directory


def import_card_collection(cards: dict[WordWithContext, CardRawDataV2]):
    for word in cards:
        card_raw_data = cards[word]
        if card_raw_data is None:
            raise ValueError(f"No object for word [{word}]. Data structure: [{json.dumps(cards)}]")

        # Copy media files (only once per word, regardless of card direction)
        copy_to_media_directory(card_raw_data.image_path)
        copy_to_media_directory(card_raw_data.audio_path)

        # Determine which card types to create
        card_types = []
        if Config.CARD_DIRECTION == BOTH:
            card_types = [RECOGNITION, PRODUCTION]
        elif Config.CARD_DIRECTION == PRODUCTION:
            card_types = [PRODUCTION]
        else:
            card_types = [RECOGNITION]

        # Create cards based on direction setting
        for card_type in card_types:
            import_result = format_and_import_card(card_raw_data, card_type)
            if import_result['error']:
                logging.error(f"Error occurred during import of {card_type} card for word [{word.word}]. Import error: [{import_result['error']}]")
                abort = confirm_action("Do you want to abort processing? If no, the processing will be resumed and this card will be skipped")
                if abort:
                    raise Exception(f"Aborting processing after error: [{import_result['error']}]")
                else:
                    continue
            logging.info(f"{card_type.capitalize()} card for word [{word.word}] imported in deck [{Config.DECK_NAME}]")

        # Import cloze cards if enabled
        if Config.INCLUDE_CLOZE and card_raw_data.cloze_sentences:
            import_cloze_cards(card_raw_data, word)


def format_and_import_card(card_data: CardRawDataV2, card_type: str = RECOGNITION):
    note = card_formatter.format(card_data, Config.DECK_NAME, card_type)
    result = invoke('addNote', {'note': note})
    return result


def import_cloze_cards(card_data: CardRawDataV2, word: WordWithContext):
    """Import cloze deletion cards for the given word."""
    cloze_cards = card_formatter.format_cloze_cards(card_data, Config.DECK_NAME)

    for i, cloze_card in enumerate(cloze_cards):
        import_result = invoke('addNote', {'note': cloze_card})
        if import_result['error']:
            logging.error(f"Error importing cloze card {i+1} for word [{word.word}]: {import_result['error']}")
        else:
            logging.info(f"Cloze card {i+1} for word [{word.word}] imported in deck [{Config.DECK_NAME}]")
