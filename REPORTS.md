# Automated Reports          

## Coverage Report
```text
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
core/__init__.py                 0      0   100%
core/backgammon.py              58     10    83%   71, 76, 120, 130, 143, 147, 153-154, 162, 182
core/board.py                   68      8    88%   53, 80-83, 153-155
core/dice.py                    13      0   100%
core/exceptions.py              10      0   100%
core/ficha.py                   15      0   100%
core/player.py                   7      0   100%
core/validaciones.py           114     23    80%   38, 68, 71, 86, 89-90, 121, 127, 131, 143, 178, 182, 192-193, 199-207, 259
tests/test_backgammon.py        47      2    96%   45-46
tests/test_board.py            134      6    96%   60, 79, 102, 124, 140, 143
tests/test_dice.py              26      1    96%   31
tests/test_ficha.py             26      0   100%
tests/test_player.py            10      0   100%
tests/test_validaciones.py      84      0   100%
----------------------------------------------------------
TOTAL                          612     50    92%

```          

## Pylint Report
```text
************* Module core.board
core/board.py:9:0: W0611: Unused Validaciones imported from validaciones (unused-import)

-----------------------------------
Your code has been rated at 9.97/10


```
