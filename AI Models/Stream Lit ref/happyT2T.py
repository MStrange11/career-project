from happytransformer import HappyTextToText, TTSettings

# Example usage of HappyTextToText for grammar correction
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

def fix_grammar(text):
    return happy_tt.generate_text(f"grammar:{text}", args=args).text

print(fix_grammar("I has a apple.")) 
