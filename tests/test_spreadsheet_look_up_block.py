from unittest.mock import Mock, patch
from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..spreadsheet_look_up_block import SpreadsheetLookUp


class TestSpreadsheetLookUp(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = SpreadsheetLookUp()
        self.configure_block(blk, {
            'source': 'tests/test.xlsx',
            'match': [
                {
                    'key': '{{ $host }}',
                    'value': 'MOXA HOST',
                },
                {
                    'key': '{{ $channel }}',
                    'value': 'CHANNEL',
                },
            ],
            'output_structure': [
                {
                    'key': 'flavor',
                    'value': 'FLAVOR',
                },
                {
                    'key': 'position',
                    'value': 'POSITION',
                },
            ],
        })
        blk.start()
        blk.process_signals([
            Signal({
                'host': '101',
                'channel': '0',
            }),
        ])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assert_last_signal_list_notified([
            Signal({
                'flavor': 'House Roast',
                'position': '0',
            }),
        ])
