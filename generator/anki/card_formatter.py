import os

from . import anki_operations
from ..config import Config
from ..entities import CardRawDataV2


def get_front_html(card_data: CardRawDataV2) -> str:
    """
    Front side: Display the term/word with audio button.
    Simple, clean design focused on the vocabulary term.
    """
    styles = """
    <style>
    .card-front {
        max-width: 90%;
        margin: auto;
        padding: 40px 20px;
        text-align: center;
    }
    .term {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 42px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .audio-container {
        margin-top: 15px;
    }
    .audio-text {
        color: #7f8c8d;
        font-size: 20px;
        font-weight: 500;
        margin-right: 8px;
    }
    </style>
    """

    front_content = styles + f"""
    <div class="card-front">
        <div class="term">{card_data.word}</div>
        <div class="audio-container">
            <span class="audio-text">🔊 Pronunciation</span>
            <span>[sound:{os.path.basename(card_data.audio_path)}]</span>
        </div>
    </div>
    """
    return front_content


def get_back_html(card_data: CardRawDataV2) -> str:
    """
    Back side: Show image at top, then definition, context sentences, notes.
    Uses inline styles for better Anki compatibility.
    """
    # Build context sentences HTML
    context_html = ""
    for sentence in card_data.context_sentences:
        context_html += f'<div style="font-size: 20px; line-height: 1.7; color: #34495e; margin-bottom: 12px; padding-left: 15px; border-left: 3px solid #e0e0e0;">• {sentence}</div>\n'

    back_content = f"""
    <div style="max-width: 95%; margin: auto; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <!-- Image at top -->
        <div style="text-align: center; margin-bottom: 20px;">
            <img style="max-width: 100%; max-height: 300px; height: auto; width: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" src="{os.path.basename(card_data.image_path)}">
        </div>

        <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">

        <!-- Definition -->
        <div style="background-color: #f8f9fa; padding: 18px; border-left: 5px solid #3498db; margin-bottom: 20px; border-radius: 4px;">
            <div style="font-size: 15px; text-transform: uppercase; color: #7f8c8d; font-weight: 600; margin-bottom: 10px;">Definition</div>
            <div style="font-size: 22px; line-height: 1.6; color: #2c3e50;">{card_data.definition}</div>
        </div>

        <!-- Russian Translation -->
        <div style="background-color: #e8f4fd; padding: 15px 18px; border-left: 5px solid #2980b9; margin-bottom: 20px; border-radius: 4px;">
            <div style="font-size: 14px; text-transform: uppercase; color: #2471a3; font-weight: 600; margin-bottom: 8px;">🇷🇺 Перевод</div>
            <div style="font-size: 20px; line-height: 1.5; color: #1a5276; font-style: italic;">{card_data.russian_translation}</div>
        </div>

        <!-- Context Sentences -->
        <div style="margin-bottom: 20px;">
            <div style="font-size: 15px; text-transform: uppercase; color: #7f8c8d; font-weight: 600; margin-bottom: 12px;">Examples</div>
            {context_html}
        </div>

        <!-- Notes -->
        <div style="background-color: #fff9e6; padding: 15px 18px; border-left: 5px solid #f39c12; margin-bottom: 20px; border-radius: 4px;">
            <div style="font-size: 14px; text-transform: uppercase; color: #d68910; font-weight: 600; margin-bottom: 8px;">💡 Notes</div>
            <div style="font-size: 18px; line-height: 1.6; color: #7d6608;">{card_data.notes}</div>
        </div>
    """

    # Add Russian speaker tips if available
    if card_data.russian_speaker_tips:
        back_content += f"""
        <div style="background-color: #fdecea; padding: 15px 18px; border-left: 5px solid #e74c3c; margin-bottom: 20px; border-radius: 4px;">
            <div style="font-size: 14px; text-transform: uppercase; color: #c0392b; font-weight: 600; margin-bottom: 8px;">⚠️ Tips for Russian Speakers</div>
            <div style="font-size: 18px; line-height: 1.6; color: #922b21;">{card_data.russian_speaker_tips}</div>
        </div>
        """

    # Add dictionary link if available
    if card_data.dictionary_url:
        back_content += f"""
        <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #e0e0e0; text-align: center;">
            <a style="color: #3498db; text-decoration: none; font-size: 20px; font-weight: 500;" href="{card_data.dictionary_url}" target="_blank">📖 View in Dictionary</a>
        </div>
        """

    back_content += """
    </div>
    """
    return back_content


def format(card_data: CardRawDataV2, deck_name: str):
    """
    Format card data for Anki import using v2 structure.
    Front: Term with audio
    Back: Definition, examples, notes, and image
    """
    front_content = get_front_html(card_data)
    back_content = get_back_html(card_data)

    return {
        "deckName": deck_name,
        "modelName": Config.CARD_MODEL,
        "fields": {
            "Front": front_content,
            "Back": back_content
        },
        "options": {
            "allowDuplicate": True,
            "duplicateScope": "deck"
        },
        "tags": [anki_operations.word_to_tag(card_data.word), "ai-generated", "v2"]
    }
