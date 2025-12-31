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
        font-size: 32px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .audio-container {
        margin-top: 15px;
    }
    .audio-text {
        color: #7f8c8d;
        font-size: 14px;
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
    Back side: Show definition, context sentences, notes, and image.
    Modern, readable design optimized for B2 level learning.
    """
    styles = """
    <style>
    .card-back {
        max-width: 90%;
        margin: auto;
        padding: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .definition-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #3498db;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    .definition-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #7f8c8d;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .definition-text {
        font-size: 18px;
        line-height: 1.6;
        color: #2c3e50;
    }
    .context-section {
        margin-bottom: 20px;
    }
    .context-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #7f8c8d;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .context-sentence {
        font-size: 16px;
        line-height: 1.7;
        color: #34495e;
        margin-bottom: 10px;
        padding-left: 15px;
        border-left: 2px solid #e0e0e0;
    }
    .notes-section {
        background-color: #fff9e6;
        padding: 12px 15px;
        border-left: 4px solid #f39c12;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    .notes-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #d68910;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .notes-text {
        font-size: 14px;
        line-height: 1.5;
        color: #7d6608;
    }
    .image-section {
        text-align: center;
        margin-top: 25px;
    }
    .card-image {
        max-width: 100%;
        max-height: 300px;
        height: auto;
        width: auto;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .footer {
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #e0e0e0;
        text-align: center;
    }
    .dictionary-link {
        color: #3498db;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
    }
    .dictionary-link:hover {
        text-decoration: underline;
    }
    </style>
    """

    # Build context sentences HTML
    context_html = ""
    for sentence in card_data.context_sentences:
        context_html += f'<div class="context-sentence">• {sentence}</div>\n'

    back_content = styles + f"""
    <div class="card-back">
        <!-- Definition -->
        <div class="definition-section">
            <div class="definition-label">Definition</div>
            <div class="definition-text">{card_data.definition}</div>
        </div>

        <!-- Context Sentences -->
        <div class="context-section">
            <div class="context-label">Examples</div>
            {context_html}
        </div>

        <!-- Notes -->
        <div class="notes-section">
            <div class="notes-label">💡 Notes</div>
            <div class="notes-text">{card_data.notes}</div>
        </div>

        <!-- Image -->
        <div class="image-section">
            <img class="card-image" src="{os.path.basename(card_data.image_path)}">
        </div>
    """

    # Add dictionary link if available
    if card_data.dictionary_url:
        back_content += f"""
        <div class="footer">
            <a class="dictionary-link" href="{card_data.dictionary_url}" target="_blank">📖 View in Dictionary</a>
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
