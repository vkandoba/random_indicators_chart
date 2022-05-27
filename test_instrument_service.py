import pytest
import instrument_service


def test_generate_instruments():
    instrument_names = instrument_service.generate_instruments(100)
    assert instrument_names[0] == 'ticker_00'
    assert instrument_names[-1] == 'ticker_99'
    assert len(instrument_names) == 100
