# python implementation of whale optimization algorithm (WOA)
# minimizing rastrigin and sphere function

import random
import numpy
import math # cos() for Rastrigin
import copy # array-copying convenience
import sys # max float
import py_dss_interface
import functions
import cmath
from scipy.stats import weibull_min

# -------------------------
# whale class
class whale:
	def __init__(self, dim, minx, maxx, seed):
		self.rnd = random.Random(seed)
		self.position = [0.0 for i in range(dim)]
		self.fitness = [0.0 for i in range(dim)]

		for i in range(dim):
			self.position[i] = ((maxx - minx) * self.rnd.random() + minx)
			self.fitness[i] = ((maxx - minx) * self.rnd.random() + minx)

# whale optimization algorithm(WOA)
def woa(max_iter, n, dim, minx, maxx):
	rnd = random.Random(0)

	# create n random whales
	whalePopulation = [whale(dim, minx, maxx, i) for i in range(n)]

	# -------open_dss_file()-------------------------------------------------------------------------------------------------
	dss = py_dss_interface.DSSDLL()
	dss_file = r"C:\Users\pedro\Documents\OpenDSS\TCC\WOA\123Bus_No_Print\IEEE123Master.dss"
	dss.text("compile {}".format(dss_file))
	# -----------------------------------------------------------------------------------------------------------------------
	# Função para modificação do valor da carga	----------------------------------------------------------------------------

	a1 = 5731;
	a2 = 1243;
	a3 = 774.1;
	a4 = 736.4;
	a5 = 460;
	a6 = 50.09;
	a7 = 87.16;
	a8 = 126.6
	b1 = 0.1089;
	b2 = 0.2;
	b3 = 0.5319;
	b4 = 0.7366;
	b5 = 1.089;
	b6 = 1.534;
	b7 = 2.302;
	b8 = 2.003
	c1 = 0.3621;
	c2 = 3.502;
	c3 = 1.502;
	c4 = 1.939;
	c5 = -2.564;
	c6 = -1.348;
	c7 = -5.034;
	c8 = -1.25
	t = 19
	Fload = a1 * math.sin(b1 * t + c1) + a2 * math.sin(b2 * t + c2) + a3 * math.sin(b3 * t + c3) + a4 * math.sin(
		b4 * t + c4) + a5 * math.sin(b5 * t + c5) + a6 * math.sin(b6 * t + c6) + a7 * math.sin(
		b7 * t + c7) + a8 * math.sin(b8 * t + c8)
	dss.loads_first()
	for i in range(dss.loads_count()):
		dss.loads_write_kw(dss.loads_read_kw() * Fload)
		dss.loads_write_kvar(dss.loads_read_kvar() * Fload)
		dss.loads_next()
	# -----------------------------------------------------------------------------------------------------------------------
	# Função para modificação por mei de Weibul	----------------------------------------------------------------------------
	# matriz de cargas em kW
	matriz_kw = numpy.zeros((5, 3))
	dss.loads_first()
	for i in range(dss.loads_count()):
		# Defina os parâmetros da distribuição de Weibull
		MTTF = dss.loads_read_kw()  # tempo médio de falha
		beta = 2  # parâmetro de forma
		# Calcule o parâmetro de escala (eta)
		eta = MTTF / (numpy.power(numpy.log(2), 1 / beta))
		# Gere 1000 valores positivos a partir da distribuição de Weibull
		valores_gerados = weibull_min.rvs(beta, scale=eta, size=3)
		matriz_kw[i][0] = valores_gerados[0]
		matriz_kw[i][1] = valores_gerados[1]
		matriz_kw[i][2] = valores_gerados[2]
		dss.loads_next()
	# matriz de cargas em Kvar

	matriz_kvar = numpy.zeros((5, 3))
	dss.loads_first()
	for i in range(dss.loads_count()):
		# Defina os parâmetros da distribuição de Weibull
		MTTF = dss.loads_read_kvar()  # tempo médio de falha
		beta = 2  # parâmetro de forma
		# Calcule o parâmetro de escala (eta)
		eta = MTTF / (numpy.power(numpy.log(2), 1 / beta))
		# Gere 1000 valores positivos a partir da distribuição de Weibull
		valores_gerados2 = weibull_min.rvs(beta, scale=eta, size=3)
		matriz_kvar[i][0] = valores_gerados2[0]
		matriz_kvar[i][1] = valores_gerados2[1]
		matriz_kvar[i][2] = valores_gerados2[2]
		dss.loads_next()

