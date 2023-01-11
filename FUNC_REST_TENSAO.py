# FUNÇÃO RESTRITIVA DE LIMITES DE TENSÃO, DETERMINANDO O MAXIMO E MINIMO EM p.u.

Tensão_pu = dss.circuit_all_node_vmag_pu_by_phase()

def Func_rest_tensao (v_pu_nodes):
    max_value_v_pu = numpy.max(v_pu_nodes)
    min_value_v_pu = numpy.min(v_pu_nodes)

    if max_value_v_pu > 1.05:
        V_rest = 0
    elif min_value_v_pu < 0.95:
        V_rest = 0
    else:
        V_rest = 1
    return V_rest
