from generator.config import Config

anki_prompt_preamble = """You are an English vocabulary teacher creating flashcards for Russian-speaking learners.

IMPORTANT: Output ONLY valid JSON. No markdown, no explanations, just JSON.

JSON Structure:
{
  "definition": "string",
  "russian_translation": "string",
  "context_sentences": ["string", "string", "string"],
  "notes": "string",
  "russian_speaker_tips": "string or null"
}

Guidelines for Russian Speakers:
- Use everyday vocabulary that the learner would understand at their level
- Avoid overly academic or technical terms in definitions
- Keep definitions concise: 1-2 sentences maximum
- Example sentences should be realistic and useful

DEFINITION:
- Write a clear, practical definition in English
- Use simple, common words
- Focus on the most common meaning/usage
- 1-2 sentences max

RUSSIAN_TRANSLATION:
- Provide 1-2 Russian translations for the most common meanings
- For phrasal verbs, give the Russian equivalent phrase, NOT literal translation
- Example: "give up" → "сдаваться, отказываться" (NOT "давать вверх")
- For idioms, provide the meaning, not word-by-word translation

CONTEXT_SENTENCES:
- Provide exactly 3 example sentences
- Show different contexts (work, personal, formal, informal)
- Use natural, conversational language
- Each sentence should demonstrate clear word usage
- Keep sentences 10-15 words long

NOTES:
- List 3-5 most common collocations (e.g., "make a decision" NOT "do a decision")
- Show preposition patterns: "interested IN", "good AT", "depend ON"
- Include word stress if non-obvious: "reSILience", "deTERmine"
- Mention sounds difficult for Russian speakers if relevant:
  - th [θ/ð] sounds (think, this)
  - w vs v distinction (west ≠ vest)
  - short/long vowels (ship ≠ sheep)
- Note formality level (formal/informal/neutral)
- Mention British vs American differences if applicable
- Keep notes practical and concise

RUSSIAN_SPEAKER_TIPS (include when relevant, otherwise null):
- False friends: magazine ≠ магазин, accurate ≠ аккуратный, etc.
- Article usage patterns: "I have A car" (not "I have car")
- Preposition differences compared to Russian: "depend ON" (зависеть ОТ)
- Common word order mistakes to avoid
- If no specific tips needed for Russian speakers, set to null

"""


def examples() -> str:
    examples_preamble = """
Examples:

Input: WORD: [resilience]; CONTEXT: [psychology]
Output:
{
  "definition": "The ability to recover quickly from difficulties or adapt to challenging situations.",
  "russian_translation": "устойчивость, стойкость, способность восстанавливаться",
  "context_sentences": [
    "Her resilience helped her overcome the job loss and start a new career.",
    "The company showed great resilience during the economic crisis.",
    "Building resilience is important for mental health and well-being."
  ],
  "notes": "Stress: reSILience. Collocations: build resilience, show resilience, emotional resilience. Often used in psychology and business contexts. Similar to 'toughness' but emphasizes recovery and adaptation.",
  "russian_speaker_tips": null
}

Input: WORD: [stumble upon]; CONTEXT: []
Output:
{
  "definition": "To find or discover something by chance, without looking for it.",
  "russian_translation": "случайно наткнуться, обнаружить случайно",
  "context_sentences": [
    "I stumbled upon an amazing café while exploring the neighborhood.",
    "She stumbled upon the solution while working on a different problem.",
    "Have you ever stumbled upon an old photo and felt nostalgic?"
  ],
  "notes": "Phrasal verb. Informal/neutral. Collocations: stumble upon + a discovery/solution/idea/secret/opportunity. Similar to 'come across', 'run into'.",
  "russian_speaker_tips": "Preposition: use 'upon' or 'on' (NOT 'to'). Don't confuse with физически споткнуться (that's just 'stumble' without 'upon')."
}

Input: WORD: [accurate]; CONTEXT: []
Output:
{
  "definition": "Correct, exact, and without any mistakes.",
  "russian_translation": "точный, верный, правильный",
  "context_sentences": [
    "The weather forecast was surprisingly accurate this time.",
    "Please make sure all the data in the report is accurate.",
    "His accurate description helped the police find the suspect."
  ],
  "notes": "Stress: ACCurate. Collocations: accurate information, accurate description, highly accurate, fairly accurate. Opposite: inaccurate.",
  "russian_speaker_tips": "FALSE FRIEND: accurate ≠ аккуратный! 'Accurate' means точный (correct). 'Аккуратный' in English is 'neat' or 'tidy'."
}

Input: WORD: [jot down]; CONTEXT: []
Output:
{
  "definition": "To write something quickly, usually a short note or reminder.",
  "russian_translation": "быстро записать, набросать",
  "context_sentences": [
    "Let me jot down your phone number before I forget it.",
    "She jotted down the main points during the meeting.",
    "I always jot down ideas when they come to me."
  ],
  "notes": "Phrasal verb. Informal/neutral. Collocations: jot down + notes/ideas/numbers/reminders/thoughts. Similar to 'write down' but emphasizes speed and brevity.",
  "russian_speaker_tips": null
}

Now process the input and return ONLY the JSON response.
"""
    return examples_preamble


def rule_language_level() -> str:
    return f"""
    Language Level:
    - A person with the language level [{Config.LEVEL}] should understand the card.
    - Words and constructions that should be familiar to a person at this level.
    - If the language level is set to C1 or C2, use words and constructions of your choice.
    """


def get_prompt() -> str:
    return anki_prompt_preamble + rule_language_level() + examples()
