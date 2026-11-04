# The two questions, put to the committed runs: the tables

Written by `two_questions.py` from the results files; see README.md.

## Question 1a. Does the effective member approach the stated member?

The largest distance of the ten named expectations from the checker's closed forms, by level, and the name that sets it. The two toolkits share one representation at every level (their effective members agree to 3 · 10^-15), so one table serves both. The mean of each law and E[ψ^(ϱ−1)] with ϱ = 2 sit at the floor at every level.

| member | level 1 | level 2 | level 3 | ratio 1→2 | ratio 2→3 | at the floor at level 3 |
|---|---|---|---|---|---|---|
| ℘ = 0.005 | 6.2 · 10^-4 (psi_squared) | 2.1 · 10^-4 (psi_squared) | 7.3 · 10^-5 (psi_squared) | 2.94 | 2.88 | psi_mean, psi_pow_rho_minus_1, theta_mean, worst_income_mass |
| ℘ = 0.0005 | 6.2 · 10^-4 (psi_squared) | 2.1 · 10^-4 (psi_squared) | 7.3 · 10^-5 (psi_squared) | 2.94 | 2.88 | psi_mean, psi_pow_rho_minus_1, theta_mean, worst_income_mass |
| ℘ = 0.00005 | 6.2 · 10^-4 (psi_squared) | 2.1 · 10^-4 (psi_squared) | 7.3 · 10^-5 (psi_squared) | 2.94 | 2.88 | psi_mean, psi_pow_rho_minus_1, theta_mean, worst_income_mass |
| restrained | 2 · 10^-2 (worst_income_mass) | 4.4 · 10^-3 (worst_income_mass) | 1 · 10^-3 (worst_income_mass) | 4.59 | 4.27 | psi_mean, psi_pow_rho_minus_1, theta_mean |

Every name's distance by level, for the restrained member (the natural members' differ only in the worst income's mass, which is the stated ℘ at every level):

| expectation | closed form | level 1 | level 2 | level 3 |
|---|---|---|---|---|
| psi_mean | 1 | 0 | -1.1 · 10^-16 | -2.2 · 10^-16 |
| theta_mean | 1 | 0 | -1.1 · 10^-16 | -2.2 · 10^-16 |
| psi_pow_1_minus_rho | 1.010048726 | -6.1 · 10^-4 | -2 · 10^-4 | -7 · 10^-5 |
| psi_inverse | 1.010048726 | -6.1 · 10^-4 | -2 · 10^-4 | -7 · 10^-5 |
| psi_log | -0.004999286686 | 3 · 10^-4 | 9.9 · 10^-5 | 3.4 · 10^-5 |
| psi_log_psi | 0.004997859383 | -3 · 10^-4 | -1 · 10^-4 | -3.5 · 10^-5 |
| psi_squared | 1.010040064 | -6.2 · 10^-4 | -2.1 · 10^-4 | -7.3 · 10^-5 |
| psi_pow_rho_minus_1 | 1 | 0 | -1.1 · 10^-16 | -2.2 · 10^-16 |
| psi_pow_rho | 1.010040064 | -6.2 · 10^-4 | -2.1 · 10^-4 | -7.3 · 10^-5 |
| worst_income_mass | 0 | 2 · 10^-2 | 4.4 · 10^-3 | 1 · 10^-3 |

## Question 1b. Does the Euler residual under the stated laws fall along the ladder?

