import json
import re
import sys
import unicodedata

class TrieNode:
    def __init__(self):
        self.children = {}
        # mark end-of-word here if needed:
        self.is_word = False

def insert_word(root, word):
    """Insert a word into the trie."""
    node = root
    for letter in word:
        if letter not in node.children:
            node.children[letter] = TrieNode()
        node = node.children[letter]
    node.is_word = True

def trie_to_dict(node, letter=""):
    """
    Recursively convert a TrieNode to a dictionary.
    Each node will have:
      - "name": the letter for that node
      - "children": a list of child nodes (empty list if none)
    """
    # sort children for consistency
    children = [trie_to_dict(child, l) for l, child in sorted(node.children.items())]
    return {"name": letter, "children": children}

def tokenize_text(text):
    """
    Tokenize the text into words.
    This regex extracts word characters; feel free to adjust if you need more sophisticated tokenization.
    """
    # normalize the text to decompose accented characters
    text = unicodedata.normalize('NFD', text)
    # remove diacritics
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # replace non-alphabet characters with whitespace
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # extract words
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_trie.py <path_to_corpus> <output_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    words = tokenize_text(text)
    print(f"Tokenized {len(words)} words.")
    
    root = TrieNode()
    for word in words:
        insert_word(root, word)
    
    # convert trie to a JSON-friendly dictionary.
    # we use an empty string as the name of the root.
    tree_dict = trie_to_dict(root, letter="")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tree_dict, f, indent=2)

if __name__ == '__main__':
    main()
