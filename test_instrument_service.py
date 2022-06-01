from generate_price_service.instrument_service import InstrumentService


def test_generate_instruments():
    instrument_names = InstrumentService(instruments_count=100).names()
    assert instrument_names[0] == 'ticker_00'
    assert instrument_names[-1] == 'ticker_99'
    assert len(instrument_names) == 100
