# test file to check if enigma class works
from Enigma import Enigma

en = Enigma(password="decentkeydkdkdk",
            text_encoding="utf-8")
text = "nv80"
text = en.cypher_text(text, decypher=True)
print(text)