The largest |r| over the request points, under the stated laws (the diagnostics' Gauss-Legendre quadrature, precision stated in each file) and under the toolkit's own representation of the laws (its nodes exactly), by level. `3+` is the method-only step: level 3's nodes with level 4's grids.

| member | toolkit | laws | level 1 | level 2 | level 3 | 3+ | ratio 2→3 | ratio 3→3+ |
|---|---|---|---|---|---|---|---|---|
| ℘ = 0.005 | HARK | stated | 1 · 10^-3 | 3.5 · 10^-4 | 1.2 · 10^-4 | 1.2 · 10^-4 | 2.89 | 1.00 |
| ℘ = 0.005 | HARK | own | 4.9 · 10^-7 | 7.6 · 10^-8 | 4.6 · 10^-9 | 4.8 · 10^-10 | 16.76 | 9.49 |
| ℘ = 0.005 | dolo | stated | 1.3 · 10^-3 | 3.5 · 10^-4 | 1.2 · 10^-4 | 1.2 · 10^-4 | 2.86 | 1.00 |
| ℘ = 0.005 | dolo | own | 1.3 · 10^-3 | 2.8 · 10^-4 | 7.7 · 10^-5 | 1.8 · 10^-5 | 3.62 | 4.23 |
| ℘ = 0.0005 | HARK | stated | 1.4 · 10^-3 | 4.7 · 10^-4 | 1.6 · 10^-4 | 1.6 · 10^-4 | 2.93 | 1.00 |
| ℘ = 0.0005 | HARK | own | 7.9 · 10^-5 | 5.3 · 10^-6 | 3.6 · 10^-7 | 2.5 · 10^-8 | 14.56 | 14.39 |
| ℘ = 0.0005 | dolo | stated | 1.3 · 10^-2 | 3.5 · 10^-3 | 8.3 · 10^-4 | 1.7 · 10^-4 | 4.22 | 4.98 |
| ℘ = 0.0005 | dolo | own | 1.3 · 10^-2 | 3.5 · 10^-3 | 8.3 · 10^-4 | 1.7 · 10^-4 | 4.22 | 4.73 |
| ℘ = 0.00005 | HARK | stated | 7.7 · 10^-3 | 6.2 · 10^-4 | 1.8 · 10^-4 | 1.8 · 10^-4 | 3.45 | 1.00 |
| ℘ = 0.00005 | HARK | own | 7.6 · 10^-3 | 6.1 · 10^-4 | 4.4 · 10^-5 | 2.8 · 10^-6 | 13.96 | 15.44 |
| ℘ = 0.00005 | dolo | stated | 9.2 · 10^-3 | 8.1 · 10^-3 | 6.9 · 10^-3 | 2.3 · 10^-3 | 1.17 | 2.98 |
| ℘ = 0.00005 | dolo | own | 9.2 · 10^-3 | 8.1 · 10^-3 | 6.9 · 10^-3 | 2.3 · 10^-3 | 1.17 | 2.98 |
| restrained | HARK | stated | 1.8 · 10^-3 | 6.8 · 10^-4 | 2.1 · 10^-4 | 2.1 · 10^-4 | 3.31 | 1.00 |
| restrained | HARK | own | 9.9 · 10^-6 | 5.1 · 10^-6 | 5.7 · 10^-7 | 7.9 · 10^-7 | 8.92 | 0.71 |
| restrained | dolo | stated | 1.8 · 10^-3 | 6.8 · 10^-4 | 2.1 · 10^-4 | 2.1 · 10^-4 | 3.31 | 0.99 |
| restrained | dolo | own | 6.6 · 10^-6 | 2.3 · 10^-6 | 9.6 · 10^-7 | 1.2 · 10^-6 | 2.39 | 0.79 |

Where the residuals sit at level 3, ℘ = 0.00005, at the request points up to m = 0.2 and at m = 1:

| m | c, HARK | c, dolo | \|Δc\|/c | r under own laws, HARK | r under own laws, dolo | r under stated laws, HARK | r under stated laws, dolo |
|---|---|---|---|---|---|---|---|
| 0.01 | 0.009932 | 0.009931 | 6.3 · 10^-5 | -1.6 · 10^-5 | 6.9 · 10^-3 | -1.6 · 10^-5 | 6.9 · 10^-3 |
| 0.02 | 0.019864 | 0.019863 | 6.2 · 10^-5 | -2.9 · 10^-5 | 6.9 · 10^-3 | -2.9 · 10^-5 | 6.9 · 10^-3 |
| 0.05 | 0.049660 | 0.049657 | 5.5 · 10^-5 | -4.4 · 10^-5 | 6.9 · 10^-3 | -4.4 · 10^-5 | 6.9 · 10^-3 |
| 0.1 | 0.099317 | 0.099314 | 2.8 · 10^-5 | -1.5 · 10^-5 | 3.9 · 10^-3 | -1.7 · 10^-5 | 3.9 · 10^-3 |
| 0.2 | 0.198611 | 0.198602 | 4.7 · 10^-5 | -3.6 · 10^-5 | 6.3 · 10^-3 | -4.5 · 10^-5 | 6.3 · 10^-3 |
| 1 | 0.964610 | 0.964604 | 6.7 · 10^-6 | 5.7 · 10^-10 | 3.9 · 10^-6 | -1.8 · 10^-4 | -1.8 · 10^-4 |

## Question 2. Do the two toolkits' solutions coincide, and within what?

The largest |c_HARK − c_dolo| at the request points (m ≤ 20, and all 39 points), beside each toolkit's own movement of the rule between levels. The kind of each step is read from the effective member: it moves across a step that changes the representation and is identical across one that does not.

| member | HARK − dolo, level 3 (m ≤ 20 / all) | HARK 2→3 | dolo 2→3 | kind of 2→3 | HARK 3→3+ | dolo 3→3+ | kind of 3→3+ | HARK − dolo at 3+ |
|---|---|---|---|---|---|---|---|---|
| ℘ = 0.005 | 1.2 · 10^-5 / 3.9 · 10^-5 | 3.3 · 10^-3 | 3.3 · 10^-3 | representation (1.4 · 10^-4) | 7.4 · 10^-11 | 9.3 · 10^-6 | method-only (0) | 3.1 · 10^-6 |
| ℘ = 0.0005 | 1.1 · 10^-5 / 3.8 · 10^-5 | 3.4 · 10^-3 | 3.4 · 10^-3 | representation (1.4 · 10^-4) | 2.7 · 10^-9 | 8.5 · 10^-6 | method-only (0) | 3 · 10^-6 |
| ℘ = 0.00005 | 2.4 · 10^-5 / 3.7 · 10^-5 | 3.5 · 10^-3 | 3.4 · 10^-3 | representation (1.4 · 10^-4) | 9.6 · 10^-8 | 1.8 · 10^-5 | method-only (0) | 6.1 · 10^-6 |
| restrained | 1.1 · 10^-5 / 3.7 · 10^-5 | 3.5 · 10^-3 | 3.4 · 10^-3 | representation (3.4 · 10^-3) | 4.1 · 10^-7 | 8.1 · 10^-6 | method-only (0) | 2.9 · 10^-6 |

The same on the relative scale, |c_HARK − c_dolo| / c_HARK over all 39 points, which the stone guide asks for the rule, with the point that sets it; and each toolkit's own relative movement across the method-only step:

| member | level 1 | level 2 | level 3 | 3+ | HARK 3→3+ | dolo 3→3+ |
|---|---|---|---|---|---|---|
| ℘ = 0.005 | 1.2 · 10^-4 at m = 50 | 4 · 10^-5 at m = 50 | 1.1 · 10^-5 at m = 50 | 2.7 · 10^-6 at m = 50 | 2.9 · 10^-10 | 7.8 · 10^-6 |
| ℘ = 0.0005 | 2.9 · 10^-4 at m = 0.01 | 7.7 · 10^-5 at m = 0.01 | 1.8 · 10^-5 at m = 0.01 | 4.1 · 10^-6 at m = 0.3 | 8 · 10^-9 | 1.6 · 10^-5 |
| ℘ = 0.00005 | 8.6 · 10^-4 at m = 0.05 | 2.4 · 10^-4 at m = 0.02 | 6.3 · 10^-5 at m = 0.01 | 1.6 · 10^-5 at m = 0.01 | 2.9 · 10^-7 | 4.7 · 10^-5 |
| restrained | 1.2 · 10^-4 at m = 50 | 3.8 · 10^-5 at m = 50 | 1 · 10^-5 at m = 50 | 2.6 · 10^-6 at m = 50 | 4 · 10^-7 | 7.5 · 10^-6 |

