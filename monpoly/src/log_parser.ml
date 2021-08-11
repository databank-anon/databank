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

open Parsing;;
let _ = parse_error;;
# 43 "log_parser.mly"
module H = Log_parser_helper.StandardLog_parser_helper
let f = H.f
# 21 "log_parser.ml"
let yytransl_const = [|
  257 (* AT *);
  258 (* LPA *);
  259 (* RPA *);
  260 (* LCB *);
  261 (* RCB *);
  262 (* COM *);
  263 (* TR *);
    0 (* EOF *);
  265 (* CMD *);
  266 (* EOC *);
  267 (* ERR *);
    0|]

let yytransl_block = [|
  264 (* STR *);
    0|]

let yylhs = "\255\255\
\001\000\001\000\003\000\002\000\002\000\002\000\002\000\002\000\
\002\000\002\000\002\000\002\000\002\000\002\000\002\000\002\000\
\002\000\002\000\008\000\008\000\009\000\010\000\010\000\011\000\
\004\000\004\000\004\000\005\000\012\000\014\000\014\000\015\000\
\013\000\017\000\017\000\016\000\006\000\006\000\018\000\018\000\
\020\000\019\000\019\000\021\000\022\000\022\000\023\000\007\000\
\000\000\000\000"

let yylen = "\002\000\
\002\000\000\000\004\000\004\000\003\000\004\000\003\000\004\000\
\004\000\004\000\004\000\002\000\002\000\001\000\004\000\004\000\
\004\000\004\000\002\000\000\000\002\000\002\000\000\000\003\000\
\003\000\001\000\000\000\007\000\003\000\003\000\001\000\005\000\
\003\000\003\000\001\000\003\000\001\000\003\000\002\000\000\000\
\003\000\002\000\000\000\005\000\002\000\000\000\003\000\007\000\
\002\000\002\000"

let yydefred = "\000\000\
\000\000\000\000\000\000\000\000\049\000\000\000\000\000\014\000\
\000\000\050\000\000\000\001\000\000\000\012\000\000\000\000\000\
\013\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\037\000\005\000\000\000\000\000\
\000\000\000\000\007\000\000\000\003\000\016\000\015\000\018\000\
\017\000\021\000\000\000\009\000\008\000\011\000\010\000\019\000\
\000\000\000\000\000\000\000\000\000\000\004\000\006\000\000\000\
\039\000\025\000\022\000\024\000\000\000\041\000\000\000\000\000\
\000\000\000\000\000\000\038\000\000\000\000\000\000\000\000\000\
\000\000\029\000\000\000\000\000\000\000\000\000\042\000\000\000\
\045\000\000\000\000\000\030\000\000\000\000\000\000\000\000\000\
\047\000\000\000\048\000\000\000\000\000\000\000\033\000\000\000\
\000\000\032\000\036\000\034\000\028\000\044\000"

let yydgoto = "\003\000\
\005\000\010\000\006\000\020\000\031\000\032\000\018\000\023\000\
\024\000\042\000\043\000\053\000\077\000\064\000\065\000\086\000\
\087\000\033\000\068\000\034\000\069\000\070\000\071\000"

let yysindex = "\011\000\
\254\254\015\000\000\000\018\255\000\000\254\254\009\000\000\000\
\018\000\000\000\002\255\000\000\008\255\000\000\019\255\015\255\
\000\000\012\255\020\255\021\255\004\000\019\255\005\000\022\255\
\002\255\023\255\024\255\027\255\000\000\000\000\017\255\025\255\
\028\255\026\255\000\000\002\255\000\000\000\000\000\000\000\000\
\000\000\000\000\019\255\000\000\000\000\000\000\000\000\000\000\
\030\255\019\255\033\255\036\255\034\255\000\000\000\000\037\255\
\000\000\000\000\000\000\000\000\035\255\000\000\038\255\039\255\
\041\255\044\255\002\255\000\000\037\255\043\255\037\255\019\255\
\045\255\000\000\036\255\048\255\046\255\040\255\000\000\051\255\
\000\000\049\255\048\255\000\000\002\255\050\255\052\255\044\255\
\000\000\002\255\000\000\042\255\055\255\048\255\000\000\056\255\
\059\255\000\000\000\000\000\000\000\000\000\000"

