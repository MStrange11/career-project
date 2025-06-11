from happytransformer import HappyTextToText, TTSettings

# ValueError: Your currently installed version of Keras is Keras 3, but this is not yet supported in Transformers. Please install the backwards-compatible tf-keras package with `pip install tf-keras`.

print("This is a test script for grammar correction using HappyTransformer.")
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

args = TTSettings(num_beams=5, min_length=1)

# Add the prefix "grammar: " before each input 
print("Adding prefix 'grammar: ' to the input text.")
result = happy_tt.generate_text("grammar: This have sentences has has bads grammar.", args=args)

print(result.text) # This sentence has bad grammar.
