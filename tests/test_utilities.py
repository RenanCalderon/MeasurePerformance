import logging
from src.utilities import *

LOG = logging.getLogger(__name__)

test_case = "hola_G_Prod_20220819.als"


def test_parse():
    lista = parse_file(test_case)
    LOG.info(f"Lista de nombre parseado: {lista}")
    assert lista[0] == "hola"
    assert lista[1] == "G"
    assert lista[2] == "Prod"
    assert lista[3] == "20220819"


def test_is_df():
    df = list_to_dataframe(parse_file(test_case))
    response = isinstance(df, pd.DataFrame)
    LOG.info(f"Response::: {response}")
    assert response == True
