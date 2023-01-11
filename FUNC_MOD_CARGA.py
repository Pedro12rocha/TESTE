#FUNÇÃO PARA SIMULAR A VARIAÇÃO DE CARGA EM DE CONSUMIDORES INDUSTRIAIS EM UM DIA.

def Func_mod_load(Dtime):
	# Acessa o opendss
	a1 = 5731; a2 = 1243; a3 = 774.1; a4 = 736.4; a5 = 460; a6 = 50.09; a7 = 87.16; a8 = 126.6
	b1 = 0.1089; b2 = 0.2; b3 = 0.5319; b4 = 0.7366; b5 = 1.089; b6 = 1.534; b7 = 2.302; b8 = 2.003
	c1 = 0.3621; c2 = 3.502; c3 = 1.502; c4 = 1.939; c5 = -2.564; c6 = -1.348; c7 = -5.034; c8 = -1.25
	t = Dtime
	Fload = a1 * math.sin(b1 * t + c1) + a2 * math.sin(b2 * t + c2) + a3 * math.sin(b3 * t + c3) + a4 * math.sin(
		b4 * t + c4) + a5 * math.sin(b5 * t + c5) + a6 * math.sin(b6 * t + c6) + a7 * math.sin(
		b7 * t + c7) + a8 * math.sin(b8 * t + c8)
	return Fload

	dss.loads_first()
		for i in range(dss.loads_count()):
			dss.loads_write_kw(dss.loads_read_kw()*Func_mod_load(Dtime))
			dss.loads_write_kvar(dss.loads_read_kvar()*Func_mod_load(Dtime))
			dss.loads_next()


