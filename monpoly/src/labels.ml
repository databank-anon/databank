type label = string

module LabelSet = Set.Make(struct type t = label
                                  let compare = compare end)

type labels = LabelSet.t

let string_of_labels l =
  Misc.string_of_list_ext "[" "]" ", " (fun x -> x) (LabelSet.elements l)

let print_label = print_string
                    
let print_labels l =
  Misc.print_list_ext "[" "]" ", " print_label (LabelSet.elements l)               
