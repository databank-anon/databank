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

open Parsing;;
let _ = parse_error;;
# 43 "lab_log_parser.mly"
module H = Log_parser_helper.LabelledLog_parser_helper	
let f = H.f
# 25 "lab_log_parser.ml"
let yytransl_const = [|
  257 (* AT *);
  258 (* LPA *);
  259 (* RPA *);
  260 (* LCB *);
  261 (* RCB *);
  262 (* LSB *);
  263 (* RSB *);
  264 (* COM *);
  265 (* TR *);
  266 (* LABELS *);
  267 (* NULL *);
    0 (* EOF *);
  269 (* CMD *);
  270 (* EOC *);
  271 (* ERR *);
    0|]

let yytransl_block = [|
  268 (* STR *);
    0|]

let yylhs = "\255\255\
\001\000\001\000\003\000\002\000\002\000\002\000\002\000\002\000\
\002\000\002\000\002\000\002\000\002\000\002\000\002\000\002\000\
\002\000\007\000\007\000\009\000\010\000\010\000\010\000\011\000\
\012\000\012\000\012\000\012\000\012\000\004\000\004\000\004\000\
\005\000\013\000\015\000\015\000\016\000\014\000\018\000\018\000\
\017\000\006\000\006\000\019\000\019\000\021\000\020\000\020\000\
\022\000\023\000\023\000\024\000\008\000\008\000\025\000\025\000\
\000\000\000\000"

let yylen = "\002\000\
\002\000\000\000\004\000\004\000\003\000\004\000\005\000\005\000\
\005\000\005\000\002\000\002\000\001\000\004\000\004\000\004\000\
\004\000\002\000\000\000\002\000\002\000\002\000\000\000\003\000\
\004\000\004\000\002\000\002\000\000\000\003\000\001\000\000\000\
\007\000\003\000\003\000\001\000\005\000\003\000\003\000\001\000\
\003\000\001\000\003\000\002\000\000\000\003\000\002\000\000\000\
\005\000\002\000\000\000\003\000\003\000\000\000\003\000\001\000\
\002\000\002\000"

let yydefred = "\000\000\
\000\000\000\000\000\000\000\000\057\000\000\000\000\000\013\000\
\000\000\058\000\000\000\001\000\000\000\011\000\000\000\012\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\042\000\005\000\000\000\000\000\000\000\000\000\000\000\003\000\
\015\000\014\000\017\000\016\000\000\000\000\000\020\000\000\000\
\000\000\000\000\018\000\000\000\000\000\000\000\004\000\006\000\
\000\000\044\000\030\000\000\000\000\000\000\000\022\000\021\000\
\000\000\000\000\008\000\007\000\010\000\009\000\046\000\000\000\
\000\000\000\000\000\000\000\000\043\000\000\000\000\000\000\000\
\000\000\000\000\024\000\000\000\053\000\000\000\034\000\000\000\
\000\000\000\000\000\000\047\000\000\000\050\000\000\000\000\000\
\055\000\000\000\035\000\000\000\000\000\000\000\000\000\052\000\
\000\000\025\000\026\000\000\000\000\000\000\000\038\000\000\000\
\000\000\037\000\041\000\039\000\033\000\049\000"

let yydgoto = "\003\000\
\005\000\010\000\006\000\018\000\027\000\028\000\021\000\042\000\
\022\000\039\000\040\000\054\000\046\000\082\000\065\000\066\000\
\093\000\094\000\029\000\069\000\030\000\070\000\071\000\072\000\
\058\000"

