open Mformula

module Helper' = Helper

module type SPLITTING = sig

  module Mformula: MFORMULA

  open Mformula
  open Extformula

  val print_ef: extformula -> unit
  val comb_m: mformula -> mformula -> mformula
  val combine_neval: (int * MFOTL.timestamp) NEval.dllist -> (int * MFOTL.timestamp) NEval.dllist -> (int * MFOTL.timestamp) NEval.dllist

  val split_formula: Helper'.splitParameters -> mformula -> mformula array
  val split_with_slicer: (Helper.Db.Tuple.tuple -> Predicate.var list -> int array) -> int -> mformula -> mformula array

end

module MakeSplitting (M: MFORMULA): (SPLITTING with module Mformula = M)
