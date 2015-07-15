"""
## Massive $\nu_\tau$ ($20 MeV$) test

<img src="plots.svg" width=100% />
<img src="particles.svg" width=100% />

This test checks that in the universe filled with photons, electrons and neutrinos:

  * $a * T$ is not conserved by a factor around `1.477` and precise details of this process
  * neutrino non-equilibrium corrections reproduce the results of the Dolgov-Hansen-Semikoz papers

[Log file](log.txt)
[Distribution functions](distributions.txt)


"""

import os
import numpy
import matplotlib

from plotting import plt, RadiationParticleMonitor, MassiveParticleMonitor
from particles import Particle
from library.SM import particles as SMP, interactions as SMI
from evolution import Universe
from common import UNITS, Params, GRID

folder = os.path.split(__file__)[0]

T_initial = 20. * UNITS.MeV
T_final = 0.015 * UNITS.MeV
params = Params(T=T_initial,
                dy=0.05)

universe = Universe(params=params, folder=folder)

photon = Particle(**SMP.photon)
electron = Particle(**SMP.leptons.electron)
neutrino_e = Particle(**SMP.leptons.neutrino_e)
neutrino_mu = Particle(**SMP.leptons.neutrino_mu)
neutrino_tau = Particle(**SMP.leptons.neutrino_tau)
neutrino_tau.mass = 20 * UNITS.MeV

neutrino_e.decoupling_temperature = T_initial
neutrino_mu.decoupling_temperature = T_initial
neutrino_tau.decoupling_temperature = T_initial


universe.add_particles([
    photon,
    electron,
    neutrino_e,
    neutrino_mu,
    neutrino_tau,
])

universe.interactions += \
    SMI.neutrino_interactions(leptons=[electron], neutrinos=[neutrino_e, neutrino_mu, neutrino_tau])

universe.graphics.monitor([
    (neutrino_e, RadiationParticleMonitor),
    (neutrino_mu, RadiationParticleMonitor),
    (neutrino_tau, MassiveParticleMonitor)
])


universe.evolve(T_final)

universe.graphics.save(__file__)


""" ## Plots for comparison with articles """

plt.ion()

"""
### 1202.2841, Figure 13
<img src="figure_13.svg" width=100% /> """

plt.figure(13)
plt.title('Figure 13')
plt.xlabel('MeV/T')
plt.ylabel(u'aT')
plt.xscale('log')
plt.xlim(0.5, UNITS.MeV/params.T)
plt.xticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
plt.axes().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.plot(UNITS.MeV / numpy.array(universe.data['T']), numpy.array(universe.data['aT']) / UNITS.MeV)
plt.show()
plt.savefig(os.path.join(folder, 'figure_13.svg'))

"""
### 1202.2841, Figure 14
<img src="figure_14.svg" width=100% /> """

plt.figure(14)
plt.title('Figure 14')
plt.xlabel('Conformal momentum y = pa')
plt.ylabel('y^2 (f-f_eq), MeV^2')
plt.xlim(0, 10)

yy = GRID.TEMPLATE * GRID.TEMPLATE / UNITS.MeV**2

distributions_file = open(os.path.join(folder, 'distributions.txt'), "w")

for neutrino in (neutrino_e, neutrino_mu, neutrino_tau):
    f = neutrino._distribution
    feq = neutrino.equilibrium_distribution()
    plt.plot(GRID.TEMPLATE/UNITS.MeV, yy*(f-feq), label=neutrino.flavour)

    numpy.savetxt(distributions_file, (f, feq, f/feq), header=str(neutrino),
                  footer='-'*80, fmt="%1.5e")

plt.legend()
plt.draw()
plt.show()
plt.savefig(os.path.join(folder, 'figure_14.svg'))

# Distribution functions arrays
distributions_file.close()

# Just to be sure everything is okay
import ipdb
ipdb.set_trace()

raw_input("...")
