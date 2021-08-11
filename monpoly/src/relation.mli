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



(**
    This module defines relations and provides operations over them.

    Relations are sets of tuples of the same length. Currently,
    relations are implemented using the
    {{:http://caml.inria.fr/pub/docs/manual-ocaml/libref/Set.html}Set}
    module from the standard library. (The ordering of tuples is given
    by the {!Tuple.compare} function, hence it's lexicographic.)

    This module has an unnamed perspective of relations. Hence,
    columns are identified by their position (from 0 to the number of
    columns minus 1). On the contrary, the {!module:Table} module has
    a named perspective and therein columns are identified by
    attributes.
*)

open MFOTL
open Tuple
open Predicate
open Labels

module type RELATION = sig

  module Tuple: TUPLE
              
  module S: Set.S with type elt = Tuple.tuple

  type relation

  val tuples: relation -> S.t
  val labels: relation -> Labels.labels

  val empty: relation
  val make_relation: ?rel:relation -> ?labs:labels -> S.elt list -> relation
  (** Builds a relation from a list of tuples. *)
  val adopt_labels: relation -> labels -> relation

  val map: (S.elt -> S.elt) -> relation -> relation
  (** [map f rel] returns the relation formed by those tuples [f t]
      with [t] in [rel]. *)

  val is_empty: relation -> bool
  (** [is_empty rel] returns true if the relation is empty (has no tuples). *)
  val is_empty_not_null: relation -> bool
  (** [is_empty rel] returns true if the relation has no tuples without nulls. *)
  val remove_null: relation -> relation
  (** [remove_null] removes tuples with nulls and adds their labels at the tabel level. *)

  val natural_join: (int * int) list -> (int * int) list -> relation -> relation -> relation
  (** [natural_join matches rel1 rel2] returns the natural join of
      relations [rel1] and [rel2]. The parameter [matches] gives the
      columns which should match in the two relations in form of a
      list of tuples [(pos2,pos1)]: column [pos2] in [rel2] should
      match column [pos1] in [rel1].
  *)

  val natural_join_sc1: (int * int) list -> relation -> relation -> relation
  (** [natural_join] special case 1: attr1 are included in attr2 *)

  val natural_join_sc2: (int * int) list -> relation -> relation -> relation
  (** [natural_join] special case 2: attr2 are included in attr1 *)

  val cross_product: relation -> relation -> relation
  (** The cross product of the arguments. *)

  val minus: int list -> relation -> relation -> relation
  (** [reldiff rel1 rel2] returns the set difference between [rel1]
      and the the natural join of [rel1] and [rel2]. *)

  val reorder: int list -> relation -> relation

  val project_away: int list -> relation -> relation
  (** [project_away posl rel] removes the columns in [posl] from
      [rel]. *)

  val eval_pred: predicate -> (relation -> relation)
  (* val selectp: predicate -> relation -> relation *)
  (** [satisfiesp p rel] returns the set of tuples from [rel] which
      satisfy predicate [p].  *)

  val eval_equal: term -> term -> relation
  val eval_not_equal: term -> term -> relation

  (** Pretty-printing functions: *)

  (* val output_rel4: out_channel -> string -> relation -> unit *)

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

module StandardRelation: RELATION with module Tuple = Tuple.StandardTuple

module LabelledRelation: RELATION with module Tuple = Tuple.LabelledTuple