let yysindex = "\025\000\
\253\254\021\000\000\000\011\255\000\000\253\254\011\000\000\000\
\012\000\000\000\012\255\000\000\010\255\000\000\002\255\000\000\
\027\255\025\255\003\000\005\255\030\255\026\255\028\255\035\255\
\000\000\000\000\029\255\031\255\033\255\040\255\012\255\000\000\
\000\000\000\000\000\000\000\000\020\255\030\255\000\000\005\255\
\032\255\017\000\000\000\043\255\045\255\041\255\000\000\000\000\
\046\255\000\000\000\000\030\255\030\255\047\255\000\000\000\000\
\044\255\048\255\000\000\000\000\000\000\000\000\000\000\039\255\
\049\255\050\255\052\255\012\255\000\000\046\255\051\255\046\255\
\054\255\055\255\000\000\032\255\000\000\056\255\000\000\045\255\
\058\255\057\255\064\255\000\000\066\255\000\000\020\255\020\255\
\000\000\058\255\000\000\012\255\061\255\065\255\052\255\000\000\
\012\255\000\000\000\000\068\255\069\255\058\255\000\000\070\255\
\071\255\000\000\000\000\000\000\000\000\000\000"

let yyrindex = "\000\000\
\053\000\000\000\000\000\000\000\000\000\053\000\000\000\000\000\
\000\000\000\000\025\255\000\000\002\000\000\000\072\255\000\000\
\073\255\000\000\000\000\001\000\018\000\002\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\072\255\025\255\000\000\
\000\000\000\000\000\000\000\000\074\255\008\000\000\000\001\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\015\255\000\000\000\000\022\255\022\255\000\000\000\000\000\000\
\075\255\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\076\255\000\000\025\255\000\000\015\255\000\000\077\255\
\080\255\081\255\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\074\255\074\255\
\000\000\000\000\000\000\025\255\082\255\000\000\000\000\000\000\
\025\255\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000"

let yygindex = "\000\000\
\051\000\000\000\000\000\225\255\000\000\000\000\056\000\223\255\
\000\000\033\000\000\000\202\255\000\000\240\255\006\000\000\000\
\254\255\243\255\060\000\022\000\000\000\000\000\019\000\000\000\
\020\000"

let yytablesize = 290
let yytable = "\051\000\
\023\000\019\000\035\000\023\000\055\000\024\000\037\000\054\000\
\004\000\019\000\014\000\016\000\011\000\025\000\038\000\026\000\
\061\000\054\000\073\000\074\000\008\000\020\000\051\000\017\000\
\054\000\001\000\002\000\032\000\048\000\054\000\052\000\053\000\
\098\000\099\000\031\000\041\000\083\000\020\000\045\000\044\000\
\049\000\023\000\047\000\057\000\048\000\063\000\064\000\068\000\
\067\000\075\000\078\000\076\000\002\000\079\000\077\000\081\000\
\012\000\080\000\085\000\092\000\101\000\087\000\088\000\090\000\
\095\000\105\000\096\000\097\000\102\000\103\000\106\000\107\000\
\056\000\110\000\109\000\031\000\029\000\043\000\104\000\045\000\
\036\000\056\000\027\000\028\000\051\000\091\000\040\000\100\000\
\108\000\050\000\086\000\084\000\000\000\000\000\000\000\089\000\
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
\000\000\023\000\019\000\033\000\000\000\000\000\023\000\019\000\
\054\000\023\000\019\000\034\000\023\000\023\000\019\000\036\000\
\054\000\059\000\054\000\054\000\054\000\007\000\013\000\015\000\
\000\000\060\000\054\000\000\000\000\000\062\000\054\000\000\000\
\000\000\009\000"

let yycheck = "\031\000\
\000\000\000\000\000\000\002\001\038\000\004\001\002\001\000\000\
\012\001\000\001\000\000\000\000\002\001\012\001\010\001\014\001\
\000\000\000\000\052\000\053\000\000\000\012\001\008\001\012\001\
\003\001\001\000\002\000\003\001\014\001\008\001\011\001\012\001\
\087\000\088\000\008\001\006\001\068\000\012\001\004\001\012\001\
\008\001\002\001\014\001\012\001\014\001\003\001\002\001\002\001\
\008\001\003\001\012\001\008\001\000\000\005\001\007\001\004\001\
\006\000\008\001\008\001\002\001\092\000\008\001\008\001\008\001\
\008\001\097\000\003\001\002\001\008\001\005\001\003\001\003\001\
\040\000\003\001\005\001\003\001\003\001\022\000\095\000\008\001\
\005\001\007\001\003\001\003\001\008\001\080\000\005\001\090\000\
\102\000\030\000\072\000\070\000\255\255\255\255\255\255\076\000\
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
\255\255\001\001\001\001\001\001\255\255\255\255\006\001\006\001\
\001\001\009\001\009\001\009\001\012\001\013\001\013\001\013\001\
\009\001\001\001\001\001\012\001\013\001\001\001\012\001\012\001\
\255\255\009\001\009\001\255\255\255\255\013\001\013\001\255\255\
\255\255\013\001"

