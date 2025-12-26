#!/bin/bash

# Start Anki (using macOS command, change if using different OS)
open -a Anki

# Wait a few seconds for Anki to fully start
sleep 3

python3 -m generator.read-generate-import ./data/input_words.csv ./processing \
          --language="english" \
          --level="B2" \
          --deck_name="my_amazing_deck" \
          --anki_media_directory_path="/Users/pg/Library/Application Support/Anki2/User 1/collection.media" \
          --card_model="Basic (type in the answer)" \
          --image_generation_mode="openai"