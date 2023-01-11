# FUNÇÃO RESTRITIVA PARADETERMINAR  SE A POTENCIA DE LINHA COM A GD INSTALADA É MAIOR QUE A POTENCIA MAXIMA SUPOIRTDADE PELA LINHA (EVITAR A INVERSÃO DO FLUXO DE POTENCIA)

def Func_rest_potencia ():
    dss.lines_first()
    for _ in range(dss.lines_count()):
        if dss.lines_read_phases() == 3:
            dss.circuit_setactiveelement(dss.lines_read_name())
            current = dss.cktelement_currentsmagang()
            voltage = dss.cktelement_voltages_mag_ang()
            rating_current = dss.cktelement_read_normamps()
            rating_voltage =

            if max(current[0:12:2]) / rating_current > 1:
                thermal_violation = 1
            else:
                thermal_violation = 0
        dss.lines_next()
        return thermal_violation