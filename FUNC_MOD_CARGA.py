import random
import numpy
import math # cos() for Rastrigin
import copy # array-copying convenience
import sys # max float
import py_dss_interface
import cmath


#FUNÇÃO PARA SIMULAR A VARIAÇÃO DE CARGA EM DE CONSUMIDORES INDUSTRIAIS EM UM DIA.

a1 = 5731
a5 = 460
b1 = 0.1089
b5 = 1.089
c1 = 0.3621
c5 = -2.564
a2 = 1243
a6 = 50.09
b2 = 0.2
b6 = 1.534
c2 = 3.502
c6 = -1.348
a3 = 774.1
a7 = 87.16
b3 = 0.5319
b7 = 2.302
c3 = 1.502
c7 = -5.034
a4 = 736.4
a8 = 126.6
b4 = 0.7366
b8 = 2.003
c4 = 1.939
c8 = -1.25
t = 0

Fload = a1*math.sin(b1*t+c1)+a2*math.sin(b2*t+c2)+a3*math.sin(b3*t+c3)+a4*math.sin(b4*t+c4)+a5*math.sin(b5*t+c5)+a6*math.sin(b6*t+c6)+a7*math.sin(b7*t+c7)+a8*math.sin(b8*t+c8)

mv_buses = list()
mv_bus_voltage_dict = dict()

for bus in buses:
    dss.circuit_setactivebus(bus)
    if bus == "sourcebus":
        pass
    elif dss.bus_kVbase() >= 1.0 and len(dss.bus_nodes()) == 3:
        mv_buses.append(bus)
        mv_bus_voltage_dict[bus] = dss.bus_kVbase()
# python implementation of whale optimization algorithm (WOA)
# minimizing rastrigin and sphere function



# -------fitness functions---------

def open_dss_file():
	# Acessa o opendss
	dss = py_dss_interface.DSSDLL()
	dss_file = r"C:\Users\pedro\Documents\OpenDSS\TCC\WOA\123Bus_No_Print\IEEE123Master.dss"
	dss.text("compile {}".format(dss_file))
	return

# Função objetivo para o indice VSi
def fitness_voltage(position):
	fitness_value = 0.0
	for i in range(len(position)):
		xi = position[i]
		fitness_value += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10
	return fitness_value


# Função objetivo para o indice de perdas
def fitness_power(position):
	fitness_value = 0.0
	for i in range(len(position)):
		xi = position[i]
		fitness_value += (xi * xi);
	return fitness_value;
# -------------------------
# whale class
class whale:
	def __init__(self, fitness, dim, minx, maxx, seed):
		self.rnd = random.Random(seed)
		self.position = [0.0 for i in range(dim)]

		for i in range(dim):
			self.position[i] = ((maxx - minx) * self.rnd.random() + minx)

		self.fitness = fitness(self.position) # curr fitness

# whale optimization algorithm(WOA)
def woa(fitness, max_iter, n, dim, minx, maxx):
	rnd = random.Random(0)

	# create n random whales
	whalePopulation = [whale(fitness, dim, minx, maxx, i) for i in range(n)]

	# compute the value of best_position and best_fitness in the whale Population
	Xbest = [0.0 for i in range(dim)]
	Fbest = sys.float_info.max

	for i in range(n): # check each whale
		if whalePopulation[i].fitness < Fbest:
			Fbest = whalePopulation[i].fitness
			Xbest = copy.copy(whalePopulation[i].position)

	# main loop of woa
	Iter = 0
	while Iter < max_iter:

		#open_dss_file()
		dss = py_dss_interface.DSSDLL()
		dss_file = r"C:\Users\pedro\Documents\OpenDSS\TCC\WOA\123Bus_No_Print\IEEE123Master.dss"
		dss.text("compile {}".format(dss_file))

		v_pu_nodes = dss.circuit_all_node_vmag_pu_by_phase()
		max_value_v_pu = numpy.max(v_pu_nodes)
		min_value_v_pu = numpy.min(v_pu_nodes)

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
						D[j] = abs(C * Xbest[j] - whalePopulation[i].position[j])
						Xnew[j] = Xbest[j] - A * D[j]
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
					D1[j] = abs(Xbest[j] - whalePopulation[i].position[j])
					Xnew[j] = D1[j] * math.exp(b * l) * math.cos(2 * math.pi * l) + Xbest[j]

			for j in range(dim):
				whalePopulation[i].position[j] = Xnew[j]

		for i in range(n):
			# if Xnew < minx OR Xnew > maxx
			# then clip it
			for j in range(dim):
				whalePopulation[i].position[j] = max(whalePopulation[i].position[j], minx)
				whalePopulation[i].position[j] = min(whalePopulation[i].position[j], maxx)

			whalePopulation[i].fitness = fitness(whalePopulation[i].position)

			if (whalePopulation[i].fitness < Fbest):
				Xbest = copy.copy(whalePopulation[i].position)
				Fbest = whalePopulation[i].fitness


		Iter += 1
	# end-while
	print(dss.circuit_num_buses())
	print(dss.circuit_num_nodes())
	print(dss.circuit_line_losses())
	print(dss.circuit_losses())
	print(dss.circuit_all_bus_names())

	# returning the best solution
	return Xbest


# ----------------------------


# Resultado para a função objetivo de melhor indice de estabilidade de Tensão

print("\nBegin whale optimization algorithm on rastrigin function\n")
dim = 3
fitness = fitness_voltage

print("Goal is to minimize Rastrigin's function in " + str(dim) + " variables")
print("Function has known min = 0.0 at (", end="")
for i in range(dim - 1):
	print("0, ", end="")
print("0)")

num_whales = 50
max_iter = 1

print("Setting num_whales = " + str(num_whales))
print("Setting max_iter = " + str(max_iter))
print("\nStarting WOA algorithm\n")

best_position = woa(fitness, max_iter, num_whales, dim, -10.0, 10.0)

print("\nWOA completed\n")
print("\nBest solution found:")
print(["%.6f" % best_position[k] for k in range(dim)])
err = fitness(best_position)
print("fitness of best solution = %.6f" % err)

print("\nEnd WOA for rastrigin\n")

print()
print()

# Resultado para a função objetivo de menor perdas
print("\nBegin whale optimization algorithm on sphere function\n")
dim = 3
fitness = fitness_power

print("Goal is to minimize sphere function in " + str(dim) + " variables")
print("Function has known min = 0.0 at (", end="")
for i in range(dim - 1):
	print("0, ", end="")
print("0)")

num_whales = 50
max_iter = 1

print("Setting num_whales = " + str(num_whales))
print("Setting max_iter = " + str(max_iter))
print("\nStarting WOA algorithm\n")

best_position = woa(fitness, max_iter, num_whales, dim, -10.0, 10.0)

print("\nWOA completed\n")
print("\nBest solution found:")
print(["%.6f" % best_position[k] for k in range(dim)])
err = fitness(best_position)
print("fitness of best solution = %.6f" % err)

print("\nEnd WOA for sphere\n")
