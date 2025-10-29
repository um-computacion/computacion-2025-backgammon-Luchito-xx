# Automated Reports          

## Coverage Report
```text
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
core/__init__.py                 0      0   100%
core/backgammon.py              58     10    83%   49, 54, 79, 89, 102, 106, 110-111, 115, 124
core/board.py                   74     10    86%   40, 52-55, 84, 86, 107-109
core/dice.py                    14      0   100%
core/exceptions.py              20      0   100%
core/ficha.py                   15      0   100%
core/player.py                   9      0   100%
core/validaciones.py            90     11    88%   15, 20, 23, 55, 61, 65, 77, 101, 107, 111, 146
tests/test_backgammon.py        47      2    96%   45-46
tests/test_board.py            134      6    96%   60, 79, 102, 124, 140, 143
tests/test_dice.py              26      1    96%   31
tests/test_ficha.py             26      0   100%
tests/test_player.py            15      0   100%
tests/test_validaciones.py      84      0   100%
----------------------------------------------------------
TOTAL                          612     40    93%

```          

## Pylint Report
```text
************* Module core.main
core/main.py:2:0: C0304: Final newline missing (missing-final-newline)
core/main.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/main.py:1:0: C0115: Missing class docstring (missing-class-docstring)
core/main.py:1:0: C0103: Class name "main" doesn't conform to PascalCase naming style (invalid-name)
core/main.py:1:0: R0903: Too few public methods (0/2) (too-few-public-methods)
************* Module core.board
core/board.py:15:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:17:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:18:47: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:19:28: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:32:59: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:37:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:41:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:49:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:56:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:63:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:73:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:92:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:96:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:104:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:106:0: C0301: Line too long (130/100) (line-too-long)
core/board.py:110:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:114:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:123:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:124:27: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:126:0: C0301: Line too long (126/100) (line-too-long)
core/board.py:130:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/board.py:2:0: W0401: Wildcard import validaciones (wildcard-import)
core/board.py:2:0: W0614: Unused import(s) Validaciones, BackgammonError, FueraDeRangoError, CeldaInvalidaError, ValidacionError, CeldaBloqueadaError, FichasCapturadasError, SinFichasCapturadas, ReingresoInvalidoError, SalidaInvalidaError and SaltosError from wildcard import of validaciones (unused-wildcard-import)
************* Module core.exceptions
core/exceptions.py:42:0: C0305: Trailing newlines (trailing-newlines)
core/exceptions.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/exceptions.py:3:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:7:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:11:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:15:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:19:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:23:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:27:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:31:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:35:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:39:4: W0107: Unnecessary pass statement (unnecessary-pass)
************* Module core.player
core/player.py:9:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:13:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:21:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.ficha
core/ficha.py:37:0: C0303: Trailing whitespace (trailing-whitespace)
core/ficha.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.validaciones
core/validaciones.py:8:17: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:17:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:21:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:24:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:27:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:30:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:33:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:37:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:39:0: C0301: Line too long (105/100) (line-too-long)
core/validaciones.py:41:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:52:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:56:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:59:31: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:61:32: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:68:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:73:28: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:76:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:78:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:85:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:91:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:97:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:102:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:112:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:114:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:129:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:136:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:140:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:150:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:159:0: C0303: Trailing whitespace (trailing-whitespace)
core/validaciones.py:160:0: C0304: Final newline missing (missing-final-newline)
core/validaciones.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/validaciones.py:1:0: W0401: Wildcard import exceptions (wildcard-import)
core/validaciones.py:100:11: R1714: Consider merging these comparisons with 'in' by using 'destino in (24, -1)'. Use a set instead if elements are hashable. (consider-using-in)
core/validaciones.py:80:4: R0912: Too many branches (14/12) (too-many-branches)
core/validaciones.py:147:23: W0718: Catching too general exception Exception (broad-exception-caught)
core/validaciones.py:157:23: W0718: Catching too general exception Exception (broad-exception-caught)
core/validaciones.py:1:0: W0614: Unused import(s) BackgammonError, ValidacionError and SaltosError from wildcard import of exceptions (unused-wildcard-import)
************* Module core.dice
core/dice.py:18:13: C0303: Trailing whitespace (trailing-whitespace)
core/dice.py:23:40: C0303: Trailing whitespace (trailing-whitespace)
core/dice.py:24:0: C0303: Trailing whitespace (trailing-whitespace)
core/dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/dice.py:15:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module core.backgammon
core/backgammon.py:41:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:50:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:55:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:57:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:62:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:66:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:70:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:77:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:80:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:90:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:93:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:96:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:99:38: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:100:40: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:103:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon.py:130:0: C0304: Final newline missing (missing-final-newline)
core/backgammon.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/backgammon.py:4:0: W0401: Wildcard import validaciones (wildcard-import)
core/backgammon.py:5:0: W0401: Wildcard import exceptions (wildcard-import)
core/backgammon.py:4:0: W0614: Unused import(s) BackgammonError, FueraDeRangoError, CeldaInvalidaError, ValidacionError, CeldaBloqueadaError, FichasCapturadasError, SinFichasCapturadas, ReingresoInvalidoError and SalidaInvalidaError from wildcard import of validaciones (unused-wildcard-import)
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
Your code has been rated at 5.98/10


```
