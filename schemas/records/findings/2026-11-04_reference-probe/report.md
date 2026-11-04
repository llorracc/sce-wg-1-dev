## The convergence study: each setting, and the rule's movement from its base, at the request points up to m = 50

- A: 1,000 points to 200, 32 nodes a piece
- B: 2,000 points to 400 (A doubled); its base is A
- C: B at 64 nodes a piece; its base is B
- D: 4,000 points to 1,000 at 64 nodes (C doubled); its base is C
- E: B with 3,000 extra points near the limit; its base is B
- F: E at 64 nodes a piece; its base is E
- G: E with 6,000 extra points near the limit; its base is E

| member | setting | grid size | iterations | bound on the distance | max abs r (32) | (64) | diagnostic's precision | movement from the base (max rel, at m) |
|---|---|---|---|---|---|---|---|---|
| bst-p-zero-0.005 | A | 1004 | 273 | 8.68e-12 | 1.18e-08 | 1.18e-08 | 7.88e-13 | — |
| bst-p-zero-0.005 | B | 2004 | 308 | 9.97e-12 | 4.72e-10 | 4.72e-10 | 7.41e-13 | 8.50e-09 (m = 50) |
| bst-p-zero-0.005 | C | 2004 | 308 | 9.97e-12 | 4.72e-10 | 4.72e-10 | 7.49e-13 | 4.66e-13 (m = 1.2) |
| bst-p-zero-0.005 | D | 4004 | 352 | 7.67e-12 | 6.13e-11 | 6.13e-11 | 1.07e-13 | 5.99e-11 (m = 50) |
| bst-p-zero-0.005 | E | 5003 | 308 | 9.48e-12 | 2.10e-12 | 2.09e-12 | 1.36e-14 | 4.04e-11 (m = 0.01) |
| bst-p-zero-0.005 | F | 5003 | 309 | 9.18e-12 | 2.10e-12 | 2.09e-12 | 1.35e-14 | 8.18e-14 (m = 50) |
| bst-p-zero-0.005 | G | 8003 | 308 | 9.89e-12 | 1.45e-12 | 1.45e-12 | 7.17e-15 | 3.17e-13 (m = 0.92) |
| bst-p-zero-0.0005 | A | 1004 | 273 | 9.42e-12 | 6.00e-07 | 6.00e-07 | 1.11e-11 | — |
| bst-p-zero-0.0005 | B | 2004 | 309 | 9.12e-12 | 4.26e-08 | 4.26e-08 | 2.49e-13 | 1.41e-08 (m = 0.3) |
| bst-p-zero-0.0005 | C | 2004 | 309 | 9.20e-12 | 4.26e-08 | 4.26e-08 | 2.50e-13 | 7.28e-14 (m = 50) |
| bst-p-zero-0.0005 | D | 4004 | 350 | 9.96e-12 | 3.45e-09 | 3.45e-09 | 2.66e-14 | 1.07e-09 (m = 0.3) |
| bst-p-zero-0.0005 | E | 5003 | 308 | 8.91e-12 | 1.42e-11 | 1.42e-11 | 2.75e-14 | 1.07e-09 (m = 0.3) |
| bst-p-zero-0.0005 | F | 5003 | 310 | 8.49e-12 | 1.42e-11 | 1.42e-11 | 2.78e-14 | 7.25e-14 (m = 50) |
| bst-p-zero-0.0005 | G | 8003 | 309 | 9.20e-12 | 1.37e-12 | 1.38e-12 | 6.64e-15 | 1.32e-12 (m = 0.8) |
| bst-p-zero-0.00005 | A | 1004 | 273 | 9.66e-12 | 7.90e-05 | 7.90e-05 | 2.44e-09 | — |
| bst-p-zero-0.00005 | B | 2004 | 309 | 9.58e-12 | 5.01e-06 | 5.01e-06 | 3.47e-10 | 5.14e-07 (m = 0.05) |
| bst-p-zero-0.00005 | C | 2004 | 310 | 8.47e-12 | 5.01e-06 | 5.01e-06 | 3.47e-10 | 8.72e-11 (m = 0.98) |
| bst-p-zero-0.00005 | D | 4004 | 351 | 8.82e-12 | 3.65e-07 | 3.65e-07 | 3.47e-10 | 3.35e-08 (m = 0.2) |
| bst-p-zero-0.00005 | E | 5003 | 309 | 9.65e-12 | 2.48e-11 | 3.50e-10 | 3.48e-10 | 3.40e-08 (m = 0.02) |
| bst-p-zero-0.00005 | F | 5003 | 309 | 9.25e-12 | 3.45e-10 | 2.48e-11 | 3.48e-10 | 8.12e-11 (m = 0.985) |
| bst-p-zero-0.00005 | G | 8003 | 309 | 9.65e-12 | 1.35e-12 | 3.48e-10 | 3.48e-10 | 8.28e-13 (m = 0.8) |
| bst-restrained | A | 1001 | 274 | 8.88e-12 | 2.70e-12 | 2.36e-10 | 2.37e-10 | — |
| bst-restrained | B | 2001 | 309 | 9.89e-12 | 1.34e-12 | 2.37e-10 | 2.37e-10 | 8.39e-09 (m = 50) |
| bst-restrained | C | 2001 | 309 | 9.40e-12 | 2.13e-10 | 1.35e-12 | 2.13e-10 | 1.89e-10 (m = 1.3) |
| bst-restrained | D | 4001 | 351 | 8.32e-12 | 2.13e-10 | 9.56e-14 | 2.13e-10 | 5.87e-11 (m = 50) |

