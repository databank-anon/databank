open Extformula
open Predicate
open MFOTL

module type MFORMULA = sig

  module Extformula: EXTFORMULA

  open Extformula
  open Helper
  open Db

  (* Immutable version of types used in eformula *)
  type mozinfo = { mozauxrels: (int * timestamp * Relation.relation) Dllist.dllist}

  type moinfo  = { moauxrels: (timestamp * Relation.relation) Dllist.dllist}

  type msainfo = { msres: Relation.relation;
                   msarel2: Relation.relation option;
                   msaauxrels: (timestamp * Relation.relation) Mqueue.t}
  type msinfo  = { msrel2: Relation.relation option;
                   msauxrels: (timestamp * Relation.relation) Mqueue.t}

  type mezinfo = { mezauxrels:  (int * timestamp * Relation.relation) Dllist.dllist}

  type meinfo  = { meauxrels:  (timestamp * Relation.relation) Dllist.dllist}

  type muinfo  = { mulast   :  int;
                   mufirst  :  bool;
                   mures    :  Relation.relation;
                   murel2   :  Relation.relation option;
                   mraux    :  (int * timestamp * (int * Relation.relation) Sk.dllist) Sj.dllist;
                   msaux    :  (int * Relation.relation) Sk.dllist}
  type muninfo = { mlast1   :  int;
                   mlast2   :  int;
                   mlistrel1:  (int * timestamp * Relation.relation) Dllist.dllist;
                   mlistrel2:  (int * timestamp * Relation.relation) Dllist.dllist;}

  (* Immutable version of eformula used for marshalling *)
  type mformula =
    | MRel of Relation.relation
    | MPred of predicate * comp_one * info
    | MLet of predicate * comp_one * mformula * mformula * (int * int)
    | MNeg of mformula
    | MAnd of comp_two * mformula * mformula * ainfo
    | MOr of comp_two * mformula * mformula * ainfo
    | MExists of comp_one * mformula
    | MAggreg of comp_one * mformula
    | MAggOnce of mformula * interval * agg_once_state *
                    (agg_once_state -> (Tuple.tuple * Tuple.tuple * cst) list -> unit) *
                      (agg_once_state -> Relation.relation -> (Tuple.tuple * Tuple.tuple * cst) list) *
                        (agg_once_state -> Relation.relation)
    | MAggMMOnce of mformula * interval * aggMM_once_state *
                      (aggMM_once_state -> timestamp -> unit) *
                        (aggMM_once_state -> timestamp -> Relation.relation -> unit) *
                          (aggMM_once_state -> Relation.relation)
    | MPrev of interval * mformula * pinfo
    | MNext of interval * mformula * ninfo
    | MSinceA of comp_two * interval * mformula * mformula * sainfo
    | MSince of comp_two * interval * mformula * mformula * sinfo
    | MOnceA of interval * mformula * oainfo
    | MOnceZ of interval * mformula * mozinfo
    | MOnce of interval * mformula  * moinfo
    | MNUntil of comp_two * interval * mformula * mformula * muninfo
    | MUntil of comp_two * interval * mformula * mformula * muinfo
    | MEventuallyZ of interval * mformula * mezinfo
    | MEventually of interval * mformula * meinfo

  type state = (timestamp * bool * mformula * (int * timestamp) array * int * bool)

  val free_vars: mformula -> Predicate.var list
  val predicates: mformula -> Predicate.predicate list
                                                  
end
                         
module MakeMformula (E: EXTFORMULA) : (MFORMULA with module Extformula = E)
