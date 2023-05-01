import numpy
from scipy.stats import weibull_min

# Defina os parâmetros da distribuição de Weibull
MTTF = 200  # tempo médio de falha
beta = 2  # parâmetro de forma

# Calcule o parâmetro de escala (eta)
eta = MTTF / (numpy.power(numpy.log(2), 1/beta))

# Gere 1000 valores positivos a partir da distribuição de Weibull
valores_gerados = weibull_min.rvs(beta, scale=eta, size=3)

# Imprima os valores gerados
print(valores_gerados)