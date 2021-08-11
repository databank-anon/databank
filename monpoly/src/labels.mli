type label = string

module LabelSet: Set.S with type elt = label

type labels = LabelSet.t

val string_of_labels: labels -> string

val print_labels: labels -> unit

