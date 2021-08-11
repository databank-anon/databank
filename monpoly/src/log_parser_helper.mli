module type LOG_PARSER_HELPER = sig

  module Helper: Helper.HELPER
  module Filter_rel: Filter_rel.FILTER_REL with module Helper = Helper

  open Helper

  val f: string -> unit

  val update_preds: (string * (Predicate.var * Predicate.tcst) list) list
                    -> (string * (Predicate.var * Predicate.tcst) list) list

  val make_predicate: 'a -> string list -> 'a * (string * Predicate.tcst) list

  val make_table:  Predicate.var -> ?labels:Labels.label list ->
           Db.Tuple.ituple list ->
           (Predicate.var * (Predicate.var * Predicate.tcst) list) *
           Helper.Db.Relation.relation

  val add_table: ('a * Helper.Db.Relation.relation) list
                 -> ('a * Helper.Db.Relation.relation)
                 -> ('a * Helper.Db.Relation.relation) list

  val make_db: ?labels:Labels.label list -> (Table.schema * Helper.Db.Relation.relation) list -> Helper.Db.db
  (* let parse_error str = () *)

  val invalid_db: bool -> Helper.parser_feed

  val make_slicing_test: Predicate.var list -> Predicate.var list -> Predicate.var list -> Helper.parser_feed

  val return_split_restore_parameters: Domain_set.heavy_unproc list
                                       -> int array array -> int array array -> Helper.commandParameter

  val convert_nested_str_list: Predicate.var list list -> int array array

  val make_split: (Predicate.var * Predicate.tcst) list
                  -> (Predicate.var list list * int list) list
                  -> Helper.commandParameter

  val make_group: 'a list -> 'a -> 'a list

  val make_subgroup: 'a -> Predicate.var list -> 'a * int list
      
  val make_key: Predicate.var -> Predicate.var * Predicate.tcst

end
                                  
module MakeLog_parser_helper: functor (H: Helper.HELPER) -> LOG_PARSER_HELPER with module Helper = H

module StandardLog_parser_helper: LOG_PARSER_HELPER with module Helper = Helper.StandardHelper
module LabelledLog_parser_helper: LOG_PARSER_HELPER with module Helper = Helper.LabelledHelper
