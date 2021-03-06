# Three-particle collision integral

\begin{multline}
    I_{coll}(t,p_1) = \frac{1}{2 E_1} \int
        \frac{d^3 p_2}{(2 \pi)^3 2 E_2} \frac{d^3 p_3}{(2 \pi)^3 2 E_3}
        S |\mathcal{\overline{M}}|^2 \mathcal{F}(\{f_\alpha\}) (2 \pi)^4
        \delta^4(p_1 - p_2 - p_3)
\end{multline}

In the following, we will assume that the matrix element of the reaction is constant. This
follows from the fact that the decaying particle has to be massive and that the decay rate in the
rest frame cannot depend on anything but particle mass. Matrix element is a Lorentz scalar, so its
value in any reference frame has to be equal to the rest frame value. Which is constant.

\begin{align}
    I_{coll}(t,p_1)
        &= \frac{S |\mathcal{\overline{M}}|^2 }{32 \pi^2 E_1} \int \frac{d^3 p_2}{E_2} \frac{d^3 p_3}{E_3}
            \mathcal{F}(\{f_\alpha\}) \delta^4(p_1 - p_2 - p_3)
        \\ &= \frac{S |\mathcal{\overline{M}}|^2 }{32 \pi^2 E_1} \int \frac{p_2^2 d p_2}{E_2} \frac{p_3^2 d p_3}{E_3}
            d \Omega_2 d \Omega_3 \mathcal{F}(\{f_\alpha\})
            \delta^3(\vec{p}_1 - \vec{p}_2 - \vec{p}_3) \delta(E_1-E_2-E_3)
\end{align}

We can get rid of the remaining delta-functions using their integral representation:

\begin{align}
    \delta^3(\vec{p}) = \int \frac{\lambda^2 d \lambda}{(2 \pi)^3} d \Omega_\lambda e^{\imath \vec{\lambda} \cdot \vec{p}}
\end{align}

\begin{align}
    I_{coll}(t,p_1)
        &= \frac{S |\mathcal{\overline{M}}|^2 }{(2\pi)^5 8 E_1}
            \int \frac{p_2^2 d p_2}{E_2} \frac{p_3^2 d p_3}{E_3} \lambda^2 d \lambda
            d \Omega_2 d \Omega_3 d \Omega_\lambda \ \mathcal{F}(f_\alpha)
            e^{\imath (\vec{p}\_1 - \vec{p}\_2 - \vec{p}\_3) \cdot \vec{\lambda}}
            \ \delta(E_1-E_2-E_3)
        \\ &= -\frac{(2\pi)^3 S |\mathcal{\overline{M}}|^2 }{(2\pi)^5 8 E_1}
            \int \frac{p_2^2 d p_2}{E_2} \frac{p_3^2 d p_3}{E_3} \lambda^2 d \lambda
            \ d \cos \theta_2 \ d \cos \theta_3 \ d \cos \theta_\lambda \ \mathcal{F}(f_\alpha)
            e^{\imath p_1 \lambda \cos \theta_\lambda - \imath p_2 \lambda \cos \theta_2 - \imath p_3 \lambda \cos \theta_3}
            \delta(E_1-E_2-E_3)
        \\ &= -\frac{S |\mathcal{\overline{M}}|^2 }{(2\pi)^2 8 E_1}
            \int \frac{p_2^2 d p_2}{E_2} \frac{p_3^2 d p_3}{E_3} \lambda^2 d \lambda
            \int d \cos \theta_2 e^{- \imath p_2 \lambda \cos \theta_2}
            \int d \cos \theta_3 e^{- \imath p_3 \lambda \cos \theta_3}
            \int d \cos \theta_\lambda e^{\imath p_1 \lambda \cos \theta_\lambda}
            \mathcal{F}(f_\alpha) \delta(E_1-E_2-E_3)
\end{align}

As the distributions are functions of energy only, the above expression is significantly simplified:

\begin{align}
    \int d \cos \theta e^{\pm \imath p \lambda \cos \theta} = -2 \frac{\sin p\lambda}{p \lambda}
\end{align}

\begin{align}
    I_{coll}(t,p_1)
        &= \frac{S |\mathcal{\overline{M}}|^2 }{(2\pi)^2 E_1}
            \int \frac{p_2^2 d p_2}{E_2} \frac{p_3^2 d p_3}{E_3} \lambda^2 d \lambda
            \mathcal{F}(f_\alpha)
            \frac{\sin p_2\lambda}{p_2 \lambda}
            \frac{\sin p_3\lambda}{p_3 \lambda}
            \frac{\sin p_1 \lambda}{p_1 \lambda}
            \ \delta(E_1-E_2-E_3)
        \\ &= \frac{S |\mathcal{\overline{M}}|^2 }{4 \pi^2 E_1 p_1}
            \int \frac{p_2 d p_2}{E_2} \frac{p_3 d p_3}{E_3}
            \mathcal{F}(f_\alpha) \ \delta(E_1-E_2-E_3)
            \int \frac{d \lambda}{\lambda}  \sin p_1 \lambda \sin p_2\lambda \sin p_3\lambda
\end{align}

The integral over $\lambda$ boils down to

\begin{align}
    \int \frac{d \lambda}{\lambda}  \sin p_1 \lambda \sin p_2\lambda \sin p_3\lambda &=
    -\frac{\pi}{8} (sign(p_1+p_2+p_3) + sign(p_1-p_2-p_3) - sign(p_1+p_2-p_3) - sign(p_1-p_2+p_3))
    \\ &= \frac{\pi}{4} \ \ \ \text{for kinematicaly allowed configurations of momenta}
\end{align}

The last condition can be expressed as a triangle rule: \
$a(\{ p \}) = \bigcap_{i j k} (p_i + p_j > p_k) $.

Finally, applying the delta function

\begin{align}
    I_{coll}(t,p_1)
        &= \frac{S |\mathcal{\overline{M}}|^2 }{16 \pi E_1 p_1}
            \int \frac{p_2 d p_2}{E_2} \mathcal{F}(f_\alpha) \ \theta(E_3-m_3) \ a(\{ p \})
\end{align}

As we see, the Boltzmann integral simplified to a single integration over the momenta of one of
the particles. From the kinematical point of view, reaction $1 \to 2 + 3$ has single free parameter
- the scattering angle of one of the decay products. Averaging over it can be expressed as
an integration that we indeed obtained.
