import pyperclip
import re
from enum import Enum

# Enum to define different types of tokens in the text
class TokenType(Enum):
    WORD = 1
    INLINE_MATH = 2
    DISPLAY_MATH = 3

# Function to tokenize the input text into WORD, INLINE_MATH, and DISPLAY_MATH
def tokenize_text_v2(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i:].startswith('\\('):
            end_index = text[i:].find('\\)') + i + 2
            tokens.append((TokenType.INLINE_MATH, text[i+2:end_index-2]))
            i = end_index
        elif text[i:].startswith('\\['):
            end_index = text[i:].find('\\]') + i + 2
            tokens.append((TokenType.DISPLAY_MATH, text[i+2:end_index-2]))
            i = end_index
        else:
            end_index = text[i:].find('\\(')
            next_display_math = text[i:].find('\\[')
            if end_index == -1 and next_display_math == -1:
                end_index = len(text)
            else:
                if end_index == -1:
                    end_index = next_display_math
                elif next_display_math == -1:
                    next_display_math = end_index
                end_index = min(end_index, next_display_math)
                end_index += i
            tokens.append((TokenType.WORD, text[i:end_index]))
            i = end_index
    return tokens

# Function to process tokens and convert them to the target format
def process_tokens(tokens):
    processed_tokens = []
    for token_type, content in tokens:
        if token_type == TokenType.INLINE_MATH:
            processed_tokens.append(f"${content.strip()}$")
        elif token_type == TokenType.DISPLAY_MATH:
            processed_tokens.append(f"$$\n{content.strip()}\n$$")
        else:
            processed_tokens.append(content)
    return processed_tokens

# Function to reassemble the processed tokens into a single string
def reassemble_text(processed_tokens):
    reassembled_text = ''
    for i, token in enumerate(processed_tokens):
        # If the current token is inline math and it's not the first or last token
        if token.startswith('$') and token.endswith('$') and i > 0 and i < len(processed_tokens) - 1:
            # Add spaces around the inline math token only if the adjacent tokens are words
            if not processed_tokens[i - 1].endswith('$') and not processed_tokens[i + 1].startswith('$'):
                reassembled_text += f' {token} '
            else:
                reassembled_text += token
        else:
            reassembled_text += token
    # Remove extra spaces
    reassembled_text = re.sub(r' +', ' ', reassembled_text)
    return reassembled_text

# Main function to read from clipboard, process the text, and write back to clipboard
def main():
    # Read the clipboard
    clipboard_content = pyperclip.paste()

    # Tokenize the clipboard content
    tokens = tokenize_text_v2(clipboard_content)

    # Process the tokens to the target format
    processed_tokens = process_tokens(tokens)

    # Reassemble the processed tokens into a single string
    new_content = reassemble_text(processed_tokens)

    # Update the clipboard with the new content
    pyperclip.copy(new_content)

# Execute the main function
main()