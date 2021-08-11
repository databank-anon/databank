/*
 * This file is part of MONPOLY.
 *
 * Copyright © 2011 Nokia Corporation and/or its subsidiary(-ies).
 * Contact:  Nokia Corporation (Debmalya Biswas: debmalya.biswas@nokia.com)
 *
 * Copyright (C) 2012 ETH Zurich.
 * Contact:  ETH Zurich (Eugen Zalinescu: eugen.zalinescu@inf.ethz.ch)
 *
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation, version 2.1 of the
 * License.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library. If not, see
 * http://www.gnu.org/licenses/lgpl-2.1.html.
 *
 * As a special exception to the GNU Lesser General Public License,
 * you may link, statically or dynamically, a "work that uses the
 * Library" with a publicly distributed version of the Library to
 * produce an executable file containing portions of the Library, and
 * distribute that executable file under terms of your choice, without
 * any of the additional requirements listed in clause 6 of the GNU
 * Lesser General Public License. By "a publicly distributed version
 * of the Library", we mean either the unmodified Library as
 * distributed by Nokia, or a modified version of the Library that is
 * distributed under the conditions defined in clause 3 of the GNU
 * Lesser General Public License. This exception does not however
 * invalidate any other reasons why the executable file might be
 * covered by the GNU Lesser General Public License.
 */



%{
module H = Log_parser_helper.StandardLog_parser_helper
let f = H.f
%}


%token AT LPA RPA LCB RCB COM TR
%token <string> STR
%token EOF
%token CMD
%token EOC
%token ERR

%start signature
%type <(Db.schema)> signature

%start tsdb
%type <(Log_parser_helper.StandardLog_parser_helper.Helper.parser_feed)> tsdb

%%


signature:
      | predicate signature     { f "signature(list)"; H.update_preds ($1::$2) }
      |                         { f "signature(end)"; H.update_preds [] }

predicate:
      | STR LPA fields RPA      { f "predicate"; H.make_predicate $1 $3 }




tsdb:
      | CMD STR slicing EOC     { CommandTuple { c = $2; parameters = Some $3 } }
      | CMD STR EOC             { CommandTuple { c = $2; parameters = None    } }
      | CMD STR parameters EOC  { CommandTuple { c = $2; parameters = Some $3 } }
      | CMD slicing_test EOC    { $2 }
      | AT STR db TR            { f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" $2; db = H.make_db $3; complete = true } }
      | AT STR db AT            { f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" $2; db = H.make_db $3; complete = false } }
      | AT STR db CMD           { f "tsdb(next)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" $2; db = H.make_db $3; complete = false } }
      | AT STR db EOF           { f "tsdb(last)"; DataTuple { ts = MFOTL.ts_of_string "Log_parser" $2; db = H.make_db $3; complete = false } }
      | AT EOF                  { f "tsdb(ts eof)"; ErrorTuple "end of file" }
      | CMD EOF                 { f "tsdb(cmd eof)"; ErrorTuple "end of file" }
      | EOF                     { f "tsdb(eof)";    ErrorTuple "enf of file" }

      | AT STR error TR         { f "tsdb(tr-err)";   H.invalid_db true }
      | AT STR error AT         { f "tsdb(next-err)"; H.invalid_db false }
      | AT STR error CMD        { f "tsdb(next-err)"; H.invalid_db false }
      | AT STR error EOF        { f "tsdb(last-err)"; H.invalid_db false }

db:
      | table db                { f "db(list)"; H.add_table $2 $1 }
      |                         { f "db()"; [] }

table:
      | STR relation            { f "table";
                                  try
                                    H.make_table $1 $2
                                  with (Failure str) as e ->
                                    if !Misc.ignore_parse_errors then
                                      begin
                                        prerr_endline str;
                                        raise Parsing.Parse_error
                                      end
                                    else
                                      raise e
                                }

relation:
      | tuple relation          { f "relation(list)"; $1::$2 }
      |                         { f "relation(end)"; [] }

tuple:
      | LPA fields RPA          { f "tuple"; $2 }


fields:
      | STR COM fields          { f "fields(list)"; $1::$3 }
      | STR                     { f "fields(end)"; [$1] }
      |                         { f "fields()"; [] }
  
slicing: 
      | LCB heavies COM shares_seeds COM shares_seeds RCB 
                                { H.return_split_restore_parameters $2 (H.convert_nested_str_list $4) (H.convert_nested_str_list $6) }

heavies:
      | LCB heavy RCB           { $2 }
heavy:
      | tupleseq COM heavy      { $1::$3 }
      | tupleseq                { [$1] }
tupleseq:
      | LPA STR COM nested_field RPA  { (int_of_string $2), $4 }

shares_seeds:
      | LCB nested_fields RCB   { $2 }
nested_fields:
      | nested_field COM nested_fields  { $1::$3 }  
      | nested_field            { [$1] }
nested_field:
      | LPA fields RPA          { $2 }


parameters:
      | STR                     { Argument   $1    }
      | keys COM group          { H.make_split $1 $3 }
keys: 
      | key      keys           { (H.make_key $1)::$2}
      |                         { [] }
key:
      | LPA STR RPA             { $2 }

group:
      | subgroup group          { H.make_group $2 $1 } 
      |                         { [] }
    
subgroup:
      | constraintList COM LPA fields RPA   { H.make_subgroup $1 $4 }

constraintList:
      | constraintSet constraintList      { $1::$2  }
      |                                   { [] }
constraintSet:
      | LPA fields RPA                    { $2 }

slicing_test:
      | LCB tuple COM tuple COM tuple RCB { H.make_slicing_test $2 $4 $6}
