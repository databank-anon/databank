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

module MakeMformula (E: EXTFORMULA) = struct

  module Extformula = E

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


  (*  IMPORTANT/TODO
    The int pointers in the marshalled states can only be used if we work under the assumption that:
    1. Each split state marshals the whole formula (given by implementation)
    2. Each Monpoly instance receives all timepoints, without filtering at the source (dependent on the scope of the project)

    If 2. is no longer given by the project, the pointers will be different for different Monpoly instances and can no longer just be combined when merging
   *)
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

  (* For each formula, returns list of relevant free variables according to sub structure *)
  let free_vars f =
    let pvars p = Predicate.pvars p in
    let rec get_pred = function
      | MRel           (_)                    -> []
      | MPred          (p, c, _)              -> (pvars p)
      | MLet           (_, _, f1, f2, _)      -> get_pred f2
      | MNeg           (f1)                   -> get_pred f1
      | MAnd           (c, f1, f2, _)         -> Misc.union (get_pred f1) (get_pred f2)
      | MOr            (c, f1, f2, _)         -> Misc.union (get_pred f1) (get_pred f2)
      (* Utilize comp to map away unwanted elements of pvars *)
      | MExists        (c, f1)                -> rel_to_pvars (c (pvars_to_rel (get_pred f1)))
      | MAggreg        (c, f1)                -> get_pred f1
      | MAggOnce       (f1, _, _, _, _, _)    -> get_pred f1
      | MAggMMOnce     (f1, _, _, _, _, _)    -> get_pred f1
      | MPrev          (_, f1, _)             -> get_pred f1
      | MNext          (_, f1, _)             -> get_pred f1
      | MSinceA        (c, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MSince         (c, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MOnceA         (_, f1, _)             -> get_pred f1
      | MOnceZ         (_, f1, _)             -> get_pred f1
      | MOnce          (_, f1, _)             -> get_pred f1
      | MNUntil        (c, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MUntil         (c, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MEventuallyZ   (_, f1, _)             -> get_pred f1
      | MEventually    (_, f1, _)             -> get_pred f1
    in
    get_pred f

  (* For each formula, returns list of relevant free variables according to sub structure *)
  let predicates f =
    let rec get_pred = function
      | MRel           (_)                    -> []
      | MPred          (p, _, _)              -> p :: []
      | MLet           (p, _, f1, f2, _)      -> Misc.union (get_pred f1)
                                                   (List.filter (fun q -> Predicate.get_name p <> Predicate.get_name q) (get_pred f2))
      | MNeg           (f1)                   -> get_pred f1
      | MAnd           (_, f1, f2, _)         -> Misc.union (get_pred f1) (get_pred f2)
      | MOr            (_, f1, f2, _)         -> Misc.union (get_pred f1) (get_pred f2)
      (* Utilize comp to map away unwanted elements of pvars *)
      | MExists        (comp, f1)             -> get_pred f1
      | MAggreg        (_, f1)                -> get_pred f1
      | MAggOnce       (f1, _, _, _, _, _)    -> get_pred f1
      | MAggMMOnce     (f1, _, _, _, _, _)    -> get_pred f1
      | MPrev          (_, f1, _)             -> get_pred f1
      | MNext          (_, f1, _)             -> get_pred f1
      | MSinceA        (_, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MSince         (_, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MOnceA         (_, f1, _)             -> get_pred f1
      | MOnceZ         (_, f1, _)             -> get_pred f1
      | MOnce          (_, f1, _)             -> get_pred f1
      | MNUntil        (_, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MUntil         (_, _, f1, f2, _)      -> Misc.union (get_pred f1) (get_pred f2)
      | MEventuallyZ   (_, f1, _)             -> get_pred f1
      | MEventually    (_, f1, _)             -> get_pred f1
    in
    get_pred f

end
