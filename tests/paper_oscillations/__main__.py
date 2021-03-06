# -*- coding: utf-8 -*-
"""

"""

import argparse
import os.path as op
from collections import defaultdict

from particles import Particle
from library.SM import particles as SMP, interactions as SMI
from library.NuMSM import particles as NuP, interactions as NuI
from evolution import Universe
from common import UNITS, Params, utils, LogSpacedGrid, LinearSpacedGrid


parser = argparse.ArgumentParser(description='Run simulation for given mass and mixing angle')
parser.add_argument('--mass', required=True)
parser.add_argument('--theta', required=True)
parser.add_argument('--tau', required=True)
parser.add_argument('--Tdec', default=100)
parser.add_argument('--Twashout', default=0.1)
parser.add_argument('--comment', default='')
args = parser.parse_args()

mass = float(args.mass) * UNITS.MeV
theta = float(args.theta)
lifetime = float(args.tau) * UNITS.s
Tdec = float(args.Tdec) * UNITS.MeV
T_washout = float(args.Twashout) * UNITS.MeV

folder = utils.ensure_dir(
    op.split(__file__)[0],
    'output',
    "mass={mass:e}_tau={tau:e}_theta={theta:e}_Tdec={Tdec:e}_Twashout={Twashout:e}"
    .format(
        mass=mass / UNITS.MeV,
        tau=lifetime / UNITS.s, theta=theta,
        Tdec=Tdec / UNITS.MeV,
        Twashout=T_washout / UNITS.MeV
    ) + args.comment
)


T_initial = Tdec
T_weak_decoupling = 5 * UNITS.MeV
T_final = 0.0008 * UNITS.MeV
params = Params(T=T_initial,
                dy=0.003125*4)

universe = Universe(params=params, folder=folder)

photon = Particle(**SMP.photon)
electron = Particle(**SMP.leptons.electron)
muon = Particle(**SMP.leptons.muon)


active_grid = LinearSpacedGrid(MOMENTUM_SAMPLES=201,
                               MAX_MOMENTUM=mass / T_washout * 1.5 * UNITS.MeV)
neutrino_e = Particle(**SMP.leptons.neutrino_e,
                      grid=active_grid)
neutrino_mu = Particle(**SMP.leptons.neutrino_mu,
                       grid=active_grid)
neutrino_tau = Particle(**SMP.leptons.neutrino_tau,
                        grid=active_grid)

sterile_grid = LogSpacedGrid(MOMENTUM_SAMPLES=51, MAX_MOMENTUM=20 * UNITS.MeV)
sterile = Particle(**NuP.dirac_sterile_neutrino(mass),
                   grid=sterile_grid)
sterile.decoupling_temperature = Tdec


universe.add_particles([
    photon,
    electron,
    muon,
    neutrino_e,
    neutrino_mu,
    neutrino_tau,
    sterile,
])

thetas = defaultdict(float, {
    'electron': theta,
})

universe.interactions += (
    SMI.neutrino_interactions(
        leptons=[electron],
        neutrinos=[neutrino_e, neutrino_mu, neutrino_tau]
    ) + NuI.sterile_leptons_interactions(
        thetas=thetas, sterile=sterile,
        neutrinos=[neutrino_e, neutrino_mu, neutrino_tau],
        leptons=[electron, muon]
    )
)

universe.init_kawano(electron=electron, neutrino=neutrino_e)
universe.init_oscillations(SMP.leptons.oscillations_map(), (neutrino_e, neutrino_mu, neutrino_tau))


def step_monitor(universe):
    # explanation of what is inside the file + first row which is a grid on y
    if universe.step == 1:
        for particle in [neutrino_e, neutrino_mu, neutrino_tau, sterile]:
            with open(op.join(folder, particle.name.replace(' ', '_') + ".distribution.txt"), 'a') as f:
                f.write('# First line is a grid of y; Starting from second line: '
                        + 'first number is a, second is temperature, next is set of numbers '
                        + 'is corresponding to f(y) on the grid\n')
                f.write('## a\tT\t' + '\t'.join([
                    '{:e}'.format(x)
                    for x in
                    particle.grid.TEMPLATE / UNITS.MeV
                ]) + '\n')
            with open(op.join(folder, particle.name.replace(' ', '_') + ".rho.txt"), 'a') as f:
                f.write('## a\tT, MeV\taT, MeV\trho_nu, MeV^4\ta^3 n, MeV^3\n')

    # Output the distribution function and collision integrals distortion to file every 10 steps,
    # first column is temperature
    if universe.step % 10 == 0:
        for particle in [neutrino_e, neutrino_mu, neutrino_tau, sterile]:
            with open(op.join(folder, particle.name.replace(' ', '_') + ".distribution.txt"), 'a') as f:
                f.write('{a:e}\t{T:e}\t'.format(a=universe.params.a, T=universe.params.T / UNITS.MeV))
                f.write('\t'.join(['{:e}'.format(x) for x in particle._distribution]) + '\n')

            with open(op.join(folder, particle.name.replace(' ', '_') + ".rho.txt"), 'a') as f:
                f.write(
                    '{a:e}\t{t:e}\t{T:e}\t{aT:e}\t{rho:e}\t{n:e}\n'.format(
                        a=universe.params.a,
                        t=universe.params.t / UNITS.s,
                        T=universe.params.T / UNITS.MeV,
                        aT=universe.params.aT / UNITS.MeV,
                        rho=particle.energy_density / UNITS.MeV**4,
                        n=universe.params.a**3 * particle.density / UNITS.MeV**3
                    )
                )


universe.step_monitor = step_monitor

universe.evolve(T_weak_decoupling, export=False)
universe.params.dy = 0.003125
universe.params.infer()
universe.evolve(T_washout, export=False)
sterile._distribution *= 0
universe.interactions = tuple()
universe.evolve(T_final)

"""
### Plots for comparison with articles

### JCAP10(2012)014, Figure 9
<img src="figure_9.svg" width=100% />

### JCAP10(2012)014, Figure 10
<img src="figure_10.svg" width=100% />
<img src="figure_10_full.svg" width=100% />
"""
