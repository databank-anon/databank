open Mformula

(*val marshal: string -> int -> MFOTL.timestamp -> Extformula.extformula -> bool -> (int * MFOTL.timestamp) Extformula.NEval.dllist -> unit
val unmarshal: string -> int * MFOTL.timestamp * Extformula.extformula * bool * (int * MFOTL.timestamp) Extformula.NEval.dllist * int * int * bool
val merge_formulas: string list -> int * MFOTL.timestamp * Extformula.extformula * bool * (int * MFOTL.timestamp) Extformula.NEval.dllist * int * int * bool*)

module type MARSHALLING = sig

  module Mformula: MFORMULA

  open Mformula
  open Extformula

  val ext_to_m: extformula ->  (int * MFOTL.timestamp) NEval.dllist -> (int * MFOTL.timestamp) array * mformula
  val m_to_ext: mformula -> (int * MFOTL.timestamp) NEval.dllist -> extformula
                                                                            
end

module MakeMarshalling (M: MFORMULA): (MARSHALLING with module Mformula = M)
