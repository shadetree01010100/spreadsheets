SpreadsheetLookUp
=======
Load an Excel spreadsheet (.xlsx) and lookup values.

Properties
----------
- **Source File**: Path to .xlsx file
- **Match**: Find the row of **Source File** where, for each configured item, the value of *key* matches the column labeled *value*.
- **Output Structure**: Define output *key: value* pairs, where *value* is the label of the column to use.

Example
-------
Source File:
```
ANIMAL, COLOR, AGE
dog,    brown, 4
dog,    white, 2
cat,    black, 7
```

Configuration:
```
Match
  key: {{ $animal }}
  value: ANIMAL

  key: {{ $color }}
  value: COLOR

Output Structure
  key: age
  value: AGE
```

When processing signals, the incoming values for `$animal` and `$color` are used to match a single row from the **Source File**. From that row, for each item added to **Output Structure**, the column matching *value* is selected, and its contents are put into the outgoing signal attribute *key*.

```
Incoming Signal:
{
  "animal": "dog",
  "color": "brown",
}

Outgoing Signal:
{
  "age": 2,
}
```

Commands
--------
None