let yynames_const = "\
  AT\000\
  LPA\000\
  RPA\000\
  LCB\000\
  RCB\000\
  LSB\000\
  RSB\000\
  COM\000\
  TR\000\
  LABELS\000\
  NULL\000\
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
# 65 "lab_log_parser.mly"
                                ( f "signature(list)"; H.update_preds (_1::_2) )
# 237 "lab_log_parser.ml"
               : (Db.schema)))
; (fun __caml_parser_env ->
    Obj.repr(
# 66 "lab_log_parser.mly"
                                ( f "signature(end)"; H.update_preds [] )
# 243 "lab_log_parser.ml"
               : (Db.schema)))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 69 "lab_log_parser.mly"
                                ( f "predicate"; H.make_predicate _1 _3 )
# 251 "lab_log_parser.ml"
               : 'predicate))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'slicing) in
    Obj.repr(
# 72 "lab_log_parser.mly"
                                ( CommandTuple { c = _2; parameters = Some _3 } )
# 259 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : string) in
    Obj.repr(
# 73 "lab_log_parser.mly"
                                ( CommandTuple { c = _2; parameters = None    } )
# 266 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'parameters) in
    Obj.repr(
# 74 "lab_log_parser.mly"
                                ( CommandTuple { c = _2; parameters = Some _3 } )
# 274 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 2 : 'db) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'labels) in
    Obj.repr(
# 76 "lab_log_parser.mly"
                                ( f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Lab_log_parser" _2; db = H.make_db ~labels:_4 _3; complete = true } )
# 283 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 2 : 'db) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'labels) in
    Obj.repr(
# 77 "lab_log_parser.mly"
                                ( f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Lab_log_parser" _2; db = H.make_db ~labels:_4 _3; complete = false } )
# 292 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 2 : 'db) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'labels) in
    Obj.repr(
# 78 "lab_log_parser.mly"
                                ( f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Lab_log_parser" _2; db = H.make_db ~labels:_4 _3; complete = false } )
# 301 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 2 : 'db) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'labels) in
    Obj.repr(
# 79 "lab_log_parser.mly"
                                ( f "tsdb(last)"; DataTuple { ts = MFOTL.ts_of_string "Lab_log_parser" _2; db = H.make_db ~labels:_4 _3; complete = false } )
# 310 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    Obj.repr(
# 80 "lab_log_parser.mly"
                                ( f "tsdb(ts eof)"; ErrorTuple "end of file" )
# 316 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    Obj.repr(
# 81 "lab_log_parser.mly"
                                ( f "tsdb(cmd eof)"; ErrorTuple "end of file" )
# 322 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    Obj.repr(
# 82 "lab_log_parser.mly"
                                ( f "tsdb(eof)";    ErrorTuple "enf of file" )
# 328 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 83 "lab_log_parser.mly"
                                ( f "tsdb(tr-err)";   H.invalid_db true )
# 335 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 84 "lab_log_parser.mly"
                                ( f "tsdb(next-err)"; H.invalid_db false )
# 342 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 85 "lab_log_parser.mly"
                                ( f "tsdb(next-err)"; H.invalid_db false )
# 349 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 86 "lab_log_parser.mly"
                                ( f "tsdb(last-err)"; H.invalid_db false )
# 356 "lab_log_parser.ml"
               : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed)))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'table) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'db) in
    Obj.repr(
# 89 "lab_log_parser.mly"
                                ( f "db(list)"; H.add_table _2 _1 )
# 364 "lab_log_parser.ml"
               : 'db))
; (fun __caml_parser_env ->
    Obj.repr(
# 90 "lab_log_parser.mly"
                                ( f "db()"; [] )
# 370 "lab_log_parser.ml"
               : 'db))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : string) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'relation) in
    Obj.repr(
# 93 "lab_log_parser.mly"
                                ( f "table";
                                  try
                                    H.make_table _1 ~labels:(snd _2) (fst _2)
                                  with (Failure str) as e ->
                                    if !Misc.ignore_parse_errors then
                                      begin
                                        prerr_endline str;
                                        raise Parsing.Parse_error
                                      end
                                    else
                                      raise e
                                )
# 389 "lab_log_parser.ml"
               : 'table))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'tuple) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'relation) in
    Obj.repr(
# 107 "lab_log_parser.mly"
                                ( f "relation(list)"; _1::(fst _2), snd _2 )
# 397 "lab_log_parser.ml"
               : 'relation))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'labels) in
    Obj.repr(
# 108 "lab_log_parser.mly"
                                ( f "relation(end+labels)"; [], _2 )
# 404 "lab_log_parser.ml"
               : 'relation))
; (fun __caml_parser_env ->
    Obj.repr(
# 109 "lab_log_parser.mly"
                                ( f "relation(end)"; [], [] )
# 410 "lab_log_parser.ml"
               : 'relation))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'tuple_fields) in
    Obj.repr(
# 112 "lab_log_parser.mly"
                                ( f "tuple"; _2 )
# 417 "lab_log_parser.ml"
               : 'tuple))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 2 : 'labels) in
    let _4 = (Parsing.peek_val __caml_parser_env 0 : 'tuple_fields) in
    Obj.repr(
# 117 "lab_log_parser.mly"
                                ( f "fields(list+labels)"; (None,_2)::_4 )
# 425 "lab_log_parser.ml"
               : 'tuple_fields))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _2 = (Parsing.peek_val __caml_parser_env 2 : 'labels) in
    let _4 = (Parsing.peek_val __caml_parser_env 0 : 'tuple_fields) in
    Obj.repr(
# 119 "lab_log_parser.mly"
                                ( f "fields(list+labels)"; (Some _1,_2)::_4 )
# 434 "lab_log_parser.ml"
               : 'tuple_fields))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'labels) in
    Obj.repr(
# 120 "lab_log_parser.mly"
                                ( f "fields(end+labels)"; [None,_2] )
# 441 "lab_log_parser.ml"
               : 'tuple_fields))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : string) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'labels) in
    Obj.repr(
# 121 "lab_log_parser.mly"
                                ( f "fields(end+labels)"; [Some _1,_2] )
# 449 "lab_log_parser.ml"
               : 'tuple_fields))
; (fun __caml_parser_env ->
    Obj.repr(
# 122 "lab_log_parser.mly"
                                ( f "fields()"; [] )
# 455 "lab_log_parser.ml"
               : 'tuple_fields))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'fields) in
    Obj.repr(
# 125 "lab_log_parser.mly"
                                ( f "fields(list)"; _1::_3 )
# 463 "lab_log_parser.ml"
               : 'fields))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 126 "lab_log_parser.mly"
                                ( f "fields(end)"; [_1] )
# 470 "lab_log_parser.ml"
               : 'fields))
; (fun __caml_parser_env ->
    Obj.repr(
# 127 "lab_log_parser.mly"
                                ( f "fields()"; [] )
# 476 "lab_log_parser.ml"
               : 'fields))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 5 : 'heavies) in
    let _4 = (Parsing.peek_val __caml_parser_env 3 : 'shares_seeds) in
    let _6 = (Parsing.peek_val __caml_parser_env 1 : 'shares_seeds) in
    Obj.repr(
# 131 "lab_log_parser.mly"
                                ( H.return_split_restore_parameters _2 (H.convert_nested_str_list _4) (H.convert_nested_str_list _6) )
# 485 "lab_log_parser.ml"
               : 'slicing))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'heavy) in
    Obj.repr(
# 134 "lab_log_parser.mly"
                                ( _2 )
# 492 "lab_log_parser.ml"
               : 'heavies))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'tupleseq) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'heavy) in
    Obj.repr(
# 136 "lab_log_parser.mly"
                                ( _1::_3 )
# 500 "lab_log_parser.ml"
               : 'heavy))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'tupleseq) in
    Obj.repr(
# 137 "lab_log_parser.mly"
                                ( [_1] )
# 507 "lab_log_parser.ml"
               : 'heavy))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'nested_field) in
    Obj.repr(
# 139 "lab_log_parser.mly"
                                      ( (int_of_string _2), _4 )
# 515 "lab_log_parser.ml"
               : 'tupleseq))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'nested_fields) in
    Obj.repr(
# 142 "lab_log_parser.mly"
                                ( _2 )
# 522 "lab_log_parser.ml"
               : 'shares_seeds))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'nested_field) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'nested_fields) in
    Obj.repr(
# 144 "lab_log_parser.mly"
                                        ( _1::_3 )
# 530 "lab_log_parser.ml"
               : 'nested_fields))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'nested_field) in
    Obj.repr(
# 145 "lab_log_parser.mly"
                                ( [_1] )
# 537 "lab_log_parser.ml"
               : 'nested_fields))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 147 "lab_log_parser.mly"
                                ( _2 )
# 544 "lab_log_parser.ml"
               : 'nested_field))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 151 "lab_log_parser.mly"
                                ( Argument   _1    )
# 551 "lab_log_parser.ml"
               : 'parameters))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'keys) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'group) in
    Obj.repr(
# 152 "lab_log_parser.mly"
                                ( H.make_split _1 _3 )
# 559 "lab_log_parser.ml"
               : 'parameters))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'key) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'keys) in
    Obj.repr(
# 154 "lab_log_parser.mly"
                                ( (H.make_key _1)::_2)
# 567 "lab_log_parser.ml"
               : 'keys))
; (fun __caml_parser_env ->
    Obj.repr(
# 155 "lab_log_parser.mly"
                                ( [] )
# 573 "lab_log_parser.ml"
               : 'keys))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : string) in
    Obj.repr(
# 157 "lab_log_parser.mly"
                                ( _2 )
# 580 "lab_log_parser.ml"
               : 'key))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'subgroup) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'group) in
    Obj.repr(
# 160 "lab_log_parser.mly"
                                ( H.make_group _2 _1 )
# 588 "lab_log_parser.ml"
               : 'group))
; (fun __caml_parser_env ->
    Obj.repr(
# 161 "lab_log_parser.mly"
                                ( [] )
# 594 "lab_log_parser.ml"
               : 'group))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 4 : 'constraintList) in
    let _4 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 164 "lab_log_parser.mly"
                                            ( H.make_subgroup _1 _4 )
# 602 "lab_log_parser.ml"
               : 'subgroup))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'constraintSet) in
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'constraintList) in
    Obj.repr(
# 167 "lab_log_parser.mly"
                                          ( _1::_2  )
# 610 "lab_log_parser.ml"
               : 'constraintList))
; (fun __caml_parser_env ->
    Obj.repr(
# 168 "lab_log_parser.mly"
                                          ( [] )
# 616 "lab_log_parser.ml"
               : 'constraintList))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'fields) in
    Obj.repr(
# 170 "lab_log_parser.mly"
                                          ( _2 )
# 623 "lab_log_parser.ml"
               : 'constraintSet))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 1 : 'cslabels) in
    Obj.repr(
# 176 "lab_log_parser.mly"
                                ( f "labels(list)"; _2 )
# 630 "lab_log_parser.ml"
               : 'labels))
; (fun __caml_parser_env ->
    Obj.repr(
# 177 "lab_log_parser.mly"
                                ( f "labels()"; [] )
# 636 "lab_log_parser.ml"
               : 'labels))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'cslabels) in
    Obj.repr(
# 180 "lab_log_parser.mly"
                                ( f "cslabels(list)"; _1::_3 )
# 644 "lab_log_parser.ml"
               : 'cslabels))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 181 "lab_log_parser.mly"
                                ( f "cslabels(end)"; [_1] )
# 651 "lab_log_parser.ml"
               : 'cslabels))
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
   (Parsing.yyparse yytables 2 lexfun lexbuf : (Log_parser_helper.LabelledLog_parser_helper.Helper.parser_feed))