## The closed forms

- bst-p-zero-0.005 A: MPC at the limit, closed form 0.932063377951; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.7e-12; the first endogenous points' EGM slopes ['0.932063377951', '0.932063377951', '0.932063377951']
- bst-p-zero-0.005 B: MPC at the limit, closed form 0.932063377951; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.7e-12; the first endogenous points' EGM slopes ['0.932063377951', '0.932063377951', '0.932063377951']
- bst-p-zero-0.005 C: MPC at the limit, closed form 0.932063377951; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.7e-12; the first endogenous points' EGM slopes ['0.932063377951', '0.932063377951', '0.932063377951']
- bst-p-zero-0.005 D: MPC at the limit, closed form 0.932063377951; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.7e-12; the first endogenous points' EGM slopes ['0.932063377951', '0.932063377951', '0.932063377951']
- bst-p-zero-0.005 E: MPC at the limit, closed form 0.932063377951; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.7e-12; the first endogenous points' EGM slopes ['0.932063377951', '0.932063377951', '0.932063377951']
- bst-p-zero-0.005 F: MPC at the limit, closed form 0.932063377951; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.7e-12; the first endogenous points' EGM slopes ['0.932063377951', '0.932063377951', '0.932063377951']
- bst-p-zero-0.005 G: MPC at the limit, closed form 0.932063377951; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.7e-12; the first endogenous points' EGM slopes ['0.932063377951', '0.932063377951', '0.932063377951']
- bst-p-zero-0.0005 A: MPC at the limit, closed form 0.978516553779; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 1.2e-12; the first endogenous points' EGM slopes ['0.978516553779', '0.978516553779', '0.978516553778']
- bst-p-zero-0.0005 B: MPC at the limit, closed form 0.978516553779; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 1.2e-12; the first endogenous points' EGM slopes ['0.978516553779', '0.978516553779', '0.978516553778']
- bst-p-zero-0.0005 C: MPC at the limit, closed form 0.978516553779; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 1.2e-12; the first endogenous points' EGM slopes ['0.978516553779', '0.978516553779', '0.978516553778']
- bst-p-zero-0.0005 D: MPC at the limit, closed form 0.978516553779; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 1.2e-12; the first endogenous points' EGM slopes ['0.978516553779', '0.978516553779', '0.978516553778']
- bst-p-zero-0.0005 E: MPC at the limit, closed form 0.978516553779; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 1.2e-12; the first endogenous points' EGM slopes ['0.978516553779', '0.978516553779', '0.978516553778']
- bst-p-zero-0.0005 F: MPC at the limit, closed form 0.978516553779; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 1.2e-12; the first endogenous points' EGM slopes ['0.978516553779', '0.978516553779', '0.978516553778']
- bst-p-zero-0.0005 G: MPC at the limit, closed form 0.978516553779; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 1.2e-12; the first endogenous points' EGM slopes ['0.978516553779', '0.978516553779', '0.978516553778']
- bst-p-zero-0.00005 A: MPC at the limit, closed form 0.993206337795; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.6e-13; the first endogenous points' EGM slopes ['0.993206337795', '0.993206337795', '0.993206337793']
- bst-p-zero-0.00005 B: MPC at the limit, closed form 0.993206337795; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.6e-13; the first endogenous points' EGM slopes ['0.993206337795', '0.993206337795', '0.993206337793']
- bst-p-zero-0.00005 C: MPC at the limit, closed form 0.993206337795; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.6e-13; the first endogenous points' EGM slopes ['0.993206337795', '0.993206337795', '0.993206337793']
- bst-p-zero-0.00005 D: MPC at the limit, closed form 0.993206337795; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.6e-13; the first endogenous points' EGM slopes ['0.993206337795', '0.993206337795', '0.993206337793']
- bst-p-zero-0.00005 E: MPC at the limit, closed form 0.993206337795; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.6e-13; the first endogenous points' EGM slopes ['0.993206337795', '0.993206337795', '0.993206337793']
- bst-p-zero-0.00005 F: MPC at the limit, closed form 0.993206337795; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.6e-13; the first endogenous points' EGM slopes ['0.993206337795', '0.993206337795', '0.993206337793']
- bst-p-zero-0.00005 G: MPC at the limit, closed form 0.993206337795; the rule's secants from 1e-9 to 1e-5 above it differ from it by at most 3.6e-13; the first endogenous points' EGM slopes ['0.993206337795', '0.993206337795', '0.993206337793']
- bst-restrained A: kink m = 0.974084142667, slope above 0.41785925, c − (m − a_lo) below: 0.0e+00
- bst-restrained B: kink m = 0.974084142668, slope above 0.41785925, c − (m − a_lo) below: 0.0e+00
- bst-restrained C: kink m = 0.974084142670, slope above 0.41785925, c − (m − a_lo) below: 0.0e+00
- bst-restrained D: kink m = 0.974084142670, slope above 0.41785925, c − (m − a_lo) below: 0.0e+00

