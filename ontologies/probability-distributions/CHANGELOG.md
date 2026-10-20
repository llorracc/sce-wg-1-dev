# Changelog

Each entry says whether a change alters a measure (a family's definition), a chart (its coordinates or conversions), or
only labels and text.

## 0.1.0-draft.1 (unreleased)

The first draft. The design: the six kinds, the three primitive operators, the identity rule, the three settlements, the
formula syntax and the two written forms. The first rows, all new:

- the standard normal, the base of the normal-based families;
- the operators pushforward, conditioning and product with a kernel, with the affine and exponential maps as cases of the
  pushforward;
- the properties support, mean, moments, moments of the logarithm and atoms, and the constraint of mean one;
- the normal, with its charts of mean and standard deviation (canonical) and mean and variance;
- the lognormal, with its subfamily of mean one;
- the point mass, with its charts of a normal with variance zero and a lognormal with zero spread, and its subfamily at
  one;
- the truncated normal, conditioned on an interval in the variate's units, with the operator of truncation to an
  interval, and its reduction to the normal when neither bound binds;
- the truncated lognormal, conditioned on an interval in the draw's units, and its reduction to the lognormal when
  neither bound binds; its subfamily of mean one, written by the parameter files' chart: the standard deviation of the
  logarithm after truncation, and the bounds in standard deviations of the normal before truncation, with an omitted
  bound meaning three and `null` meaning none.

Every coordinate that is an expectation under the law says so, and the tests check it by quadrature.
