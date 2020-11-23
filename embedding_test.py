import lorem
from embedder.embedder import Embedder
from encoder_decoder import encoder_decoder

some_text = lorem.paragraph()
some_secret = encoder_decoder.encode('Hello World', 3)

embedder = Embedder()
embedder.embed(some_text, some_secret)
embedder.embed(some_text, some_secret, is_colored=True)
embedder.generate_document('embedded_document')

embedder = Embedder()
embedder.print_all_fontfamilies(is_colored=True)
embedder.generate_document('fontfamilies')