let yyrindex = "\000\000\
\055\000\000\000\000\000\000\000\000\000\055\000\000\000\000\000\
\000\000\000\000\060\255\000\000\014\000\000\000\000\000\058\255\
\000\000\000\000\063\255\000\000\000\000\001\000\000\000\014\000\
\060\255\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\058\255\000\000\060\255\000\000\000\000\000\000\000\000\
\000\000\000\000\001\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\253\254\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\062\255\000\000\060\255\000\000\253\254\000\000\064\255\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\060\255\066\255\000\000\000\000\
\000\000\060\255\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000"

let yygindex = "\000\000\
\062\000\000\000\000\000\231\255\000\000\000\000\000\000\045\000\
\000\000\029\000\243\255\000\000\241\255\255\255\000\000\248\255\
\238\255\043\000\010\000\000\000\000\000\007\000\000\000"

let yytablesize = 282
let yytable = "\049\000\
\023\000\026\000\046\000\040\000\046\000\004\000\043\000\021\000\
\014\000\019\000\058\000\001\000\002\000\020\000\008\000\022\000\
\027\000\017\000\028\000\011\000\025\000\035\000\029\000\037\000\
\030\000\036\000\054\000\027\000\050\000\022\000\052\000\051\000\
\060\000\056\000\055\000\062\000\061\000\063\000\067\000\066\000\
\072\000\078\000\089\000\074\000\098\000\073\000\075\000\076\000\
\080\000\085\000\083\000\088\000\090\000\091\000\002\000\094\000\
\095\000\099\000\082\000\093\000\101\000\102\000\027\000\040\000\
\097\000\026\000\031\000\012\000\048\000\046\000\035\000\059\000\
\096\000\084\000\092\000\100\000\057\000\081\000\079\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\023\000\000\000\000\000\038\000\044\000\000\000\023\000\
\023\000\023\000\039\000\045\000\041\000\047\000\020\000\007\000\
\013\000\000\000\000\000\000\000\020\000\015\000\020\000\009\000\
\000\000\016\000"

let yycheck = "\025\000\
\000\000\015\000\006\001\000\000\000\000\008\001\010\001\000\001\
\000\000\008\001\036\000\001\000\002\000\000\000\000\000\008\001\
\002\001\000\000\004\001\002\001\002\001\010\001\008\001\003\001\
\010\001\006\001\010\001\002\001\006\001\008\001\004\001\008\001\
\003\001\006\001\010\001\003\001\050\000\002\001\002\001\006\001\
\006\001\067\000\003\001\005\001\003\001\008\001\006\001\004\001\
\006\001\002\001\006\001\006\001\002\001\005\001\000\000\006\001\
\005\001\003\001\072\000\085\000\005\001\003\001\003\001\006\001\
\090\000\003\001\005\001\006\000\024\000\006\001\005\001\043\000\
\088\000\075\000\083\000\094\000\034\000\071\000\069\000\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\255\
\255\255\001\001\255\255\255\255\001\001\001\001\255\255\007\001\
\008\001\009\001\007\001\007\001\009\001\009\001\001\001\001\001\
\008\001\255\255\255\255\255\255\007\001\004\001\009\001\009\001\
\255\255\008\001"

let yynames_const = "\
  AT\000\
  LPA\000\
  RPA\000\
  LCB\000\
  RCB\000\
  COM\000\
  TR\000\
  EOF\000\
  CMD\000\
  EOC\000\
  ERR\000\
  "

let yynames_block = "\
  STR\000\
  "

let yyact = [|
  (fun _ -> failwith "parser")
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'predicate) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : (Db.schema)) in
    Obj.repr(
# 65 "log_parser.mly"
                                ( f "signature(list)"; H.update_preds (_1::_2) )
# 216 "log_parser.ml"
               : (Db.schema)))
; (fun __caml_parser_env ->
    Obj.repr(
# 66 "log_parser.mly"
                                ( f "signature(end)"; H.update_preds [] )
# 222 "log_parser.ml"
               : (Db.schema)))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 69 "log_parser.mly"
                                ( f "predicate"; H.make_predicate _1 _3 )
