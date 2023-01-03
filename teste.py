import py_dss_interface
import map
import numpy
import operator
import cmath



# |Acessa o opendss
dss = py_dss_interface.DSSDLL()
dss_file = r"C:\Users\pedro\Documents\OpenDSS\TCC\WOA\123Bus_No_Print\IEEE123Master_no_loads.dss"
dss.text("compile {}".format(dss_file))

# função restritiva

# functions.volt_var(dss)

ov_violation = False
thermal_violation = False
i = 0
while not ov_violation and not thermal_violation and i < 100:
    i += 1
    dss.pvsystems_first()
    for _ in range(dss.pvsystems_count()):
        dss.text(f"edit pvsystem.{dss.pvsystems_read_name()} pmpp={p_step * i} kva={kva_to_kw * p_step * i} pf={pf} pfpriority=yes")
        dss.pvsystems_next()
    dss.solution_solve()
    voltages = dss.circuit_allbusvmagpu()
    voltage_max = max(voltages)
    voltage_min = min(voltages)
    total_p_feederhead = -1 * dss.circuit_totalpower()[0]
    total_q_feederhead = -1 * dss.circuit_totalpower()[1]

    if voltage_max >= v_threshold:
        ov_violation = True

    dss.lines_first()
    for _ in range(dss.lines_count()):
        if dss.lines_read_phases() == 3:
            dss.circuit_setactiveelement(dss.lines_read_name())
            current = dss.cktelement_currentsmagang()
            rating_current = dss.cktelement_read_normamps()

            if max(current[0:12:2]) / rating_current > 1:
                thermal_violation = True
        dss.lines_next()
