# Automated Reports          

## Coverage Report
```text
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
core/__init__.py                 0      0   100%
core/backgammon.py              58     10    83%   72, 77, 121, 131, 144, 148, 154-155, 163, 183
core/board.py                   74     10    86%   53, 80-83, 123, 125, 159-161
core/dice.py                    14      0   100%
core/exceptions.py              10      0   100%
core/ficha.py                   15      0   100%
core/player.py                   7      0   100%
core/validaciones.py            90     11    88%   38, 43, 46, 96, 102, 106, 118, 153, 159, 163, 217
tests/test_backgammon.py        47      2    96%   45-46
tests/test_board.py            134      6    96%   60, 79, 102, 124, 140, 143
tests/test_dice.py              26      1    96%   31
tests/test_ficha.py             26      0   100%
tests/test_player.py            10      0   100%
tests/test_validaciones.py      84      0   100%
----------------------------------------------------------
TOTAL                          595     40    93%

```          

## Pylint Report
```text
************* Module core.board
core/board.py:19:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:26:49: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:27:30: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:45:61: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:50:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:54:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:70:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:84:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:98:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:112:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:144:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:148:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:156:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:158:0: C0301: Line too long (136/100) (line-too-long)
core/board.py:162:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:166:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:175:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:176:27: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:178:0: C0301: Line too long (132/100) (line-too-long)
core/board.py:182:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:184:0: C0304: Final newline missing (missing-final-newline)
core/board.py:9:0: W0611: Unused Validaciones imported from validaciones (unused-import)
************* Module core.exceptions
core/exceptions.py:34:0: C0304: Final newline missing (missing-final-newline)
************* Module core.player
core/player.py:23:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:31:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:38:0: C0304: Final newline missing (missing-final-newline)
************* Module core.ficha
core/ficha.py:27:0: C0303: Trailing whitespace (trailing-whitespace)
core/ficha.py:73:0: C0304: Final newline missing (missing-final-newline)
************* Module core.validaciones
core/validaciones.py:20:17: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:40:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:44:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:47:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:50:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:53:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:56:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:60:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:62:0: C0301: Line too long (105/100) (line-too-long)
core/validaciones.py:64:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:93:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:97:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:100:31: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:102:32: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:109:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:114:28: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:117:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:119:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:137:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:143:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:149:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:154:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:164:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:166:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:190:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:207:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:211:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:221:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:230:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:231:0: C0304: Final newline missing (missing-final-newline)
core/validaciones.py:152:11: R1714: Consider merging these comparisons with 'in' by using 'destino in (24, -1)'. Use a set instead if elements are hashable. (consider-using-in)
core/validaciones.py:121:4: R0912: Too many branches (14/12) (too-many-branches)
core/validaciones.py:218:23: W0718: Catching too general exception Exception (broad-exception-caught)
core/validaciones.py:228:23: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module core.dice
core/dice.py:32:13: C0303: Trailing whitespace (trailing-whitespace)
core/dice.py:40:40: C0303: Trailing whitespace (trailing-whitespace)
core/dice.py:41:0: C0303: Trailing whitespace (trailing-whitespace)
core/dice.py:48:0: C0304: Final newline missing (missing-final-newline)
core/dice.py:29:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module core.backgammon
core/backgammon.py:59:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:73:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:78:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:80:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:89:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:97:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:105:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:119:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:122:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:132:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:135:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:138:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:141:40: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:142:42: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:145:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:189:0: C0304: Final newline missing (missing-final-newline)
************* Module cli.cli
cli/cli.py:8:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:9:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:13:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:16:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:20:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:22:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:25:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:30:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:37:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:46:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:59:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:62:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:66:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:74:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:84:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:89:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:100:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:103:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:109:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:110:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:120:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:125:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:135:0: C0304: Final newline missing (missing-final-newline)
cli/cli.py:1:0: C0114: Missing module docstring (missing-module-docstring)
cli/cli.py:2:0: W0401: Wildcard import core.exceptions (wildcard-import)
cli/cli.py:5:0: C0115: Missing class docstring (missing-class-docstring)
cli/cli.py:32:18: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
cli/cli.py:41:18: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
cli/cli.py:42:18: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
cli/cli.py:44:18: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
cli/cli.py:45:18: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
cli/cli.py:80:15: W0718: Catching too general exception Exception (broad-exception-caught)
cli/cli.py:68:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
cli/cli.py:2:0: W0614: Unused import(s) FueraDeRangoError, CeldaInvalidaError, ValidacionError, CeldaBloqueadaError, FichasCapturadasError, SinFichasCapturadas, ReingresoInvalidoError, SalidaInvalidaError and SaltosError from wildcard import of core.exceptions (unused-wildcard-import)

-----------------------------------
Your code has been rated at 6.58/10


```