## Distances from the finest setting available: the committed level-3 rules and HARK at its default settings

| member | finest | HARK level 3, max rel (at m) | dolo level 3 | HARK default, max rel (at m) | HARK default, m ≤ 20 (at m) | HARK default, kink | HARK default, max abs r | finest's max abs r |
|---|---|---|---|---|---|---|---|---|
| bst-p-zero-0.005 | G | 7.79e-04 (m = 10) | 7.76e-04 (m = 10) | 2.34e-02 (m = 50) | 5.38e-03 (m = 10) | — | 3.85e-02 | 1.45e-12 |
| bst-p-zero-0.0005 | G | 8.15e-04 (m = 10) | 8.12e-04 (m = 10) | 2.29e-02 (m = 50) | 6.52e-03 (m = 0.3) | — | 3.42e-02 | 1.37e-12 |
| bst-p-zero-0.00005 | G | 8.29e-04 (m = 10) | 8.26e-04 (m = 10) | 2.28e-02 (m = 50) | 1.13e-02 (m = 0.6) | — | 2.17e-02 | 1.35e-12 |
| bst-restrained | D | 8.35e-04 (m = 10) | 8.32e-04 (m = 10) | 2.40e-02 (m = 50) | 5.53e-03 (m = 10) | +2.01e-03 | 2.11e-03 | 2.13e-10 |

