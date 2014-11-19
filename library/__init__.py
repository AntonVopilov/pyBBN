# -*- coding: utf-8 -*-

from common import UNITS, CONST
from particles import STATISTICS
from interaction import Interaction, WeakM


class StandardModelParticles:
    """ A collection of Standard Model particles templates to be used as a reference and to avoid\
        typical mistakes such as wrong degree of freedom for the neutrinos (2, not 4 - there are\
        no right-handed neutrinos and left-handed antineutrinos). """

    photon = {
        'name': 'Photon',
        'symbol': 'γ',
        'statistics': STATISTICS.BOSON,
        'dof': 2
    }
    neutrino_e = {
        'name': 'Electron neutrino',
        'symbol': 'ν_e',
        'statistics': STATISTICS.FERMION,
        'dof': 2,
        'decoupling_temperature': 5 * UNITS.MeV
    }
    neutrino_mu = {
        'name': 'Muon neutrino',
        'symbol': 'ν_μ',
        'statistics': STATISTICS.FERMION,
        'dof': 2,
        'decoupling_temperature': 5 * UNITS.MeV
    }
    neutrino_tau = {
        'name': 'Tau neutrino',
        'symbol': 'ν_τ',
        'statistics': STATISTICS.FERMION,
        'dof': 2,
        'decoupling_temperature': 5 * UNITS.MeV
    }
    neutron = {
        'name': 'Neutron',
        'symbol': 'n',
        'statistics': STATISTICS.FERMION,
        'mass': 0.939 * UNITS.GeV,
        'dof': 4
    }
    proton = {
        'name': 'Proton',
        'symbol': 'p',
        'statistics': STATISTICS.FERMION,
        'mass': 0.938 * UNITS.GeV,
        'dof': 4
    }
    electron = {
        'name': 'Electron',
        'symbol': 'e',
        'statistics': STATISTICS.FERMION,
        'mass': 0.511 * UNITS.MeV,
        'dof': 4
    }
    muon = {
        'name': 'Muon',
        'symbol': 'μ',
        'statistics': STATISTICS.FERMION,
        'mass': 105.7 * UNITS.MeV,
        'dof': 4
    }
    tau = {
        'name': 'Tau',
        'symbol': 'τ',
        'statistics': STATISTICS.FERMION,
        'mass': 1777 * UNITS.MeV,
        'dof': 4
    }


class StandardModelInteractions:

    @staticmethod
    def neutrino_self_scattering(neutrino):
        """ \begin{align}
                \nu_\alpha + \nu_\alpha &\to \nu_\alpha + \nu_\alpha
                \\\\ \nu_\alpha + \overline{\nu_\alpha} &\to \nu_\alpha + \overline{\nu_\alpha}
            \end{align} """
        return Interaction(
            name="Neutrino self-scattering",
            in_particles=[neutrino, neutrino],
            out_particles=[neutrino, neutrino],
            decoupling_temperature=0 * UNITS.MeV,
            Ms=[WeakM(K1=6, K2=0., order=(0, 1, 2, 3))]
        )

    @staticmethod
    def neutrino_inter_scattering(neutrino_a, neutrino_b):
        """ \begin{align}
                \nu_\alpha + \nu_\beta &\to \nu_\alpha + \nu_\beta
                \\\\ \nu_\alpha + \overline{\nu_\beta} &\to \nu_\alpha + \overline{\nu_\beta}
            \end{align} """
        return Interaction(
            name="Neutrino species-scattering",
            in_particles=[neutrino_a, neutrino_b],
            out_particles=[neutrino_a, neutrino_b],
            decoupling_temperature=0 * UNITS.MeV,
            Ms=[WeakM(K1=2, K2=0., order=(0, 1, 2, 3))]
        )

    @staticmethod
    def neutrino_pair_flavour_change(neutrino_a, neutrino_b):
        """ \begin{align}
                \nu_\alpha + \overline{\nu_\alpha} &\to \nu_\beta + \overline{\nu_\beta}
            \end{align} """
        return Interaction(
            name="Neutrino pair flavor change",
            in_particles=[neutrino_a, neutrino_a],
            out_particles=[neutrino_b, neutrino_b],
            decoupling_temperature=0 * UNITS.MeV,
            Ms=[WeakM(K1=1., K2=0., order=(0, 1, 2, 3))]
        )

    @staticmethod
    def neutrinos_to_electrons(neutrino=None, electron=None, g_L=CONST.g_R + 0.5):
        """ \begin{align}
                \nu_\alpha + \overline{\nu_\alpha} &\to e^- + e^+
            \end{align} """
        return Interaction(
            name="Neutrino-anti-neutrino annihilation to electron-positron pair",
            in_particles=[neutrino, neutrino],
            out_particles=[electron, electron],
            decoupling_temperature=0 * UNITS.MeV,
            Ms=[
                WeakM(K1=4 * CONST.g_L**2, order=(0, 3, 1, 2)),
                WeakM(K1=4 * CONST.g_R**2, order=(0, 2, 1, 3)),
                WeakM(K2=-4 * CONST.g_L * CONST.g_R, order=(2, 3, 0, 1)),
            ]
        )

    @staticmethod
    def neutrino_electron_scattering(neutrino=None, electron=None, g_L=CONST.g_R + 0.5):
        """ \begin{align}
                \nu_\alpha + e^- &\to \nu_\alpha + e^-
            \end{align} \begin{align}
                \nu_\alpha + e^+ &\to \nu_\alpha + e^+
            \end{align} """
        return Interaction(
            name="Neutrino-electron scattering",
            in_particles=[neutrino, neutrino],
            out_particles=[electron, electron],
            decoupling_temperature=0 * UNITS.MeV,
            Ms=[
                WeakM(K1=4 * (CONST.g_R**2 + g_L**2), order=(0, 1, 2, 3)),
                WeakM(K1=4 * (CONST.g_R**2 + g_L**2), order=(0, 3, 1, 2)),
                WeakM(K2= -2 * 4 * g_L * CONST.g_R, order=(2, 3, 0, 2)),
            ]
        )