import pytest
import ftp_hands
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
from handparser.common import ET
from handparser.ftp import FullTiltHand


@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text and returns a PokerStarsHand instance."""
    h = FullTiltHand(request.instance.hand_text, parse=False)
    h.parse_header()
    return h


@pytest.fixture
def hand(request):
    """Parse handhistory defined in hand_text class attribute and returns a PokerStarsHand instance."""
    return FullTiltHand(request.instance.hand_text)


class TestHandWithFlopOnly:
    hand_text = ftp_hands.HAND1

    @pytest.mark.parametrize('attribute,expected_value',
                             [('game_type', 'TOUR'),
                              ('sb', Decimal(10)),
                              ('bb', Decimal(20)),
                              ('date', ET.localize(datetime(2013, 9, 22, 13, 26, 50))),
                              ('game', 'HOLDEM'),
                              ('limit', 'NL'),
                              ('ident', '33286946295'),
                              ('tournament_ident', '255707037'),
                              ('tournament_name', 'MiniFTOPS Main Event'),
                              ('table_name', '179'),
                              ('tournament_level', None),
                              ('buyin', None),
                              ('rake', None),
                              ('currency', None),
                             ])
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value

    @pytest.mark.parametrize('attribute,expected_value',
                             [('players', OrderedDict([('Popp1987', 13587), ('Luckytobgood', 10110),
                                                       ('FatalRevange', 9970), ('IgaziFerfi', 10000),
                                                       ('egis25', 6873), ('gamblie', 9880), ('idanuTz1', 10180),
                                                       ('PtheProphet', 9930), ('JohnyyR', 9840)])),
                              ('button', 'egis25'),
                              ('button_seat', 5),
                              ('max_players', 9),
                              ('hero', 'IgaziFerfi'),
                              ('hero_seat', 4),
                              ('hero_hole_cards', ('9d', 'Ks'))
                             ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value
