from embedder.embedder import embed, setup_document
from encoder_decoder import encoder_decoder

def test_embed():
    lorem_ipsum = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr.'
    secret = ['000', '100', '100', '001', '100', '101', '011', '011', '000', '110', '110', '001', '101', '111', '001', '000', '000', '101', '011', '101', '101', '111', '011', '100', '100', '110', '110', '001', '100', '100'] # 'Hello World'
    expected_result = r"\fch{L}{put}\fch{o}{put}\fch{r}{qpl}\fch{e}{pbk}\fch{m}{pbk} \fch{i}{put}\fch{p}{put}\fch{s}{qcs}\fch{u}{bch}\fch{m}{ppl} \fch{d}{ppl}\fch{o}{qcs}\fch{l}{ppl}\fch{o}{qtm}\fch{r}{qtm} \fch{s}{qpl}\fch{i}{bch}\fch{t}{ppl} \fch{a}{qpl}\fch{m}{pbk}\fch{e}{pbk}\fch{t}{qtm}, \fch{c}{qcs}\fch{o}{qcs}\fch{n}{ppl}\fch{s}{put}\fch{e}{qpl}\fch{t}{put}\fch{e}{put}\fch{t}{qtm}ur sadipscing elitr."
    document = setup_document()
    assert expected_result in embed(document, lorem_ipsum, secret).dumps()