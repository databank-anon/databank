type token =
  | FALSE
  | TRUE
  | LPA
  | RPA
  | LSB
  | RSB
  | COM
  | SC
  | DOT
  | QM
  | LD
  | LESSEQ
  | EQ
  | LESS
  | GTR
  | GTREQ
  | STAR
  | LARROW
  | PLUS
  | MINUS
  | SLASH
  | MOD
  | F2I
  | I2F
  | STR of (string)
  | STR_CST of (string)
  | INT of (float)
  | RAT of (float)
  | TU of (int*char)
  | LET
  | IN
  | NOT
  | AND
  | OR
  | IMPL
  | EQUIV
  | EX
  | FA
  | PREV
  | NEXT
  | EVENTUALLY
  | ONCE
  | ALWAYS
  | PAST_ALWAYS
  | SINCE
  | UNTIL
  | BAR
  | FREX
  | PREX
  | CNT
  | MIN
  | MAX
  | SUM
  | AVG
  | MED
  | END
  | EOF

val formula :
  (Lexing.lexbuf  -> token) -> Lexing.lexbuf -> MFOTL.formula
