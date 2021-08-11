(*
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
 *)


open Misc
open Predicate
open MFOTL
open Domain_set

module Helper' = Helper

module type LOG_PARSER_HELPER = sig

  module Helper: Helper'.HELPER
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

module MakeLog_parser_helper (H: Helper.HELPER) = struct

  module Helper = H
  module Filter_rel = Filter_rel.MakeFilter_rel(H)

  open Helper

  let f str =
    if Misc.debugging Dbg_log then
      Printf.printf "[Log_parser_helper] %s with start=%d and end=%d\n%!" str (Parsing.symbol_start()) (Parsing.symbol_end())
    else
      ()

  let preds = ref []

  let update_slicer_preds e =
    Domain_set.predicates := e :: !Domain_set.predicates

  let update_preds l =
    preds := l;
    List.iter (fun e -> update_slicer_preds (Domain_set.convert_predicate e)) l;
    l

  let get_type = function
    | "int" -> TInt
    | "string" -> TStr
    | "float" -> TFloat
    | t -> let spos = Parsing.symbol_start_pos() in
           let str = Printf.sprintf
             "[Log_parser_helper.check_fields] Unknown type %s in signature at line %d."
             t spos.Lexing.pos_lnum
           in
           failwith str

  let make_predicate p attr = 
    let tl =
      List.map
        (fun str ->
          match Misc.nsplit str ":" with
          | [] -> failwith "[Log_parser_helper.make_predicate] internal error"
          | [type_str] -> "", get_type type_str
          | var_name :: type_str :: _ ->
             var_name, get_type type_str
        )
        attr
    in
    (p, tl)


  let get_schema pname =
    try
      List.find (fun (p, _) -> pname = p) !preds
    with Not_found ->
      let spos = Parsing.symbol_start_pos() in
      let str = Printf.sprintf
        "[Log_parser_helper.get_schema] The predicate %s at line %d was not found in the signature."
        pname spos.Lexing.pos_lnum
      in
      failwith str

  let process_tuple pname attr ar t =
    if List.length t = ar then
      try
      	Db.Tuple.make_tuple2 t attr
      with Db.Tuple.Type_error str_err ->
        let str = Printf.sprintf
          "[Log_parser_helper.make_tuple] Wrong type for predicate %s at line %d in the log file: %s"
          pname (Parsing.symbol_start_pos()).Lexing.pos_lnum str_err
        in
        failwith str
    else
      let str = Printf.sprintf
        "[Log_parser_helper.make_tuple] Wrong tuple length for predicate %s at line %d in the log file."
        pname (Parsing.symbol_start_pos()).Lexing.pos_lnum
      in
      failwith str

  let process_tuples s tuples =
    let pname, attr = s in
    let ar = List.length attr in
    (* we only reverse because [rev_map] is tail-recursive, while [map] is not *)
    List.rev_map (process_tuple pname attr ar) tuples

  (* a tuple is a list of strings here, not a value of type Tuple.tuple *)
  let make_table p ?labels:((labels:Labels.label list)=[]) tuples =
    let s = get_schema p in
    let rel =
      if !Filter_rel.enabled then
        if Filter_rel.rel_OK p then
	  List.filter (Filter_rel.tuple_OK p) (process_tuples s tuples)
        else
          []
      else
        process_tuples s tuples
    in
    let labs = Labels.LabelSet.of_list labels in
    s, (Db.Relation.make_relation ~labs rel)

  (* db is seen here as an association list *)
  let add_table db (s,rel) =
    (*if Db.Relation.is_empty rel then (* removed as this risked erasing labels *)
      db
    else*) if List.mem_assoc s db then
      let rel' = List.assoc s db in
      let new_rel = Db.Relation.union rel rel' in
      (s,new_rel)::(List.remove_assoc s db)
    else
      (s,rel)::db

  let make_db ?labels:(labels=[]) db =
    Db.make_db
      (List.map
         (fun (s,r) -> Db.Table.make_table s (Db.Relation.adopt_labels r (Labels.LabelSet.of_list labels))) db)

  (* let parse_error str = () *)

  let invalid_db complete =
    if !Misc.ignore_parse_errors then
      DataTuple { ts = ts_invalid; db = Db.make_db []; complete }
    else
      raise Parsing.Parse_error


(*
  Below functions are only relevant for the manual specification of the mappings from values to state partitions
  in the split_and_save command. Useful for manual testing involving small sample log files.

  Example: 
  > split_state (a:string)(f:int)(m:string),  (Alice,Charlie)(160,187,152)(Mallory),   (0,2)
                                              (Bob)(163)(Merlin),                      (1)
  <
 *)
let make_slicing_test vars tuple destinations =
  let dest = Array.of_list (List.map (fun e -> int_of_string e) destinations) in
  SlicingTestTuple { vars = vars; tuple = tuple; output = dest }

let get_2 (_, a) = a

let return_split_restore_parameters heavy_list shares seeds =
  let heavy_arr = Array.of_list heavy_list in
  SplitSave (heavy_arr, shares, seeds)

let convert_str_list l =  
  Array.of_list (List.map(fun e -> int_of_string e) l)

let convert_nested_str_list l =
  Array.of_list (List.map(fun a -> convert_str_list a) l) 
  

(* Creates a SplitParameters by converting value lists to their appropriate type as defined by the matching key *)
let make_split kwt group  =
  let convert_lists valueLists = 
    let pos = ref 0 in
    List.map2
    (fun k values ->
      List.map (fun v ->
        incr pos;
        let t = get_2 k in 
        Predicate.cst_of_str t v
      ) values
    )
    kwt valueLists
  in
  let g    = List.map (fun sb  -> let vals, parts = sb in Helper'.{values = (convert_lists vals); partitions = parts}) group in
  let keys = List.map (fun kwt -> let k, t = kwt in k) kwt in
  let max  = Helper'.get_max g in
  SplitParameters { keys = keys; constraints = g; num_partitions = max }
  
(* Combines partition lists to state partition group
   State partition group represents the mappings of different value partitions to different state partitions, with a subgroup
   representing the mapping of one value partition to one state partition.
 *)  
let make_group group subgroup = subgroup::group

(* Creates list of integers representing the state partitions a value partition is mapped to*)
let make_subgroup valueLists partitions = (valueLists, List.map (fun p -> try (int_of_string p) with Failure _ -> raise (Db.Tuple.Type_error ("Partitions list expects integers"))) partitions)

(* Creates a list of keys consisting of a name and type each *)
let make_key str = match Misc.nsplit str ":" with
        | [] -> failwith "[Log_parser_helper.make_predicate] internal error"
        | [type_str] -> "", get_type type_str
        | var_name :: type_str :: _ ->
            var_name, get_type type_str

end

module StandardLog_parser_helper = MakeLog_parser_helper(Helper.StandardHelper)
module LabelledLog_parser_helper = MakeLog_parser_helper(Helper.LabelledHelper)
