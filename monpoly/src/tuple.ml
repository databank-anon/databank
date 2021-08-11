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
open Predicate
open MFOTL
open Labels

module type TUPLE = sig

  type tuple
  (** Tuples are currently implemented as lists of constants
      (see {!type:Predicate.cst}). *)

  type ielt
  type ituple = ielt list

  val compare: tuple -> tuple -> int
  (** [compare x y] returns [0] if [x] is equal to [y], a negative
      integer if [x] is less than [y], and a positive integer if [x]
      is greater than [y]. It is currently an alias to
      {{:http://caml.inria.fr/pub/docs/manual-ocaml/libref/Pervasives.html}Pervasives.compare},
      hence it using the lexicographic ordering. *)

  exception Type_error of string

  val labels: ?indices:int list option -> tuple -> labels
  (** [labels] returns the list of labels of a given tuple at positions [indices] (at all positions
      if [indices] is None or not specified). *)

  val unlabel: ?indices:int list option -> tuple -> tuple

  val make_tuple: cst list -> tuple
  (** [make_tuple] builds a tuple from a list of constants. *)

  val make_tuple2: ituple -> (string * tcst) list -> tuple
  (** [make_tuple] builds a tuple from a list of strings and a list of
    tuple types. *)

  val get_constants: tuple -> cst list

  val get_at_pos: tuple -> int -> cst
  (** [get_at_pos pos t] returns the value at position [pos] in [t] *)

  val get_labels_at_pos: tuple -> int -> labels
  (** [get_labels_at_pos pos t] returns the labels at position [pos] in [t] *)

  val get_all_labels: tuple -> labels
  (** [get_all_labels t] returns all labels in [t] *)

  val add_first: tuple -> cst -> tuple
  (** [add_first t v] builds a new tuple by adding the value [v] at the
      beginning of [t] *)

  (* val duplicate_pos: int -> tuple -> tuple *)
  (*   (\** [duplicate_pos pos t] builds a new tuple by adding the value at *)
  (*       position [pos] in [t] to the end of [t]. *\) *)

  val projections: int list -> tuple -> tuple
  (** [projections posl t] builds a new tuple by keeping from [t] only
    the values at positions in the [posl] list (the order of the
    remaining values is preserved). *)

  val project_away: int list -> tuple -> tuple
  (** [project_away posl t] builds a new tuple by removing from [t] the
    values at positions in the [posl] list (the order of the remaining
    values is preserved). *)


  val satisfiesp: term list -> tuple -> bool * tuple * labels
  (** [satisfiesp p t] returns [(true,t',l)] if the tuple [t] satisfies
      the predicate [p] with table labels [l], and [(false,[],{})] otherwise. In the former
      case, [t'] consists of the values assigned to the variables in
      [p], in the order these variables appear therein.

      For instance, [satisfies p t] where [p] represents the formula
      [P(x,"b",y,x)] returns [(true;["a";"c"];l)] for
      [t=["a";"b";"c";"a"]], and [(false,[];{})] for
      [t=["a";"b";"c";"d"]].
   *)

  (* val satisfiesf1: (cst -> bool) -> int -> tuple -> bool *)
  (*   (\** [satisfiesf1 f pos t] returns [f v] where [v] is the value at *)
  (*       position [pos] in [t]. *\) *)

  (* val satisfiesf2: (cst -> cst -> bool) -> int -> int -> tuple -> bool *)
  (*   (\** [satisfiesf1 f pos1 pos2 t] returns [f v1 v2] where [v1] and *)
  (*       [v2] are the values at positions [pos1] and respectively [pos2] *)
  (*       in [t]. *\) *)


  val get_filter: (var list) -> formula -> tuple -> bool
  val get_tf: (var list) -> formula -> tuple -> tuple


  exception Not_joinable of labels
  (** [Not_joinable] is raised when two tuples are not joinable (see
      {!Tuple.join}). *)

  val join: (int * cst) list -> tuple -> tuple -> tuple * labels * int list
  (** [join posvall t1 t2] builds a new tuple by joining the tuples
      [t1] and [t2]. The list [posvall] consists of pairs of positions
      and values, indicating what the values at the corresponding
      positions in [t2] should be. In other words, if [(pos,val)]
      appears in [posvall], then [t] should have value [val] at
      position [pos]. If this is not the case then the {!Not_joinable}
      exception is raised. The result is obtained by appending [t1] to
      the what remains of [t2] after ignoring the values at the
      positions appearing in [posvall].
      (The list of positions in [posvall] is assumed to be ordered
      ascendingly.)

      For instance, for [posvall = [(0,"b");(1,"c");(3,"a")]],
      [t1=["a";"c";"b"]], and [t2 = ["b";"c";"d";"a"]], the result is
      [["a";"c";"b";"d"]].
   *)

  val join_rev: int list -> (int * cst) list -> tuple -> tuple -> tuple * labels * int list

  (** Pretty-printing functions: *)

  val string_of_tuple: tuple -> string
  (* val output_tuple: out_channel -> tuple -> unit *)
  val print_tuple: tuple -> unit

  val has_null: tuple -> bool
  val has_null_at_pos: int list -> tuple -> bool

  val set_null: int list -> (int * int) list -> tuple -> tuple

end

module StandardTuple = struct
 
  type tuple = cst list

  type ielt = string
  type ituple = ielt list

  (* compare two tuples *)
  let compare t1 t2 = compare t1 t2
  (* this is Pervasives.compare: [2]>[1;4] (as 2>1), [2]<[3;4] (as 2<3),
     and [2]<[2;4] (as []<l for any non-empty l) *)

  (*** operations on tuples ***)

  let labels ?indices:(i=None) _ = LabelSet.empty

  let unlabel ?indices:(i=None) x = x

  let make_tuple x = x

  exception Type_error of string

  let make_tuple2 sl tl =
    let pos = ref 0 in
    List.map2
      (fun s (_, t) ->
        incr pos;
        match t with
        | TInt ->
           (try Int (int_of_string s)
            with Failure _ ->
              raise (Type_error ("Expected type int for field number "
                                 ^ (string_of_int !pos))))
        | TStr -> Str s
        | TFloat ->
           (try Float (float_of_string s)
            with Failure _ ->
              raise (Type_error ("Expected type float for field number "
                                 ^ (string_of_int !pos))))
        | TNull -> Null
      )
      sl tl

  let get_constants tuple = tuple

  let get_at_pos = List.nth

  let get_labels_at_pos _ _ = LabelSet.empty

  let get_all_labels _ = LabelSet.empty

  let add_first tuple v = v :: tuple
  let add_last tuple v = tuple @ [v]

  (*let duplicate_pos pos tuple =
    let v = get_at_pos tuple pos in
    add_last tuple v*)

  let project_away = Misc.remove_positions
  let projections = Misc.get_positions


  (*** OLD ***)
  (* let satisfiesp p t =  *)
  (*   (\* we use same idea as Samuel: assign values to variables *\) *)
  (*   let rec satisf assign t a =  *)
  (*     match t,a with *)
  (*       | [],[] ->  *)
  (*   true, List.rev (snd (List.split assign)) *)
  (*       | ht::tt,ah::at ->  *)
  (*   (match ah with *)
  (*     | Var x -> *)
  (*       (try *)
  (*          let v = List.assoc x assign in *)
  (*          if v = ht then *)
  (*      satisf assign tt at *)
  (*          else *)
  (*      (false,[]) *)
  (*        with Not_found ->  *)
  (*          satisf ((x,ht)::assign) tt at) *)
  (*     | Cst v ->  *)
  (*       if v = ht then *)
  (*         satisf assign tt at  *)
  (*       else *)
  (*         (false,[]) *)
  (*   ) *)
  (*       | _ -> failwith "[Tuple.satisfiesp] The arity of [p] and the length of [t] differ." *)
  (*   in  *)
  (*   satisf [] t (Predicate.get_args p) *)


  let rec check_constr assign = function
    | [] -> true
    | (c, sterm) :: rest ->
       (c = Predicate.eval_term assign sterm) && (check_constr assign rest)


  (* We assume that terms are simplified: the only ground terms are *)
  (* constants. TODO: do we really? Anyhow, terms should be simplified. *)
  let satisfiesp arg_list tuple =
    let rec satisf assign res crt_tuple args constr =
      match crt_tuple, args with
      | [], [] ->
         if check_constr assign constr then
           true, List.rev res, LabelSet.empty
         else
           false, [], LabelSet.empty
                        
      | c :: rest, term :: args' ->
         (match term with
          | Var x ->
             (try
                let c' = List.assoc x assign in
                if c = c' then
                  satisf assign res rest args' constr
                else
                  false, [], LabelSet.empty
              with Not_found ->
                satisf ((x, c) :: assign) (c :: res) rest args' constr
             )

          | Cst c' ->
             if c = c' then
               satisf assign res rest args' constr
             else
               false, [], LabelSet.empty

          | _ -> satisf assign res rest args' ((c, term) :: constr)
         )
      | _ -> failwith "[Tuple.satisfiesp] The arity of [p] and the length of [t] differ."
    in
    satisf [] [] tuple arg_list []


  let satisfiesf1 f pos tuple =
    f (get_at_pos tuple pos)


  let satisfiesf2 f pos1 pos2 tuple =
    f (get_at_pos tuple pos1) (get_at_pos tuple pos2)

  let eval_term_on_tuple tuple =
    Predicate.eval_eterm (get_at_pos tuple)

  let satisfiesf2 cond term1 term2 tuple =
    cond (eval_term_on_tuple tuple term1) (eval_term_on_tuple tuple term2)


  let rec get_pos_term attr = function
    | Var x -> Var (Misc.get_pos x attr)
    | Cst c -> Cst c
    | I2f t -> I2f (get_pos_term attr t)
    | F2i t -> F2i (get_pos_term attr t)
    | UMinus t -> UMinus (get_pos_term attr t)
    | Plus (t1, t2) -> Plus (get_pos_term attr t1, get_pos_term attr t2)
    | Minus (t1, t2) -> Minus (get_pos_term attr t1, get_pos_term attr t2)
    | Mult (t1, t2) -> Mult (get_pos_term attr t1, get_pos_term attr t2)
    | Div (t1, t2) -> Div (get_pos_term attr t1, get_pos_term attr t2)
    | Mod (t1, t2) -> Mod (get_pos_term attr t1, get_pos_term attr t2)


  let get_filter attr formula =
    let pos_t1, pos_t2 =
      match formula with
      | Equal (t1, t2)
        | Less (t1, t2)
        | LessEq (t1, t2)
        | Neg (Equal (t1, t2))
        | Neg (Less (t1, t2))
        | Neg (LessEq (t1, t2))
        ->
         get_pos_term attr t1, get_pos_term attr t2
      | _ -> failwith "[Tuple.get_filter, pos] internal error"
    in
    let cond =
      match formula with
      | Equal (t1, t2) -> (=)
      | Less (t1, t2) -> (<)
      | LessEq (t1, t2) -> (<=)
      | Neg (Equal (t1, t2)) -> (<>)
      | Neg (Less (t1, t2)) -> (>=)
      | Neg (LessEq (t1, t2)) -> (>)
      | _ -> failwith "[Tuple.get_filter, cond] internal error"
    in
    satisfiesf2 cond pos_t1 pos_t2



  (* return a transformation function on tuples *)
  let get_tf attr = function
    | Equal (t1, t2) ->
       let f t =
         let pos_term = get_pos_term attr t in
         (fun tuple ->
           let c = eval_term_on_tuple tuple pos_term in
           add_last tuple c)
       in
       (match t1, t2 with
        | Var x, t when not (List.mem x attr) -> f t
        | t, Var x when not (List.mem x attr) -> f t
        | _ -> failwith "[Tuple.get_processing_func, equal] internal error"
       )
    | _ -> failwith "[Tuple.get_processing_func, formula] internal error"


  exception Not_joinable of labels


  let join posval t1 t2 =
    let rec join' crtpos pv t =
      match pv,t with
      | (hp,hv)::tpv, ht::tt ->
         if hp = crtpos then
           if hv = ht then
             join' (crtpos+1) tpv tt
           else
             raise (Not_joinable LabelSet.empty)
         else
           ht::(join' (crtpos+1) pv tt)
      | [],_ -> t
      | _,[] -> failwith "[Tuple.join] bad posval list"
    in
    (t1 @ (join' 0 posval t2), LabelSet.empty, [])

  (* the result should be the same as [join t1 t2] *)
  (* [join'] just checks that values in [t1] are correspct with respect
   to [posval], but does not select elements, while [join''] does not
   check anything, just selects positions that don't appear in [pos] *)
  let join_rev pos2 posval t2 t1 =
    let rec check crtpos pv t =
      match pv,t with
      | (hp, hv)::tpv, ht::tt ->
         if hp = crtpos then
           if hv = ht then
             check (crtpos+1) tpv tt
           else
             raise (Not_joinable LabelSet.empty)
         else
           check (crtpos+1) pv tt
      | [], _ -> ()
      | _, [] -> failwith "[Tuple.join] bad posval list"
    in
    let rec sel crtpos pl t =
      match pl,t with
      | hp::tpv, ht::tt ->
         if hp = crtpos then
           sel (crtpos+1) tpv tt
         else
           ht :: (sel (crtpos+1) pl tt)
      | [], _ -> t
      | _, [] -> failwith "[Tuple.join_rev] bad pos list"
    in
    check 0 posval t1;
    (t1 @ (sel 0 pos2 t2), LabelSet.empty, [])



  (** printing functions **)

  let string_of_tuple = Misc.string_of_list (string_of_cst false)
  let print_tuple = Misc.print_list (print_cst false)

  (** test Null **)

  let has_null _ = false
  let has_null_at_pos _ _ = false

  let set_null nulls matches tup =
    let rec all_pos1 nulls matches = match nulls, matches with
          hn::tn, (pos2, pos1)::tm when hn = pos2 -> pos1::(all_pos1 tn tm)
        | hn::tn, (pos2, pos1)::tm (* necessarily hn > pos2 *) -> all_pos1 (hn::tn) tm
        | []    , _  -> []
        | _     , [] -> assert false in
    let pos1_ = all_pos1 nulls matches in
    let rec set_null_ curpos pos1_ tup = match pos1_, tup with
        pos1::tp, v::tt when pos1 = curpos -> Null::(set_null_ (curpos+1) tp tt)
      | pos1::tp, v::tt -> v::(set_null_ (curpos+1) pos1_ tt)
      | []      , _     -> tup
      | _       , []    -> assert false in
    set_null_ 0 pos1_ tup 

                                    
end

module LabelledTuple = struct
 
  type tuple = (cst * labels) list

  type ielt = string option * (string list)
  type ituple = ielt list

  (* compare two tuples *)
  let compare t1 t2 = compare t1 t2
  (* this is Pervasives.compare: [2]>[1;4] (as 2>1), [2]<[3;4] (as 2<3),
  and [2]<[2;4] (as []<l for any non-empty l) *)
      
  (** printing functions **)

  let string_of_tuple = Misc.string_of_list (fun x -> string_of_cst false (fst x)
                                                      ^ " [" ^ string_of_labels (snd x) ^ "]")

  let print_tuple = Misc.print_list (fun x -> print_cst false (fst x);
                                              print_string " [";
                                              print_labels (snd x);
                                              print_string "]")


  (*** operations on tuples ***)

  let labels ?indices:(i=None) x = match i with
      None -> List.fold_left (fun u (_, l) -> LabelSet.union u l) LabelSet.empty x
    | Some j -> fst (List.fold_left (fun (u, k) (_, l) ->
                         if List.mem k j then (LabelSet.union u l, k+1) else (u, k+1))
                       (LabelSet.empty, 0) x)

  let unlabel ?indices:((i:int list option)=None) x = match i with
      None -> List.map (fun (c, _) -> (c, LabelSet.empty)) x
    | Some j -> List.mapi (fun i (c, k) -> if List.mem i j then (c, LabelSet.empty) else (c, k)) x

  let make_tuple x =
    List.map (fun c -> (c, LabelSet.empty)) x

  exception Type_error of string

  let make_tuple2 sl tl =
    let pos = ref 0 in
    List.map2
      (fun (s, l) (_, t) ->
        incr pos;
        (begin match s, t with
        | Some s', TInt -> (try Int (int_of_string s')
                            with Failure _ ->
                              raise (Type_error ("Expected type int for field number "
                                                 ^ (string_of_int !pos))))
        | Some s', TStr -> Str s'
        | Some s', TFloat -> (try Float (float_of_string s')
                              with Failure _ ->
                                raise (Type_error ("Expected type float for field number "
                                                   ^ (string_of_int !pos))))
        | Some s', TNull -> Null
        | None   , _     -> Null
         end, LabelSet.of_list l)
      )
      sl tl

  let get_constants x = List.fold_left (fun l x -> match fst x with Null -> l | _ -> (fst x)::l) [] x

  let get_at_pos x i = fst (List.nth x i)

  let get_labels_at_pos x i = snd (List.nth x i)

  let get_all_labels = List.fold_left (fun l (_, l') -> LabelSet.union l l') LabelSet.empty

  let add_first tuple v = (v, LabelSet.empty) :: tuple
  let add_last tuple v = tuple @ [(v, LabelSet.empty)]

  (*let duplicate_pos pos tuple =
    let v = get_at_pos tuple pos in
    add_last tuple v*)

  let project_away = Misc.remove_positions
  let projections = Misc.get_positions

  let rec check_constr assign = function
    | [] -> true
    | (c, sterm) :: rest ->
       (c = Predicate.eval_term assign sterm) && (check_constr assign rest)

  module SatisfiespM = Map.Make(struct type t = var
                                       let compare = compare
                                end)
    
  (* We assume that terms are simplified: the only ground terms are *)
  (* constants. TODO: do we really? Anyhow, terms should be simplified. *)
  let satisfiesp arg_list tuple =
    (* Check variables that only appear once *)
    let safe_vars = fst (List.split
                           (SatisfiespM.bindings
                              (SatisfiespM.filter (fun _ n -> n == 1)
                                 (List.fold_left
                                    (fun s v -> match v with
                                                  Var x -> SatisfiespM.update x
                                                             (function None -> Some 1
                                                                     | Some n -> Some (n+1)) s
                                                | _ -> s)
                                    SatisfiespM.empty arg_list)))) in
    let rec satisf assign res labs crt_tuple args constr =
      match crt_tuple, args with
      | [], [] ->
         if check_constr assign constr then
           true, List.rev res, labs
         else
           false, [], labs
                        
      | (c, l) :: rest, term :: args' ->
         (match term with
          | Var x ->
             (let labs' = if List.mem x safe_vars then LabelSet.union labs l else labs in
              try
                let c' = List.assoc x assign in
                if c = c' then
                  satisf assign res labs' rest args' constr
                else
                  false, [], labs'
              with Not_found ->
                satisf ((x, c) :: assign) ((c, l) :: res) labs' rest args' constr
             )
          | Cst c' ->
             if c = c' then
               satisf assign res (LabelSet.union labs l) rest args' constr
             else
               false, [], labs

          | _ -> satisf assign res (LabelSet.union labs l) rest args' ((c, term) :: constr)
         )
      | _ -> failwith "[Tuple.satisfiesp] The arity of [p] and the length of [t] differ."
    in
    satisf [] [] LabelSet.empty tuple arg_list []

  let satisfiesf1 f pos tuple =
    f (get_at_pos tuple pos)

  let satisfiesf2 f pos1 pos2 tuple =
    f (get_at_pos tuple pos1) (get_at_pos tuple pos2)

  let eval_term_on_tuple tuple =
    Predicate.eval_eterm (get_at_pos tuple)

  let satisfiesf2 cond term1 term2 tuple =
    cond (eval_term_on_tuple tuple term1) (eval_term_on_tuple tuple term2)

  let rec get_pos_term attr = function
    | Var x -> Var (Misc.get_pos x attr)
    | Cst c -> Cst c
    | I2f t -> I2f (get_pos_term attr t)
    | F2i t -> F2i (get_pos_term attr t)
    | UMinus t -> UMinus (get_pos_term attr t)
    | Plus (t1, t2) -> Plus (get_pos_term attr t1, get_pos_term attr t2)
    | Minus (t1, t2) -> Minus (get_pos_term attr t1, get_pos_term attr t2)
    | Mult (t1, t2) -> Mult (get_pos_term attr t1, get_pos_term attr t2)
    | Div (t1, t2) -> Div (get_pos_term attr t1, get_pos_term attr t2)
    | Mod (t1, t2) -> Mod (get_pos_term attr t1, get_pos_term attr t2)

  let get_filter attr formula =
    let pos_t1, pos_t2 =
      match formula with
      | Equal (t1, t2)
        | Less (t1, t2)
        | LessEq (t1, t2)
        | Neg (Equal (t1, t2))
        | Neg (Less (t1, t2))
        | Neg (LessEq (t1, t2))
        ->
         get_pos_term attr t1, get_pos_term attr t2
      | _ -> failwith "[Tuple.get_filter, pos] internal error"
    in
    let cond =
      match formula with
      | Equal (t1, t2) -> (=)
      | Less (t1, t2) -> (<)
      | LessEq (t1, t2) -> (<=)
      | Neg (Equal (t1, t2)) -> (<>)
      | Neg (Less (t1, t2)) -> (>=)
      | Neg (LessEq (t1, t2)) -> (>)
      | _ -> failwith "[Tuple.get_filter, cond] internal error"
    in
    satisfiesf2 cond pos_t1 pos_t2

  (* return a transformation function on tuples *)
  let get_tf attr = function
    | Equal (t1, t2) ->
       let f t =
         let pos_term = get_pos_term attr t in
         (fun tuple ->
           let c = eval_term_on_tuple tuple pos_term in
           add_last tuple c)
       in
       (match t1, t2 with
        | Var x, t when not (List.mem x attr) -> f t
        | t, Var x when not (List.mem x attr) -> f t
        | _ -> failwith "[Tuple.get_processing_func, equal] internal error"
       )
    | _ -> failwith "[Tuple.get_processing_func, formula] internal error"

  exception Not_joinable of labels

  let join posval t1 t2 =
    (*print_string "join (\n";
    print_string "  posval = ";
    List.iter (fun (a,b) -> print_string "("; print_int a; print_string ", "; Predicate.print_cst true b; print_string "); ") posval; print_newline ();
    print_string "  t1 = ";
    print_tuple t1; print_newline ();
    print_string "  t2 = ";
    print_tuple t2; print_newline ();*)
    let rec join' crtpos pv t =
      match pv, t with
      | (hp, hv)::tpv, (ht, lt)::tt ->
         if hp = crtpos then
           begin
             if (hv = ht) || (hv = Null) then
               let t', l', nulls' = join' (crtpos+1) tpv tt in
               t', LabelSet.union l' lt, nulls'
             else (if (ht = Null) then
                     let t', l', nulls' = join' (crtpos+1) tpv tt in
                     t', LabelSet.union l' lt, hp::nulls'
                   else
                     raise (Not_joinable lt))
           end
         else 
           let t', l', nulls' = join' (crtpos+1) pv tt in
           (ht, lt)::t', l', nulls'
      | [],_ -> t, LabelSet.empty, []
      | _,[] -> failwith "[Tuple.join] bad posval list"
    in
    let t', l', nulls' = join' 0 posval t2 in
    (*print_string ") = ";
    print_tuple (t1 @ t'); print_newline ();*)
    t1 @ t', l', List.rev nulls'

  (* the result should be the same as [join t1 t2] *)
  (* [join'] just checks that values in [t1] are correct with respect
   to [posval], but does not select elements, while [join''] does not
   check anything, just selects positions that don't appear in [pos] *)
  let join_rev pos2 posval t2 t1 =
    let rec check crtpos pv t =
      match pv,t with
      | (hp, hv)::tpv, (ht, lt)::tt ->
         if hp = crtpos then
           begin
             if (hv = ht) || (hv = Null) || (ht = Null) then
               check (crtpos+1) tpv tt
             else 
               raise (Not_joinable lt)
           end
         else
           check (crtpos+1) pv tt
      | [], _ -> ()
      | _, [] -> failwith "[Tuple.join] bad posval list"
    in
    let rec sel crtpos pl t =
      match pl, t with
      | hp::tpv, (ht, lt)::tt ->
         if hp = crtpos then
           begin
           if (ht <> Null) then
             let t', l', nulls' = sel (crtpos+1) tpv tt in
             t', LabelSet.union l' lt, nulls'
           else
             let t', l', nulls' = sel (crtpos+1) tpv tt in
             t', LabelSet.union l' lt, hp::nulls'
           end
         else
           let t', l', nulls' = sel (crtpos+1) pl tt in
           (ht, lt)::t', l', nulls'
      | [], _ -> t, LabelSet.empty, []
      | _, [] -> failwith "[Tuple.join_rev] bad pos list"
    in
    check 0 posval t1;
    let t', l', nulls' = sel 0 pos2 t2 in
    t1 @ t', l', List.rev nulls'

  (** test Null **)

  let has_null = List.exists (fun (s, _) -> match s with Null -> true | _ -> false)
  let has_null_at_pos posl x = has_null (projections posl x)

  let set_null nulls matches tup =
      let rec all_pos1 nulls matches = match nulls, matches with
          hn::tn, (pos2, pos1)::tm when hn = pos2 -> pos1::(all_pos1 tn tm)
        | hn::tn, (pos2, pos1)::tm (* necessarily hn > pos2 *) -> all_pos1 (hn::tn) tm
        | []    , _  -> []
        | _     , [] -> assert false in
      let pos1_ = all_pos1 nulls matches in
      let rec set_null_ curpos pos1_ tup = match pos1_, tup with
          pos1::tp, (v, l)::tt when pos1 = curpos -> (Null, l)::(set_null_ (curpos+1) tp tt)
        | pos1::tp, (v, l)::tt -> (v, l)::(set_null_ (curpos+1) pos1_ tt)
        | []      , _          -> tup
        | _       , []         -> assert false in
      set_null_ 0 pos1_ tup 
                                    
end
