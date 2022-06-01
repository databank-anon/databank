open MFOTL
open Predicate
open Db

type constraintSet

type valueTuple = (string list * int list)

type sconstraint   = { values: cst list list; partitions: int list}

type constraintRelation = sconstraint list

type splitParameters = {keys: string list; constraints: constraintRelation; num_partitions: int}

val empty: constraintSet
val is_empty: constraintSet -> bool
val add: cst -> constraintSet -> constraintSet
val singleton: cst -> constraintSet
val find_opt: cst -> constraintSet -> cst option
val get_max: constraintRelation -> int

module type HELPER = sig

  module Db: DB

  open Db
              
  (* Enables using the compare function in EExists to project away unwanted free vars *)
  val pvars_to_rel: string list -> Relation.relation
  val rel_to_pvars: Relation.relation -> string list

  val comp_preds: (Relation.relation -> Relation.relation) -> Predicate.predicate list -> Predicate.predicate list

  type commandParameter = 
    | SplitSave       of Domain_set.split_save_parameters
    | SplitParameters of splitParameters
    | Argument        of string

  type dataTuple    = { ts: MFOTL.timestamp; db: db; complete:bool }
  type commandTuple = { c: string;  parameters: commandParameter option; }
  type slicingTestTuple = { vars: Predicate.var list; tuple: string list; output: int array}

  type parser_feed =
    | SlicingTestTuple of slicingTestTuple
    | CommandTuple of commandTuple
    | DataTuple    of dataTuple
    | ErrorTuple   of string

  type monpolyData    = { tp: int; ts: MFOTL.timestamp; db: db }
  type monpolyCommand = { c: string; parameters: commandParameter option}
  type monpolyTestTuple = { vars: Predicate.var list; tuple: string list; output: int array}

  type monpoly_feed =
    | MonpolyTestTuple of monpolyTestTuple
    | MonpolyCommand of commandTuple
    | MonpolyData    of monpolyData
    | MonpolyError   of string
                          
  type 'a atree =
    | ALNode of 'a
    | AINode of ('a * int * int)  
                  
  type ('a, 'b) stree =  ('a, 'b option) Sliding.node atree

  val get_new_elements: 'a Dllist.dllist -> 'a Dllist.cell -> ('a -> bool) -> ('a -> 'b) -> 'b list * 'a Dllist.cell

  val show_results: bool -> 'a -> int -> timestamp -> Relation.relation -> unit

end

module MakeHelper: functor (D: DB) -> (HELPER with module Db = D)

module StandardHelper: HELPER with module Db = Db.MakeDb(Table.MakeTable(Relation.StandardRelation))
module LabelledHelper: HELPER with module Db = Db.MakeDb(Table.MakeTable(Relation.LabelledRelation))
