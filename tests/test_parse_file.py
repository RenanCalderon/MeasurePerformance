import logging
from src.utility import parse_file

LOG = logging.getLogger(__name__)

test_case = "hola_G_Prod_20220819.als"

def test_parse():
    lista = parse_file(test_case)
    LOG.info(f"Lista de nombre parseado: {lista}")
    assert lista[0] == "hola"
    assert lista[1] == "G"
    assert lista[2] == "Prod"
    assert lista[3] == "20220819"
    assert lista[4] == "als"