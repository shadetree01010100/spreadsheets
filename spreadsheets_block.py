from nio import Block
from nio.properties import VersionProperty


class Spreadsheets(Block):

    version = VersionProperty('0.1.0')

    def process_signals(self, signals):
        for signal in signals:
            pass
        self.notify_signals(signals)