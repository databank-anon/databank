open MFOTL
open Predicate
module Db' = Db
open Helper.StandardHelper
open Helper.StandardHelper.Db

val is_monitorable: Db'.schema -> MFOTL.formula -> bool * (MFOTL.formula * string) option
val convert_formula: Db'.schema -> MFOTL.formula -> Verified.Monitor.formula
val convert_db: monpolyData -> (string,
                                  Verified.Monitor.event_data list Verified.Monitor.set list) Verified.Monitor.mapping *
                                   Verified.Monitor.nat
val convert_violations: (Verified.Monitor.nat * Verified.Monitor.event_data option list Verified.Monitor.set) list -> (int * Relation.relation) list

