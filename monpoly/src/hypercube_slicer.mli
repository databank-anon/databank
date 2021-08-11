open Predicate
open Domain_set
open Tuple
open Mformula

type var_id = { var: Predicate.var; free_id: int; tcst: Predicate.tcst }
                
module type HYPERCUBE_SLICER = sig

  module Mformula: MFORMULA

  open Mformula
  open Extformula.Helper.Db
  
  type hypercube_slicer = {
      formula: mformula;
      variables_in_order: var_id array;
      heavy:  heavy array;
      shares: int array array;
      seeds: int array array;
      strides: int array array;
      degree: int;
    }

  val convert_heavy: mformula -> heavy_unproc array -> heavy array

  val create_slicer: mformula -> heavy array -> int array array -> int array array -> hypercube_slicer

  val add_slices_of_valuation: hypercube_slicer -> Tuple.tuple -> Predicate.var list -> int array
  val return_shares: hypercube_slicer -> Predicate.cst option array -> int array

  val convert_slicing_tuple: hypercube_slicer -> string list -> string list -> Predicate.cst option array
                                                                                             
end

module MakeHypercube_slicer (M: MFORMULA) : (HYPERCUBE_SLICER with module Mformula = M)