# 230 "log_parser.ml"
               : 'predicate))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'slicing) in
    Obj.repr(
# 75 "log_parser.mly"
                                ( CommandTuple { c = _2; parameters = Some _3 } )
# 238 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : string) in
    Obj.repr(
# 76 "log_parser.mly"
                                ( CommandTuple { c = _2; parameters = None    } )
# 245 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'parameters) in
    Obj.repr(
# 77 "log_parser.mly"
                                ( CommandTuple { c = _2; parameters = Some _3 } )
# 253 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'slicing_test) in
    Obj.repr(
# 78 "log_parser.mly"
                                ( _2 )
# 260 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'db) in
    Obj.repr(
# 79 "log_parser.mly"
                                ( f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" _2; db = H.make_db _3; complete = true } )
# 268 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'db) in
    Obj.repr(
# 80 "log_parser.mly"
                                ( f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" _2; db = H.make_db _3; complete = false } )
# 276 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'db) in
    Obj.repr(
# 81 "log_parser.mly"
                                ( f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" _2; db = H.make_db _3; complete = false } )
# 284 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'db) in
    Obj.repr(
# 82 "log_parser.mly"
                                ( f "tsdb(last)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" _2; db = H.make_db _3; complete = false } )
# 292 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    Obj.repr(
# 83 "log_parser.mly"
                                ( f "tsdb(ts eof)"; ErrorTuple "end of file" )
# 298 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    Obj.repr(
# 84 "log_parser.mly"
                                ( f "tsdb(cmd eof)"; ErrorTuple "end of file" )
# 304 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    Obj.repr(
# 85 "log_parser.mly"
                                ( f "tsdb(eof)";    ErrorTuple "enf of file" )
# 310 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 87 "log_parser.mly"
                                ( f "tsdb(tr-err)";   H.invalid_db true )
# 317 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 88 "log_parser.mly"
                                ( f "tsdb(next-err)"; H.invalid_db false )
# 324 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 89 "log_parser.mly"
                                ( f "tsdb(next-err)"; H.invalid_db false )
# 331 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 90 "log_parser.mly"
                                ( f "tsdb(last-err)"; H.invalid_db false )
# 338 "log_parser.ml"
               : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'table) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'db) in
    Obj.repr(
# 93 "log_parser.mly"
                                ( f "db(list)"; H.add_table _2 _1 )
# 346 "log_parser.ml"
               : 'db))
; (fun __caml_parser_env ->
    Obj.repr(
# 94 "log_parser.mly"
                                ( f "db()"; [] )
# 352 "log_parser.ml"
               : 'db))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : string) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'relation) in
    Obj.repr(
# 97 "log_parser.mly"
                                ( f "table";
                                  try
                                    H.make_table _1 _2
                                  with (Failure str) as e ->
                                    if !Misc.ignore_parse_errors then
                                      begin
                                        prerr_endline str;
                                        raise Parsing.Parse_error
                                      end
                                    else
                                      raise e
                                )
# 371 "log_parser.ml"
               : 'table))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'tuple) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'relation) in
    Obj.repr(
# 111 "log_parser.mly"
                                ( f "relation(list)"; _1::_2 )
# 379 "log_parser.ml"
               : 'relation))
; (fun __caml_parser_env ->
    Obj.repr(
# 112 "log_parser.mly"
                                ( f "relation(end)"; [] )
# 385 "log_parser.ml"
               : 'relation))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 115 "log_parser.mly"
                                ( f "tuple"; _2 )
# 392 "log_parser.ml"
               : 'tuple))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'fields) in
    Obj.repr(
# 119 "log_parser.mly"
                                ( f "fields(list)"; _1::_3 )
# 400 "log_parser.ml"
               : 'fields))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 120 "log_parser.mly"
                                ( f "fields(end)"; [_1] )
# 407 "log_parser.ml"
               : 'fields))
; (fun __caml_parser_env ->
    Obj.repr(
# 121 "log_parser.mly"
                                ( f "fields()"; [] )
# 413 "log_parser.ml"
               : 'fields))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 5 : 'heavies) in
    let _4 = (Parsing.peek_val __caml_parser_env 3 : 'shares_seeds) in
    let _6 = (Parsing.peek_val __caml_parser_env 1 : 'shares_seeds) in
    Obj.repr(
# 125 "log_parser.mly"
                                ( H.return_split_restore_parameters _2 (H.convert_nested_str_list _4) (H.convert_nested_str_list _6) )
# 422 "log_parser.ml"
               : 'slicing))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'heavy) in
    Obj.repr(
# 128 "log_parser.mly"
                                ( _2 )
# 429 "log_parser.ml"
               : 'heavies))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'tupleseq) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'heavy) in
    Obj.repr(
# 130 "log_parser.mly"
                                ( _1::_3 )
# 437 "log_parser.ml"
               : 'heavy))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'tupleseq) in
    Obj.repr(
# 131 "log_parser.mly"
                                ( [_1] )
# 444 "log_parser.ml"
               : 'heavy))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'nested_field) in
    Obj.repr(
# 133 "log_parser.mly"
                                      ( (int_of_string _2), _4 )
# 452 "log_parser.ml"
               : 'tupleseq))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'nested_fields) in
    Obj.repr(
# 136 "log_parser.mly"
                                ( _2 )
# 459 "log_parser.ml"
               : 'shares_seeds))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'nested_field) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'nested_fields) in
    Obj.repr(
# 138 "log_parser.mly"
                                        ( _1::_3 )
# 467 "log_parser.ml"
               : 'nested_fields))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'nested_field) in
    Obj.repr(
# 139 "log_parser.mly"
                                ( [_1] )
# 474 "log_parser.ml"
               : 'nested_fields))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 141 "log_parser.mly"
                                ( _2 )
# 481 "log_parser.ml"
               : 'nested_field))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 145 "log_parser.mly"
                                ( Argument   _1    )
# 488 "log_parser.ml"
               : 'parameters))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'keys) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'group) in
    Obj.repr(
# 146 "log_parser.mly"
                                ( H.make_split _1 _3 )
# 496 "log_parser.ml"
               : 'parameters))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'key) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'keys) in
    Obj.repr(
# 148 "log_parser.mly"
                                ( (H.make_key _1)::_2)
# 504 "log_parser.ml"
               : 'keys))
; (fun __caml_parser_env ->
    Obj.repr(
# 149 "log_parser.mly"
                                ( [] )
# 510 "log_parser.ml"
               : 'keys))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : string) in
    Obj.repr(
# 151 "log_parser.mly"
                                ( _2 )
# 517 "log_parser.ml"
               : 'key))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'subgroup) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'group) in
    Obj.repr(
# 154 "log_parser.mly"
                                ( H.make_group _2 _1 )
# 525 "log_parser.ml"
               : 'group))
; (fun __caml_parser_env ->
    Obj.repr(
# 155 "log_parser.mly"
                                ( [] )
# 531 "log_parser.ml"
               : 'group))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 4 : 'constraintList) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 158 "log_parser.mly"
                                            ( H.make_subgroup _1 _4 )
# 539 "log_parser.ml"
               : 'subgroup))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'constraintSet) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'constraintList) in
    Obj.repr(
# 161 "log_parser.mly"
                                          ( _1::_2  )
# 547 "log_parser.ml"
               : 'constraintList))
; (fun __caml_parser_env ->
    Obj.repr(
# 162 "log_parser.mly"
                                          ( [] )
# 553 "log_parser.ml"
               : 'constraintList))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 164 "log_parser.mly"
                                          ( _2 )
# 560 "log_parser.ml"
               : 'constraintSet))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 5 : 'tuple) in
    let _4 = (Parsing.peek_val __caml_parser_env 3 : 'tuple) in
    let _6 = (Parsing.peek_val __caml_parser_env 1 : 'tuple) in
    Obj.repr(
# 167 "log_parser.mly"
                                          ( H.make_slicing_test _2 _4 _6)
# 569 "log_parser.ml"
               : 'slicing_test))
(* Entry signature *)
; (fun __caml_parser_env -> raise (Parsing.YYexit (Parsing.peek_val __caml_parser_env 0)))
(* Entry tsdb *)
; (fun __caml_parser_env -> raise (Parsing.YYexit (Parsing.peek_val __caml_parser_env 0)))
|]
let yytables =
  { Parsing.actions=yyact;
    Parsing.transl_const=yytransl_const;
    Parsing.transl_block=yytransl_block;
    Parsing.lhs=yylhs;
    Parsing.len=yylen;
    Parsing.defred=yydefred;
    Parsing.dgoto=yydgoto;
    Parsing.sindex=yysindex;
    Parsing.rindex=yyrindex;
    Parsing.gindex=yygindex;
    Parsing.tablesize=yytablesize;
    Parsing.table=yytable;
    Parsing.check=yycheck;
    Parsing.error_function=parse_error;
    Parsing.names_const=yynames_const;
    Parsing.names_block=yynames_block }
let signature (lexfun : Lexing.lexbuf -> token) (lexbuf : Lexing.lexbuf) =
   (Parsing.yyparse yytables 1 lexfun lexbuf : (Db.schema))
let tsdb (lexfun : Lexing.lexbuf -> token) (lexbuf : Lexing.lexbuf) =
   (Parsing.yyparse yytables 2 lexfun lexbuf : (Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed))
