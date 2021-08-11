type token =
  | AT
  | LPA
  | RPA
  | LCB
  | RCB
  | LSB
  | RSB
  | COM
  | TR
  | LABELS
  | NULL
  | STR of (string)
  | EOF
  | CMD
  | EOC
  | ERR

val signature :
  (Lexing.lexbuf  -> token) -> Lexing.lexbuf -> (Db.schema)
val tsdb :
  (Lexing.lexbuf  -> token) -> Lexing.lexbuf -> (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)