# Função definir qual combinação de cargas	----------------------------------------------------------------------------
	for i in range(5):
		for j in range(3):
			dss.loads_first()
			for k in range(dss.loads_count()):
				dss.loads_read_kw(matriz_kw[i][j])
				dss.loads_read_kvar(matriz_kvar[i][j])
				dss.loads_next()
			dss.solution_solve()
	# -----------------------------------------------------------------------------------------------------------------------
			# compute the value of best_position and best_fitness in the whale Population
			Xbest = sys.float_info.max
			Fbest = sys.float_info.max

			for i in range(n): # check each whale
				for j in range(dim):
					if whalePopulation[i].fitness[j] < Fbest:
						Fbest = whalePopulation[i].fitness[j]
						Xbest = copy.copy(whalePopulation[i].position[j])
			# main loop of woa
			Iter = 0
			while Iter < max_iter:
				# after every 10 iterations
				# print iteration number and best fitness value so far
				if Iter % 10 == 0 and Iter > 1:
					print("Iter = " + str(Iter) + " best fitness = %.3f" % Fbest)

				# linearly decreased from 2 to 0
				a = 2 * (1 - Iter / max_iter)
				a2=-1+Iter*((-1)/max_iter)

				for i in range(n):
					A = 2 * a * rnd.random() - a
					C = 2 * rnd.random()
					b = 1
					l = (a2-1)*rnd.random()+1;
					p = rnd.random()

					D = [0.0 for i in range(dim)]
					D1 = [0.0 for i in range(dim)]
					Xnew = [0.0 for i in range(dim)]
					Xrand = [0.0 for i in range(dim)]
					if p < 0.5:
						if abs(A) > 1:
							for j in range(dim):
								D[j] = abs(C * Xbest - whalePopulation[i].position[j])
								Xnew[j] = Xbest - A * D[j]
						else:
							p = random.randint(0, n - 1)
							while (p == i):
								p = random.randint(0, n - 1)

							Xrand = whalePopulation[p].position

							for j in range(dim):
								D[j] = abs(C * Xrand[j] - whalePopulation[i].position[j])
								Xnew[j] = Xrand[j] - A * D[j]
					else:
						for j in range(dim):
							D1[j] = abs(Xbest - whalePopulation[i].position[j])
							Xnew[j] = D1[j] * math.exp(b * l) * math.cos(2 * math.pi * l) + Xbest

					for j in range(dim):
						whalePopulation[i].position[j] = abs(int(Xnew[j]))

				for i in range(n):
					# if Xnew < minx OR Xnew > maxx
					# then clip it
					for j in range(dim):
						whalePopulation[i].position[j] = abs(int(max(whalePopulation[i].position[j], minx)))
						whalePopulation[i].position[j] = abs(int(min(whalePopulation[i].position[j], maxx)))

		# Função para implementar a unidade de GD ------------------------------------------------------------------------------
						buses = dss.circuit_all_bus_names()
						mv_bus_voltage_dict = dict()
						if whalePopulation[i].position[j] in buses:
							p_step = 10
							v_threshold = 1.05
							kva_to_kw = 1
							pf = 1
							dss.circuit_set_active_bus(whalePopulation[i].position[j])
							if whalePopulation[i].position[j] == "sourcebus":
								pass
							elif dss.bus_kVbase() >= 1.0 and len(dss.bus_nodes()) == 3:
								mv_bus_voltage_dict[whalePopulation[i].position[j]] = dss.bus_kVbase()
								functions.define_3ph_pvsystem(dss, whalePopulation[i].position[j], mv_bus_voltage_dict[whalePopulation[i].position[j]], p_step * kva_to_kw, p_step)
								functions.add_bus_marker(dss, whalePopulation[i].position[j], "blue", 2)

							dss.text("Solve")
		# ----------------------------------------------------------------------------------------------------------------------
		# Função restrição de tensão -------------------------------------------------------------------------------------------
						v_pu_nodes = []
						v_pu_nodes.append(dss.circuit_all_bus_vmag_pu())
						max_value_v_pu = numpy.max(v_pu_nodes)
						min_value_v_pu = numpy.min(v_pu_nodes)

						if max_value_v_pu > 1.05:
							V_rest = 0
						elif min_value_v_pu < 0.95:
							V_rest = 0
						else:
							V_rest = 1
		#-----------------------------------------------------------------------------------------------------------------------
		# Função restrição de fluxo de potencia --------------------------------------------------------------------------------
		#				dss.lines_first()
		#				for _ in range(dss.lines_count()):
		#					if dss.lines_read_phases() == 3:
		#						dss.circuit_set_active_element(dss.lines_read_name())
		#						current = dss.cktelement_currents_mag_ang()
		#						rating_current = dss.cktelement_read_norm_amps()
		#						if max(current[0:12:2]) / rating_current > 1:
		#							thermal_violation = 1
		#						else:
		#							thermal_violation = 0
		#					dss.lines_next()
		#-----------------------------------------------------------------------------------------------------------------------
		# Função objetivo potencia Redução potencia ativa e reativa
		#-----------------------------------------------------------------------------------------------------------------------
		# Função Objetiva VSI---------------------------------------------------------------------------------------------------
		#-----------------------------------------------------------------------------------------------------------------------
		# Função objetivos de variação de tensão--------------------------------------------------------------------------------
						vdeviation_1 = ((1 - abs(max_value_v_pu)) / abs(max_value_v_pu))
						vdeviation_2 = ((1 - abs(min_value_v_pu)) / abs(min_value_v_pu))

						if (vdeviation_2 > vdeviation_1):
							fitness_value = vdeviation_2
						else:
							fitness_value = vdeviation_1
		# ----------------------------------------------------------------------------------------------------------------------
						whalePopulation[i].fitness[j] = fitness_value
						if (whalePopulation[i].fitness[j] < Fbest):
		#					if Rest_pot==0:
								if V_rest==0:
									Xbest = whalePopulation[i].position[j]
									Fbest = whalePopulation[i].fitness[j]

				Iter += 1
			dss.text("New EnergyMeter.Feeder Line.L115 1")
			dss.text("solve")
			dss.text("Buscoords Buscoords.dat")
			dss.text("Plot Profile")
			dss.text("plot profile phases=all")
			dss.text("Redirect CircuitplottingScripts.DSS")
			dss.text("plot Loadshape Object=default")

			print("\nWOA completed\n")
			print("\nBest solution found:")
			print(Xbest)
			print("\nBest Err found:")
			print(Fbest)
			# end-while
			# returning the best solution
			load_buses = list()
			loads = dss.loads_all_names()
			for load in loads:
				dss.circuit_set_active_element(load)
				load_buses = load_buses + dss.cktelement_read_bus_names()
			for bus in load_buses:
				functions.add_bus_marker(dss, bus, "red", 5)
			dss.text("Interpolate")
			dss.solution_solve()
			dss.text("Plot circuit")
	return Xbest

# Interface com usuário ------------------------------------------------------------------------------------------------
# Resultado para a função objetivo de melhor indice de estabilidade de Tensão

print("\nBegin whale optimization algorithm on rastrigin function\n")
dim = 1
num_whales = 5
max_iter = 100

print("Setting num_whales = " + str(num_whales))
print("Setting max_iter = " + str(max_iter))
print("\nStarting WOA algorithm\n")

best_position = woa(max_iter, num_whales, dim, 1.0, 500.0)

dss.circuit_all_bus_names
dss.cir