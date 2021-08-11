(*
 * This file is part of MONPOLY.
 *
 * Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
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
open Tuple
open Predicate
open MFOTL
open Labels

module type RELATION = sig

  module Tuple: TUPLE
              
  module S: Set.S with type elt = Tuple.tuple

  type relation

  val tuples: relation -> S.t
  val labels: relation -> Labels.labels

  val empty: relation
  val make_relation: ?rel:relation -> ?labs:labels -> S.elt list -> relation
  val adopt_labels: relation -> labels -> relation

  val map: (S.elt -> S.elt) -> relation -> relation

  val is_empty: relation -> bool
  val is_empty_not_null: relation -> bool
  val remove_null: relation -> relation

  val natural_join: (int * int) list -> (int * int) list -> relation -> relation -> relation

  val natural_join_sc1: (int * int) list -> relation -> relation -> relation

  val natural_join_sc2: (int * int) list -> relation -> relation -> relation

  val cross_product: relation -> relation -> relation
                                               
  val minus: int list -> relation -> relation -> relation

  val reorder: int list -> relation -> relation

  val project_away: int list -> relation -> relation

  val eval_pred: predicate -> (relation -> relation)
  val eval_equal: term -> term -> relation
  val eval_not_equal: term -> term -> relation

  val print_rel: string -> relation -> unit
  val print_rel4: string -> relation -> unit
  val print_reln: string -> relation -> unit
  val print_bigrel: relation -> unit
  val print_orel: relation option -> unit

  val union: relation -> relation -> relation
  val diff: relation -> relation -> relation
  val inter: relation -> relation -> relation
  val add: S.elt -> relation -> relation
  val neg: relation -> relation
  val filter: (S.elt -> bool) -> relation -> relation

  val adopt: relation -> relation -> relation
  val adopt_labels: relation -> Labels.labels -> relation

end

module StandardRelation = struct

  module Tuple = StandardTuple

  module S = Set.Make(struct type t = Tuple.tuple
                             let compare = compare
                      end)

  type relation = S.t

  let tuples x = x
  let labels x = Labels.LabelSet.empty

  (*** printing functions ***)

  let print_rel str rel =
    print_string str;
    let rel' = S.elements rel in
    Misc.print_list Tuple.print_tuple rel'

  let print_rel4 str rel =
    print_string str;
    let rel' = S.elements rel in
    Misc.print_list4 Tuple.print_tuple rel'

  let print_reln str rel =
    print_rel str rel;
    print_newline()

  let print_bigrel rel =
    let rel' = S.elements rel in
    Misc.print_list3 Tuple.print_tuple rel'

  let print_orel = function
    | None -> print_string "N"
    | Some rel -> print_rel "S" rel

  (********************************)

  let empty = S.empty
                
  let make_relation ?rel:(rel=empty) ?labs:(labs=LabelSet.empty) list =
    let rec make acc = function
      | [] -> acc
      | h::t -> make (S.add h acc) t
    in make S.empty list

  let adopt_labels rel _ = rel

  let map f rel =
    let res = ref (S.empty) in
    S.iter
      (fun t ->
        res := S.add (f t) !res
      )
      rel

  let map f rel =
    S.fold (fun t rel' -> S.add (f t) rel') rel S.empty

  (********************************)

  let is_empty = S.is_empty

  let is_empty_not_null = is_empty

  let remove_null x = x

  (*******************************************************************)
  (*** rigid predicates ***)

  let trel = make_relation [Tuple.make_tuple []]
  let frel = S.empty

  let eval_equal t1 t2 =
    match t1,t2 with
    | Var x, Cst c
      | Cst c, Var x -> make_relation [Tuple.make_tuple [c]]
    | Cst c, Cst c' when c = c' -> trel
    | Cst c, Cst c' -> frel
    | _ -> failwith "[Relation.eval_equal] (x=y)"

  let eval_not_equal t1 t2 =
    match t1,t2 with
    | Var x, Var y when x = y -> frel
    | Cst c, Cst c' when c = c' -> frel
    | Cst c, Cst c' -> trel
    | _ -> failwith "[Relation.eval_not_equal] (x <> y)"

  (**********************************************************************)

  (** [matches] gives the columns which should match in the two
    relations in form of a list of tuples [(pos2,pos1)]: column [pos2] in
    [rel2] should match column [pos1] in [rel1] *)
  let natural_join matches1 matches2 rel1 rel2 =
    let joinrel = ref S.empty in
    let process_rel_tuple join_fun matches rel2 t1 =
      (* For each tuple in [rel1] we compute the columns (i.e. positions)
       in rel2 for which there should be matching values and the values
       tuples in rel2 should have at these columns.

       For instance, for [matches] = [(0,1);(1,2);(3,0)] and t1 =
       [6;7;9] we obtain [(0,7);(1,9);(3,6)]. That is, from [rel2] we
       will select all tuples which have 7 on position 0, 9 on
       position 1, and 6 on position 3.  *)
      let pv = List.map
                 (fun (pos2, pos1) -> (pos2, Tuple.get_at_pos t1 pos1))
                 matches
      in
      S.iter
        (fun t2 ->
          try
            let t = join_fun pv t1 t2 in
            joinrel := S.add t !joinrel
          with
            Tuple.Not_joinable labs -> ()
        )
        rel2
    in
    if S.cardinal rel1 < S.cardinal rel2 then
      let join_fun = fun x y z -> match Tuple.join x y z with a, _, _ -> a in
      S.iter (process_rel_tuple join_fun matches1 rel2) rel1
    else
      begin
        let pos2 = List.map fst matches1 in
        let join_fun = fun x y z -> match Tuple.join_rev pos2 x y z with a, _, _ -> a in
        S.iter (process_rel_tuple join_fun matches2 rel1) rel2
      end;
    !joinrel

  let in_t2_not_in_t1 t2 matches =
    let len  = List.length (Tuple.get_constants t2) in
    (* these are the positions in t2 which also appear in t1 *)
    let t2_pos = List.map snd matches in
    let rec get_aux pos =
      if pos = len then []
      else if not (List.mem pos t2_pos) then
        let v = Tuple.get_at_pos t2 pos in
        v :: (get_aux (pos+1))
      else
        get_aux (pos+1)
    in
    get_aux 0

  (* Misc.subset attr1 attr2 *)
  (* Note that free_vars in (f1 AND f2) are ordered according to f1 not
   to f2!  Thus, for instance, for p(x,y) AND q(z,y,x) the fields
   should be ordered by (x,y,z).
   *)
  let natural_join_sc1 matches rel1 rel2 =
    let joinrel = ref S.empty in
    S.iter (fun t2 ->
        let t1_list =
          List.map
            (fun (pos1, pos2) ->
              (* x is at pos1 in t1 and at pos2 in t2 *)
              Tuple.get_at_pos t2 pos2)
            matches
        in
        let t1 = Tuple.make_tuple t1_list in
        if S.mem t1 rel1 then

          let t2_list = in_t2_not_in_t1 t2 matches in
          let t2' = Tuple.make_tuple (t1_list @ t2_list) in
          joinrel := S.add t2' !joinrel
      ) rel2;
    !joinrel

  (* Misc.subset attr2 attr1 *)
  let natural_join_sc2 matches rel1 rel2 =
    let joinrel = ref S.empty in
    S.iter (fun t1 ->
        let t2 = Tuple.make_tuple (
                     List.map
                       (* x is at pos2 in t2 and at pos1 in t1 *)
                       (fun (pos2, pos1) -> Tuple.get_at_pos t1 pos1)
                       matches)
        in
        if S.mem t2 rel2 then
          joinrel := S.add t1 !joinrel
      ) rel1;
    !joinrel

  let cross_product rel1 rel2 =
    natural_join [] [] rel1 rel2

  let reorder new_pos rel =
    let new_rel = ref S.empty in
    S.iter (fun t ->
        let t' = Tuple.projections new_pos t in
        new_rel := S.add t' !new_rel
      ) rel;
    !new_rel

  (* not set difference, but the diff operator as defined in Abiteboul, page 89 *)
  let minus posl rel1 rel2 =
    S.filter
      (fun t ->
        let t' = (Tuple.projections posl t) in
        not (S.mem t' rel2)
      )
      rel1

  let no_constraints tlist =
    let rec iter vars = function
      | [] -> true
      | (Var x) :: tlist ->
         if List.mem x vars then
           false (* there are constraints *)
         else (* new variable, we record its position *)
           iter (x :: vars) tlist

      | _ :: tlist -> false  (* there are constraints *)
    in
    iter [] tlist

  (* Given a predicate [f]=[p(t_1,\dots,t_n)], [eval_pred] returns a
   function from relations to relations; this function transforms
   [|p(x_1,\dots,x_n)|] into [|p(t_1,\dots,t_n)|]
   *)
  let eval_pred p =
    let tlist = Predicate.get_args p in
    if no_constraints tlist then
      fun rel -> rel
    else
      fun rel ->
      let res = ref S.empty in
      S.iter
        (fun t ->
          let b, t', _ = Tuple.satisfiesp tlist t in
          if b then
            res := S.add t' !res;
        ) rel;
      !res

  (* the columns in [posl] are eliminated *)
  let project_away posl rel =
    map (Tuple.project_away posl) rel

  let union = S.union
  let diff = S.diff
  let inter = S.inter
  let add = S.add

  let neg rel =
    if is_empty rel then (* false? *)
      S.singleton (Tuple.make_tuple [])
    else
      empty (* true *)

  let filter = S.filter

  let adopt x _ = x

  let adopt_labels x _ = x
                
end

module LabelledRelation = struct

  module Tuple = LabelledTuple

  module S = Set.Make(struct type t = Tuple.tuple
                             let compare = compare
                      end)

  type label = string

  type relation = {tuples: S.t; labels: LabelSet.t}

  let tuples x = x.tuples
  let labels x = x.labels

  (*** printing functions ***)

  let print_set = Labels.print_labels
                        
  let print_rel str rel =
    print_string str;
    let tuples = S.elements rel.tuples in
    print_string "{ tuples = ";
    Misc.print_list Tuple.print_tuple tuples;
    print_string ";\n  labels = ";
    print_set rel.labels;
    print_string " }"
    
  let print_rel4 str rel =
    print_string str;
    let tuples = S.elements rel.tuples in
    Misc.print_list4 Tuple.print_tuple tuples

  let print_reln str rel =
    print_rel str rel;
    print_newline()

  let print_bigrel rel =
    let tuples = S.elements rel.tuples in
    Misc.print_list3 Tuple.print_tuple tuples

  let print_orel = function
    | None -> print_string "N"
    | Some rel -> print_rel "S" rel

  (********************************)

  let empty = { tuples = S.empty; labels = LabelSet.empty }
                                            
  let make_relation ?rel:(rel=empty) ?labs:(labs=LabelSet.empty) list =
    let rec make acc = function
      | [] -> acc
      | h::t -> make (S.add h acc) t
    in { tuples = make S.empty list; labels = LabelSet.union rel.labels labs }

  let adopt_labels rel labs =
    { tuples = rel.tuples; labels = LabelSet.union rel.labels labs }

  let map_t = S.map

  let map f rel =
    { rel with tuples = map_t f rel.tuples }

  (********************************)

  let is_empty rel =
    S.is_empty rel.tuples

  let is_empty_not_null rel =
    S.exists Tuple.has_null rel.tuples

  let remove_null rel =
    let null_labels = S.fold (fun x l -> LabelSet.union l (Tuple.get_all_labels x))
                        (S.filter Tuple.has_null rel.tuples) LabelSet.empty in
    { tuples = S.filter (fun x -> not (Tuple.has_null x)) rel.tuples;
      labels = LabelSet.union rel.labels null_labels }

  (*******************************************************************)
  (*** rigid predicates ***)

  let trel = make_relation [Tuple.make_tuple []]
  let frel = { tuples = S.empty; labels = LabelSet.empty }

  let eval_equal t1 t2 =
    match t1,t2 with
    | Var x, Cst c
      | Cst c, Var x -> make_relation [Tuple.make_tuple [c]]
    | Cst c, Cst c' when c = c' -> trel
    | Cst c, Cst c' -> frel
    | _ -> failwith "[Relation.eval_equal] (x=y)"

  let eval_not_equal t1 t2 =
    match t1,t2 with
    | Var x, Var y when x = y -> frel
    | Cst c, Cst c' when c = c' -> frel
    | Cst c, Cst c' -> trel

    | _ -> failwith "[Relation.eval_not_equal] (x <> y)"
  (**********************************************************************)

  (** [matches] gives the columns which should match in the two
    relations in form of a list of tuples [(pos2,pos1)]: column [pos2] in
    [rel2] should match column [pos1] in [rel1] *)
  let natural_join matches1 matches2 rel1 rel2 =
    (*print_string "natural_join (\n";
    print_string "  matches1 = ";
    List.iter (fun (a,b) -> print_string "("; print_int a; print_string ", "; print_int b; print_string "); ") matches1; print_newline ();
    print_string "  matches2 = ";
    List.iter (fun (a,b) -> print_string "("; print_int a; print_string ", "; print_int b; print_string "); ") matches2; print_newline ();
    print_string "  rel1 = ";
    print_rel "Rel " rel1; print_newline ();
    print_string "  rel2 = ";
    print_rel "Rel " rel2; print_newline ();*)
    let process_rel_tuple join_fun matches rel2 t1 rel =
      (* For each tuple in [rel1] we compute the columns (i.e. positions)
       in rel2 for which there should be matching values and the values
       tuples in rel2 should have at these columns.

       For instance, for [matches] = [(0,1);(1,2);(3,0)] and t1 =
       [6;7;9] we obtain [(0,7);(1,9);(3,6)]. That is, from [rel2] we
       will select all tuples which have 7 on position 0, 9 on
	 position 1, and 6 on position 3.  *)
      let pv = List.map (fun (pos2, pos1) -> (pos2, Tuple.get_at_pos t1 pos1)) matches in
      let l'' = List.fold_left
                  (fun l (pos2, pos1) -> LabelSet.union (Tuple.get_labels_at_pos t1 pos1) l)
          rel.labels matches in
      S.fold (fun t2 rel -> try let t', l', nulls' = join_fun pv t1 t2 in
                                { tuples = S.add (Tuple.set_null nulls' matches t') rel.tuples;
                                  labels = LabelSet.union l' l'' }
                            with Tuple.Not_joinable labs -> rel)
	rel2.tuples
	{ rel with labels = LabelSet.union rel.labels l'' }
    in
    let r = (if S.cardinal rel1.tuples < S.cardinal rel2.tuples then
      S.fold (process_rel_tuple Tuple.join matches1 rel2) rel1.tuples
        { tuples = S.empty; labels = LabelSet.union rel2.labels rel1.labels }
    else
      S.fold (process_rel_tuple (Tuple.join_rev (List.map fst matches1)) matches2 rel1) rel2.tuples
        { tuples = S.empty; labels = LabelSet.union rel2.labels rel1.labels })
    in
    (*print_string ") = ";
    print_rel "Rel " r; print_newline (); print_newline (); print_newline ();*)
    r

  let in_t2_not_in_t1 t2 matches =
    let len  = List.length (Tuple.get_constants t2) in
    (* these are the positions in t2 which also appear in t1 *)
    let t2_pos = List.map snd matches in
    let rec get_aux pos =
      if pos = len then []
      else if not (List.mem pos t2_pos) then
        let v = Tuple.get_at_pos t2 pos in
        v :: (get_aux (pos+1))
      else
        get_aux (pos+1)
    in
    get_aux 0

  (* Misc.subset attr1 attr2 *)
  (* Note that free_vars in (f1 AND f2) are ordered according to f1 not
   to f2!  Thus, for instance, for p(x,y) AND q(z,y,x) the fields
   should be ordered by (x,y,z).
   *)
  let natural_join_sc1 matches rel1 rel2 =
    natural_join (List.map (fun (a,b) -> (b,a)) matches) matches rel1 rel2
                 
  (* Misc.subset attr2 attr1 *)
  let natural_join_sc2 matches rel1 rel2 =
    natural_join matches (List.map (fun (a,b) -> (b,a)) matches) rel1 rel2

  let cross_product rel1 rel2 =
    natural_join [] [] rel1 rel2

  let reorder new_pos rel =
    S.fold (fun t rel -> let t' = Tuple.projections new_pos t in
                       { rel with tuples = S.add t' rel.tuples })
      rel.tuples { tuples = S.empty; labels = rel.labels }

  (* not set difference, but the diff operator as defined in Abiteboul, page 89 *)
  let minus posl rel1 rel2 =
    let rel2 = remove_null rel2 in
    let rel2_labels = S.fold (fun t lab -> LabelSet.union lab (Tuple.labels t)) rel1.tuples LabelSet.empty in
    S.fold (fun t rel -> let t' = Tuple.projections posl t in
                         let l' = Tuple.labels ~indices:(Some posl) t in
                         match S.find_opt t' rel2.tuples with
                           Some _ -> { rel with labels = LabelSet.union rel.labels l' }
                         | None -> { tuples = S.add (Tuple.unlabel ~indices:(Some posl) t) rel.tuples;
                                     labels = LabelSet.union rel.labels l' })
      rel1.tuples { tuples = S.empty; labels = LabelSet.union rel2_labels (LabelSet.union rel1.labels rel2.labels) }

  (* given the "predicate formula" [p] and a relation [rel] ("having the
   same signature" as [p]), obtain the relation containing those
   tuples of [rel] which satisfy [p] *)
  let eval_pred p rel =
    let rel = remove_null rel in
    let tlist = Predicate.get_args p in
    S.fold (fun t rel ->
        let b, t', l = Tuple.satisfiesp tlist t in
        if b then { tuples = S.add t' rel.tuples; labels = LabelSet.union rel.labels l }
        else { rel with labels = LabelSet.union rel.labels l }) rel.tuples
      { tuples = S.empty; labels = rel.labels }
              
  (* the columns in [posl] are eliminated *)
  let project_away posl rel =
    (*List.iter (fun x -> print_int x; print_string "; ") posl; print_newline();*)
    let tuples = map_t (Tuple.project_away posl) (S.filter (fun x -> not (Tuple.has_null_at_pos posl x)) rel.tuples)
    and labels = S.fold (fun x l -> LabelSet.union l (Tuple.get_all_labels x))
        (S.filter (Tuple.has_null_at_pos posl) rel.tuples) rel.labels in
    { tuples; labels }

  (* lifting set operations *)
  let union rel1 rel2 =
    { tuples = S.union rel1.tuples rel2.tuples; labels = LabelSet.union rel1.labels rel2.labels }

  let lift_op_gather_labels op rel1 rel2 =
    let rel1_0 = S.filter Tuple.has_null rel1.tuples
    and rel2_0 = S.filter Tuple.has_null rel2.tuples
    and rel1_1 = S.filter (fun x -> not (Tuple.has_null x)) rel1.tuples
    and rel2_1 = S.filter (fun x -> not (Tuple.has_null x)) rel2.tuples in
    { tuples = S.union (S.map Tuple.unlabel (op rel1_1 rel2_1)) (S.union rel1_0 rel2_0);
      labels = List.fold_left LabelSet.union LabelSet.empty
                 [rel1.labels; rel2.labels;
                  S.fold (fun x t -> LabelSet.union t (Tuple.labels x)) rel1.tuples LabelSet.empty;
                  S.fold (fun x t -> LabelSet.union t (Tuple.labels x)) rel2.tuples LabelSet.empty]  }    

  let diff =
    lift_op_gather_labels S.diff

  let inter =
    lift_op_gather_labels S.inter

  let add t rel = { rel with tuples = S.add t rel.tuples }

  let neg rel =
    if is_empty rel then
      { rel with tuples = S.singleton (Tuple.make_tuple []) }
    else
      { rel with tuples = S.empty }

  let filter f rel =
    { rel with tuples = S.filter f rel.tuples }

  let adopt rel1 rel2 =
    { rel1 with labels = LabelSet.union rel1.labels rel2.labels }

  let adopt_labels rel labs =
    { rel with labels = LabelSet.union rel.labels labs }
        
        
end                            
