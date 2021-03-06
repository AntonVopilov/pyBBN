from library.SM import particles as SMP
from interactions import CrossGeneratingInteraction
from interactions.four_particle import FourParticleM, FourParticleIntegral
from particles import Particle
from evolution import Universe
from common import CONST, UNITS, Params


params = Params(T=2 * UNITS.MeV,
                dy=0.025)

photon = Particle(**SMP.photon)
neutrino = Particle(**SMP.leptons.neutrino_e)

neutrino_scattering = CrossGeneratingInteraction(
    particles=((neutrino, neutrino), (neutrino, neutrino)),
    antiparticles=((False, True), (False, True)),
    Ms=(FourParticleM(K1=64 * CONST.G_F**2, order=(0, 1, 2, 3)),),
    integral_type=FourParticleIntegral
)

universe = Universe(params=params)
universe.PARALLELIZE = False
universe.add_particles([photon, neutrino])
universe.interactions += [neutrino_scattering]


import numpy
addition = numpy.vectorize(lambda x: 0.1 * numpy.exp(-(x/UNITS.MeV-3)**2),
                           otypes=[numpy.float_])
neutrino._distribution += addition(neutrino.grid.TEMPLATE)

# def check(p=[]):
#     return neutrino_scattering.F_B(in_p=p[:2], out_p=p[2:]) * (1 - neutrino.distribution(p[0])) \
#         - neutrino_scattering.F_A(in_p=p[:2], out_p=p[2:]) * neutrino.distribution(p[0])


# # print [neutrino.distribution(p) - neutrino._distribution_interpolation(p)
# #        for p in numpy.linspace(neutrino.grid.MIN_MOMENTUM, neutrino.grid.MAX_MOMENTUM,
# #                                num=200, endpoint=True)]

import matplotlib.pyplot as plt

x = numpy.linspace(neutrino.grid.MIN_MOMENTUM, neutrino.grid.MAX_MOMENTUM*2,
                   num=neutrino.grid.MOMENTUM_SAMPLES*100, endpoint=True)[1:]
y = numpy.vectorize(neutrino.distribution)(x)
z = neutrino.equilibrium_distribution(x)
w = z + addition(x)

plt.ioff()
plt.plot(x / UNITS.MeV, y, label="interpolated distribution", alpha=0.5)
plt.plot(x / UNITS.MeV, z, label="equilibrium distribution", alpha=0.5, linestyle='--')
plt.plot(x / UNITS.MeV, w, label="analytic", alpha=0.5, linestyle=':')
plt.plot(neutrino.grid.TEMPLATE / UNITS.MeV, neutrino._distribution, label="points", alpha=1, linewidth=0, linestyle=None, marker='x')
plt.plot(neutrino.grid.TEMPLATE / UNITS.MeV, numpy.vectorize(neutrino.distribution)(neutrino.grid.TEMPLATE), label="interpolated points", alpha=0.5, linewidth=1)

plt.xscale('log')
# plt.yscale('log')
plt.legend()

plt.show()
plt.draw()

# res = []
# for p0 in neutrino.grid.TEMPLATE:
#     for p1 in neutrino.grid.TEMPLATE:
#         for p2 in neutrino.grid.TEMPLATE:
#             p3 = p0 + p1 - p2
#             if p3 >= 0 and p3 <= neutrino.grid.MAX_MOMENTUM:
#                 # val = check(p=[p0, p1, p2, p3])
#                 # f0 = neutrino.distribution(p0)
#                 # f1 = neutrino.distribution(p1)
#                 # f2 = neutrino.distribution(p2)
#                 # f3 = neutrino.distribution(p3)
#                 # val = f2 * f3 * (1 - f0) * (1 - f1) - f0 * f1 * (1 - f2) * (1 - f3)
#                 res.append(val)

# from interactions.ds import D1, D2, D3
# from plotting import plot_integrand

# plot_integrand(lambda (p1, p2): D1(p1, p2, 1, 1), 'D1', 0)
# plot_integrand(lambda (p1, p2): D2(p1, p2, 1, 1), 'D2', 0)
# plot_integrand(lambda (p1, p2): D3(p1, p2, 1, 1), 'D3', 0)

# raw_input("...")
