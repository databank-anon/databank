open Predicate
open MFOTL
open Helper

module type EXTFORMULA = sig

  module Helper: HELPER

  open Helper
  open Db

  module NEval = Dllist
  module Sk = Dllist
  module Sj = Dllist

  type info  = (int * timestamp * Relation.relation) Queue.t
  type linfo = {
      mutable llast: (int * timestamp) NEval.cell;
      mutable llastq: int
    }
  type ainfo = {mutable arel: Relation.relation option}
  type pinfo = {mutable ptsq: timestamp}
  type ninfo = {mutable init: bool}
  type oainfo = {mutable ores: Relation.relation;
                 oaauxrels: (timestamp * Relation.relation) Mqueue.t}

  type t_agg =
    | C_aux of int 
    | SA_aux of int * cst
    | Med_aux of (int * Intmap.int_map)

  type agg_once_state = {
      tw_rels: (timestamp * (Tuple.tuple * Tuple.tuple * cst) list) Queue.t;
      other_rels: (timestamp * Relation.relation) Queue.t;
      mutable mset: (Tuple.tuple, int) Hashtbl.t;
      mutable hres: (cst list, t_agg) Hashtbl.t;
      mutable labs: Labels.labels;
    }

  type aggMM_once_state = {
      non_tw_rels: (timestamp * Relation.relation) Queue.t;
      mutable tbl: (Tuple.tuple, (timestamp * cst) Dllist.dllist) Hashtbl.t;
      mutable labs: Labels.labels;
    }

  type ozinfo = {mutable oztree: (int, Relation.relation) Sliding.stree;
                 mutable ozlast: (int * timestamp * Relation.relation) Dllist.cell;
                 ozauxrels: (int * timestamp * Relation.relation) Dllist.dllist}
  type oinfo = {mutable otree: (timestamp, Relation.relation) Sliding.stree;
                mutable olast: (timestamp * Relation.relation) Dllist.cell;
                oauxrels: (timestamp * Relation.relation) Dllist.dllist}
  type sainfo = {mutable sres: Relation.relation;
                 mutable sarel2: Relation.relation option;
                 saauxrels: (timestamp * Relation.relation) Mqueue.t}
  type sinfo = {mutable srel2: Relation.relation option;
                sauxrels: (timestamp * Relation.relation) Mqueue.t}
  type ezinfo = {mutable ezlastev: (int * timestamp) NEval.cell;
                 mutable eztree: (int, Relation.relation) Sliding.stree;
                 mutable ezlast: (int * timestamp * Relation.relation) Dllist.cell;
                 ezauxrels: (int * timestamp * Relation.relation) Dllist.dllist}
  type einfo = {mutable elastev: (int * timestamp) NEval.cell;
                mutable etree: (timestamp, Relation.relation) Sliding.stree;
                mutable elast: (timestamp * Relation.relation) Dllist.cell;
                eauxrels: (timestamp * Relation.relation) Dllist.dllist}
  type uinfo = {mutable ulast: (int * timestamp) NEval.cell;
                mutable ufirst: bool;
                mutable ures: Relation.relation;
                mutable urel2: Relation.relation option;
                raux: (int * timestamp * (int * Relation.relation) Sk.dllist) Sj.dllist;
                mutable saux: (int * Relation.relation) Sk.dllist}
  type uninfo = {mutable last1: (int * timestamp) NEval.cell;
                 mutable last2: (int * timestamp) NEval.cell;
                 mutable listrel1: (int * timestamp * Relation.relation) Dllist.dllist;
                 mutable listrel2: (int * timestamp * Relation.relation) Dllist.dllist}

  type comp_one = Relation.relation -> Relation.relation
  type comp_two = Relation.relation -> Relation.relation -> Relation.relation

  type extformula =
    | ERel of Relation.relation
    | EPred of predicate * comp_one * info
    | ELet of predicate * comp_one * extformula * extformula * linfo
    | ENeg of extformula
    | EAnd of comp_two * extformula * extformula * ainfo
    | EOr of comp_two * extformula * extformula * ainfo
    | EExists of comp_one * extformula
    | EAggreg of comp_one * extformula
    | EAggOnce of extformula * interval * agg_once_state *
                    (agg_once_state -> (Tuple.tuple * Tuple.tuple * cst) list -> unit) *
                      (agg_once_state -> Relation.relation -> (Tuple.tuple * Tuple.tuple * cst) list) *
                        (agg_once_state -> Relation.relation)
    | EAggMMOnce of extformula * interval * aggMM_once_state *
                      (aggMM_once_state -> timestamp -> unit) *
                        (aggMM_once_state -> timestamp -> Relation.relation -> unit) *
                          (aggMM_once_state -> Relation.relation)
    | EPrev of interval * extformula * pinfo
    | ENext of interval * extformula * ninfo
    | ESinceA of comp_two * interval * extformula * extformula * sainfo
    | ESince of comp_two * interval * extformula * extformula * sinfo
    | EOnceA of interval * extformula * oainfo
    | EOnceZ of interval * extformula * ozinfo
    | EOnce of interval * extformula * oinfo
    | ENUntil of comp_two * interval * extformula * extformula * uninfo
    | EUntil of comp_two * interval * extformula * extformula * uinfo
    | EEventuallyZ of interval * extformula * ezinfo
    | EEventually of interval * extformula * einfo

  val contains_eventually: extformula -> bool

  val print_auxel:  int * Relation.relation -> unit
  val print_sauxel: MFOTL.timestamp * Relation.relation -> unit

  val print_neval: string -> (int * MFOTL.timestamp) Dllist.dllist -> unit
  val print_predinf: string -> info -> unit
  val print_uinf: string -> uinfo -> unit

  val print_einfn: string -> einfo -> unit
  val print_ezinf: string -> ezinfo -> unit

  val print_extf: string -> extformula -> unit

end

module MakeExtformula: functor (H: HELPER) -> (EXTFORMULA with module Helper = H)