## The ergodic distribution on the dense grid: the grid's effect, the transition's nodes' effect, and level 3

Pass 1 is the bench's geometric grid (4,000 points to 60); pass 2 is uniform to the 99.9th percentile of a, 32,000 points, then geometric to 300. Relative changes; the mass at the constraint absolute.

| member | nodes a shock | a at 0.999 (dense) | mean a: pass 2 − pass 1 | median a | a at 0.999 | mean MPC | mass at the constraint | mass beyond the dense part | level 3 − dense: mean a | median a | mean MPC |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bst-p-zero-0.00005 | 31 | 0.488685 | -1.4e-06 | +3.9e-05 | +9.3e-06 | -3.3e-07 | +0.0e+00 | 9.24e-04 | -6.5e-03 | -7.7e-03 | +4.6e-03 |
| bst-p-zero-0.0005 | 31 | 0.597993 | -1.8e-06 | -3.2e-05 | +3.5e-05 | -6.0e-07 | +0.0e+00 | 9.18e-04 | -4.6e-03 | -5.0e-03 | +4.0e-03 |
| bst-p-zero-0.005 | 31 | 0.961565 | -2.5e-06 | +2.9e-05 | +9.1e-05 | -1.4e-06 | +0.0e+00 | 9.12e-04 | -2.7e-03 | -2.8e-03 | +2.8e-03 |
| bst-p-zero-0.005 | 63 | 0.966672 | -2.5e-06 | -3.6e-05 | +3.9e-06 | -1.4e-06 | +0.0e+00 | 9.12e-04 | -3.1e-03 | -2.8e-03 | +2.8e-03 |
| bst-restrained | 31 | 0.445890 | -1.3e-06 | +2.2e-05 | -4.6e-05 | -2.3e-05 | -1.8e-05 | 9.27e-04 | -8.7e-03 | -1.3e-02 | +4.6e-03 |
| bst-restrained | 63 | 0.452033 | -1.3e-06 | +3.4e-05 | +2.1e-05 | +3.0e-06 | +2.3e-06 | 9.29e-04 | -1.0e-02 | -2.4e-02 | +6.7e-03 |

The transition's nodes doubled, on the dense grid (relative change from 31 to 63 nodes a shock; the mass at the constraint absolute):

| member | mean a | median a | a at 0.9 | a at 0.999 | mean MPC | mass at the constraint |
|---|---|---|---|---|---|---|
| bst-p-zero-0.005 | +3.8e-04 | -3.3e-06 | +9.3e-04 | +5.3e-03 | +7.2e-06 | +0.0e+00 |
| bst-restrained | +1.4e-03 | +1.1e-02 | +9.4e-03 | +1.4e-02 | -2.1e-03 | -1.6e-03 |

## HARK at its default settings: the kink, and the residual by point

- bst-p-zero-0.005: cycles 90, last step 8.7e-07, kink None; the largest |r| at m = ['0.1: 3.8e-02', '0.05: 3.6e-02', '0.4: 2.4e-02', '0.2: 2.3e-02']
- bst-p-zero-0.0005: cycles 89, last step 8.2e-07, kink None; the largest |r| at m = ['0.8: 3.4e-02', '0.6: 3.1e-02', '0.5: 3.0e-02', '0.4: 3.0e-02']
- bst-p-zero-0.00005: cycles 89, last step 7.2e-07, kink None; the largest |r| at m = ['0.9: 2.2e-02', '0.85: 2.2e-02', '0.8: 2.1e-02', '0.7: 2.1e-02']
- bst-restrained: cycles 88, last step 8.0e-07, kink 0.97609509; the largest |r| at m = ['50: -2.1e-03', '1.2: -1.2e-03', '1.3: -8.8e-04', '1.05: -8.6e-04']
