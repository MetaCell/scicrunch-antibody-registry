from api.utilities.functions import catalog_number_chunked


def test_catalog_number_chunked():

    # Create antibodies
    SEARCH_CATALOG_TERM_1 = 'N1002'
    chunk_term_1 = catalog_number_chunked(SEARCH_CATALOG_TERM_1)
    assert set(chunk_term_1.split(' ')) == set('n 1002'.split(' '))

    SEARCH_CATALOG_TERM_2 = 'N0304-AB635P-L'
    chunk_term_2 = catalog_number_chunked(SEARCH_CATALOG_TERM_2)
    assert set(chunk_term_2.split(' ')) == set(
        'n 0304 ab 635 p l pl'.split(' '))

    SEARCH_CATALOG_TERM_3 = 'N0304-AB635'
    chunk_term_3 = catalog_number_chunked(SEARCH_CATALOG_TERM_3)
    assert set(chunk_term_3.split(' ')) == set('n 0304 ab 635'.split(' '))

    SEARCH_CATALOG_TERM_4 = 'K0202'
    chunk_term_4 = catalog_number_chunked(SEARCH_CATALOG_TERM_4)
    assert set(chunk_term_4.split(' ')) == set('k 0202'.split(' '))

    SEARCH_CATALOG_TERM_5 = 'N0304-AB635P-S'
    chunk_term_5 = catalog_number_chunked(SEARCH_CATALOG_TERM_5)
    assert set(chunk_term_5.split(' ')) == set(
        'n 0304 ab 635 p s ps'.split(' '))


    SEARCH_CATALOG_TERM_6 = 'N0304-AB635P-'
    chunk_term_6 = catalog_number_chunked(SEARCH_CATALOG_TERM_6)
    assert set(chunk_term_6.split(' ')) == set('n 0304 ab 635 p'.split(' '))

    SEARCH_CATALOG_TERM_7 = 'N1002-AbRED-S'
    chunk_term_7 = catalog_number_chunked(SEARCH_CATALOG_TERM_7)
    assert set(chunk_term_7.split(' ')) == set(
        'n 1002 abred s abreds'.split(' '))

    SEARCH_CATALOG_TERM_8 = 'N0304-AB6'
    chunk_term_8 = catalog_number_chunked(SEARCH_CATALOG_TERM_8)
    assert set(chunk_term_8.split(' ')) == set('n 0304 ab 6'.split(' '))

    SEARCH_CATALOG_TERM_9 = 'N1002-AbRED'
    chunk_term_9 = catalog_number_chunked(SEARCH_CATALOG_TERM_9)
    assert set(chunk_term_9.split(' ')) == set('n 1002 abred'.split(' '))

    SEARCH_CATALOG_TERM_10 = 'N0304-AB635P-L'
    SEARCH_CATALOG_ALT_TERM_10 = 'N0304-AB635P-S'
    chunk_term_10 = catalog_number_chunked(
        SEARCH_CATALOG_TERM_10, SEARCH_CATALOG_ALT_TERM_10)
    assert set(chunk_term_10.split(' ')) == set(
        'n 0304 ab 635 p l s pl ps'.split(' '))
