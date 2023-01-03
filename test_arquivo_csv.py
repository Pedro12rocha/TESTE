# particleswarm.py
# python 3.4.3
# demo of particle swarm optimization (PSO)
# solves Rastrigin's function

import numpy
import py_dss_interface
import random
import math  # cos() for Rastrigin
import copy  # array-copying convenience
import sys  # max float


# ------------------------------------
#        PROGRAMA VERSÃO TEST
#       FALTA A IMPLEMENTAÇÃO DA POLITICA DE INCENTIVO
# ------------------------------------

class Particle:
    def __init__(self, dim, minx, maxx, seed):
        self.rnd = random.Random(seed)
        self.position = [0.0 for i in range(dim)]
        self.velocity = [0.0 for i in range(dim)]
        self.best_part_pos = [0.0 for i in range(dim)]

        self.error = dim  # curr error
        self.best_part_pos = copy.copy(self.position)
        self.best_part_err = self.error  # best error
        self.best_part_tensao = [0.0 for i in range(dim)]


def Solve(max_epochs, n, dim, minx, maxx, ger):
    rnd = random.Random(0)

    # create n random particles
    swarm = [Particle(dim, minx, maxx, i) for i in range(n)]

    for i in range(n):
        for k in range(ger):
            swarm[i].position[k] = random.randint(0, dim)
            swarm[i].velocity[k] = round(random.uniform(minx, maxx), 2)

    best_swarm_pos = [0.0 for i in range(dim)]  # not necess.
    best_swarm_err = dim * 2  # swarm best

    for i in range(n):  # check each particle
        if swarm[i].error < best_swarm_err:
            best_swarm_err = swarm[i].error
            best_swarm_pos = copy.copy(swarm[i].position)

    epoch = 0
    w = 0.729  # inertia
    c1 = 1.49445  # cognitive (particle)
    c2 = 1.49445  # social (swarm)

    while epoch < max_epochs:

        for i in range(n):  # process each particle

            # |Acessa o opendss
            dss = py_dss_interface.DSSDLL()
            dss_file = r"C:\Users\pedro\Documents\OpenDSS\TCC\teste_fusao_2_exemplos.dss"
            dss.text("compile {}".format(dss_file))

            # compute new velocity of curr particle
            for k in range(dim):
                r1 = rnd.random()  # randomizations
                r2 = rnd.random()

                swarm[i].velocity[k] = ((w * swarm[i].velocity[k]) + (c1 * r1 * (swarm[i].best_part_pos[k] - swarm[i].position[k])) + (c2 * r2 * (best_swarm_pos[k] - swarm[i].position[k])))

                if swarm[i].velocity[k] < minx:
                    swarm[i].velocity[k] = minx
                elif swarm[i].velocity[k] > maxx:
                    swarm[i].velocity[k] = maxx

            # compute new position using new velocity
            for k in range(dim):
                swarm[i].position[k] += swarm[i].velocity[k]
                swarm[i].position[k] = int(swarm[i].position[k])

                if swarm[i].position[k] < 1:
                    swarm[i].position[k] = 1
                elif swarm[i].position[k] > dim:
                    swarm[i].position[k] = dim

            for j in range(ger):
                no = swarm[i].position[j]
                no = str(no)
                gerador = str(j+1)

                # Implementando geradores no sistema
                my_string = "new generator.gen bus1=node  Kw=2342 Kvar= 0.00 model=7"
                index = my_string.find(" bus")
                my_string = my_string[:index] + gerador + my_string[index:]
                index = my_string.find("  Kw")
                final_string = my_string[:index] + no + my_string[index:]

                dss.text(final_string)

            dss.text("set controlmode=STATIC")
            dss.text("set mode=snapshot")
            dss.text("set voltagebases= 12.66")
            dss.text("calcvoltagebases")
            dss.text("solve")

            v_pu_nodes = dss.circuit_all_node_vmag_pu_by_phase()

            erro_v_pu = [1] * dim
            erro_v_pu = numpy.subtract(erro_v_pu, v_pu_nodes)
            desvio_padrao_v_pu = numpy.multiply(erro_v_pu,erro_v_pu)
            desvio_padrao_v_pu= sum(desvio_padrao_v_pu)
            desvio_padrao_v_pu = desvio_padrao_v_pu/dim

            # compute error of new position

            swarm[i].error = desvio_padrao_v_pu

            # Restrição de maximo e minimo de tensão nos nos

            max_value_v_pu = numpy.max(v_pu_nodes)
            min_value_v_pu = numpy.min(v_pu_nodes)

            if (max_value_v_pu < 1.05) and (min_value_v_pu > 0.95):

                # define melhor grupo de particulas geral
                 if swarm[i].error < best_swarm_err:
                    best_swarm_err = swarm[i].error
                    best_part_err = numpy.min(best_swarm_err)
                    best_swarm_pos = copy.copy(swarm[i].position)
                    best_part_pos = numpy.min(best_swarm_pos )
                    print(best_swarm_pos)
                    print(best_part_pos)

        # for-each particle
        epoch += 1
    # while
    del best_swarm_pos[ger:dim]
    print("\n A(s) melhor(es) posição(es) nodal(is) é(sao): ")
    print(best_swarm_pos)
    print("\n O menor desvio padrão é: ")
    print(best_part_err)
    print("\n A(s) tensão(es) nodal(is) da melhor particula em pu. respectivamente: ")

    # |Acessa o opendss
    dss = py_dss_interface.DSSDLL()
    dss_file = r"C:\Users\pedro\Documents\OpenDSS\TCC\teste_fusao_2_exemplos.dss"
    dss.text("compile {}".format(dss_file))

    for j in range(ger):
        no = best_part_pos[j]
        no = str(no)
        gerador = str(j + 1)

        # Implementando geradores no sistema
        my_string = "new generator.gen bus1=node  Kw=2342 Kvar= 0.00 model=7"
        index = my_string.find(" bus")
        my_string = my_string[:index] + gerador + my_string[index:]
        index = my_string.find("  Kw")
        final_string = my_string[:index] + no + my_string[index:]

    dss.text(final_string)
    dss.text("set controlmode=STATIC")
    dss.text("set mode=snapshot")
    dss.text("set voltagebases= 12.66")
    dss.text("calcvoltagebases")
    dss.text("solve")

    v_pu_nodes = dss.circuit_all_node_vmag_pu_by_phase()
    print(v_pu_nodes)

    return best_swarm_pos


# end Solve

# tamanho da rede de distribuição
dim = 33

# quantidade de geradores a ser instalado
ger = 3

# quantidade de grupo de particulas
num_particles = 5

# maximo de interações
max_epochs = 10

# limita variações bruscas de posições
lim1 = -5.0
lim2 = 5.0

# resolve o problema proposto
best_position = Solve(max_epochs, num_particles, dim, lim1, lim2, ger)ma separated