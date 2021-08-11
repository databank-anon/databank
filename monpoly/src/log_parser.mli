type token =
  | AT
  | LPA
  | RPA
  | LCB
  | RCB
  | COM
  | TR
  | STR of (string)
  | EOF
  | CMD
  | EOC
  | ERR

val signature :
  (Lexing.lexbuf  -> token) -> Lexing.lexbuf -> (Db.schema)
val tsdb :
  (Lexing.lexbuf  -> token) -> Lexing.lexbuf -> (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)
