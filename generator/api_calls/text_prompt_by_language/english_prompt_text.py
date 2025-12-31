from generator.config import Config

anki_prompt_preamble = """You are an English vocabulary teacher creating flashcards for B2 level learners.

IMPORTANT: Output ONLY valid JSON. No markdown, no explanations, just JSON.

JSON Structure:
{
  "definition": "string",
  "context_sentences": ["string", "string", "string"],
  "notes": "string"
}

B2 Level Guidelines:
- Use everyday vocabulary that an upper-intermediate learner would understand
- Avoid overly academic or technical terms in definitions
- Keep definitions concise: 1-2 sentences maximum
- Example sentences should be realistic and useful

DEFINITION:
- Write a clear, practical definition
- Use simple, common words
- Focus on the most common meaning/usage
- 1-2 sentences max

CONTEXT_SENTENCES:
- Provide exactly 3 example sentences
- Show different contexts (work, personal, formal, informal)
- Use natural, conversational language
- Each sentence should demonstrate clear word usage
- Keep sentences 10-15 words long

NOTES:
- Mention common collocations (e.g., "often used with...", "followed by...")
- Warn about confusing similar words
- Note formality level if relevant (formal/informal/neutral)
- Mention British vs American differences if applicable
- Keep notes brief and practical

"""


def examples() -> str:
    examples_preamble = """
Examples:

Input: WORD: [resilience]; CONTEXT: [psychology]
Output:
{
  "definition": "The ability to recover quickly from difficulties or adapt to challenging situations.",
  "context_sentences": [
    "Her resilience helped her overcome the job loss and start a new career.",
    "The company showed great resilience during the economic crisis.",
    "Building resilience is important for mental health and well-being."
  ],
  "notes": "Often used in psychology and business contexts. Common phrase: 'build resilience'. Similar to 'toughness' but emphasizes recovery and adaptation."
}

Input: WORD: [stumble upon]; CONTEXT: []
Output:
{
  "definition": "To find or discover something by chance, without looking for it.",
  "context_sentences": [
    "I stumbled upon an amazing café while exploring the neighborhood.",
    "She stumbled upon the solution while working on a different problem.",
    "Have you ever stumbled upon an old photo and felt nostalgic?"
  ],
  "notes": "Phrasal verb. Informal/neutral tone. Always followed by a noun (stumble upon something). Similar to 'come across' or 'discover by accident'."
}

Input: WORD: [jot down]; CONTEXT: []
Output:
{
  "definition": "To write something quickly, usually a short note or reminder.",
  "context_sentences": [
    "Let me jot down your phone number before I forget it.",
    "She jotted down the main points during the meeting.",
    "I always jot down ideas when they come to me."
  ],
  "notes": "Phrasal verb. Informal/neutral. Common in everyday speech. Similar to 'write down' but emphasizes speed and brevity. Often used with: ideas, notes, numbers, reminders."
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
