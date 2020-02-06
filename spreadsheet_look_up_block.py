import xlrd

from nio import Block, Signal
from nio.properties import FileProperty, ListProperty, PropertyHolder, \
    StringProperty, VersionProperty


class Match(PropertyHolder):

    key = StringProperty(title='Key', order=0)
    value = StringProperty(title='Value', order=1)


class OutputStructure(PropertyHolder):

    key = StringProperty(title='Key', order=0)
    value = StringProperty(title='Value', order=1)


class SpreadsheetLookUp(Block):

    source = FileProperty(title='Source File', order=0)
    match = ListProperty(
        Match,
        title='Match',
        order=1)
    output_structure = ListProperty(
        OutputStructure,
        title='Output Structure',
        order=2)

    version = VersionProperty('0.1.0')

    def start(self):
        self.map = {}
        rows = self._read_xlsx(xlrd.open_workbook(self.source().file))
        for row in rows:
            value = {}
            for item in self.output_structure():
                value[item.key()] = row[item.value()] or None
            self.nested_set(
                self.map,
                [row[match.value()] for match in self.match()],
                value)
        super().start()

    def process_signal(self, signal):
        dic = self.map
        for match in self.match():
            dic = dic[match.key(signal)]
        return Signal(dic)

    @staticmethod
    def nested_set(dic, keys, value):
        # https://stackoverflow.com/a/13688108/11653218
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

    @staticmethod
    def _read_xlsx(source, sheet='Sheet1'):
        open_sheet = source.sheet_by_name(sheet)
        rows = []
        labels = [n.value for n in open_sheet.row(0)]
        for i, row in enumerate(open_sheet.get_rows()):
            if not i:
                continue
            cells = []
            # number data is always float, drop tailing zeroes and stringify
            for cell in row:
                if cell.ctype in (2, 3):
                    # data is float
                    if int(cell.value) == cell.value:
                        # data is actually an int stored as a float
                        cells.append(str(int(cell.value)))
                    else:
                        cells.append(str(cell.value))
                else:
                    # data is text
                    cells.append(cell.value.strip())
            row_data = dict(zip(labels, cells))
            rows.append(row_data)
        return rows
