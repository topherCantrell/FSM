import sys

import SMGen_PyDict
import SMGen_Prop
import SMGen_SNAPpy

# mod_name = sys.argv[1]
# in_mode  = SMGen_PyDict
# out_mode = SMGen_Prop
# modName = "TM_Euclid.py"
# mod_name = "TicTacToe.py"

mod_name = sys.argv[1]

if sys.argv[2] == "PyDict":
    in_mode = SMGen_PyDict
elif sys.argv[2] == "Prop":
    in_mode = SMGen_Prop
elif sys.argv[2] == "SNAPpy":
    in_mode = SMGen_SNAPpy

if sys.argv[3] == "PyDict":
    out_mode = SMGen_PyDict
elif sys.argv[3] == "Prop":
    out_mode = SMGen_Prop
elif sys.argv[3] == "SNAPpy":
    out_mode = SMGen_SNAPpy

(sm, org) = in_mode.loadStates(mod_name)

out_mode.print_states(sm, org)
