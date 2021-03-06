#!/usr/bin/env python
"""
A simple example from Stan. The model is written in Stan.

Probability model
    Prior: Beta
    Likelihood: Bernoulli
Variational model
    Likelihood: Mean-field Beta
"""
import edward as ed

model_code = """
    data {
      int<lower=0> N;
      int<lower=0,upper=1> y[N];
    }
    parameters {
      real<lower=0,upper=1> theta;
    }
    model {
      theta ~ beta(1.0, 1.0);
      for (n in 1:N)
        y[n] ~ bernoulli(theta);
    }
"""
ed.set_seed(42)
model = ed.StanModel(model_code=model_code)
variational = ed.MFBeta(1)
data = ed.Data(dict(N=10, y=[0, 1, 0, 0, 0, 0, 0, 0, 0, 1]))

inference = ed.MFVI(model, variational, data)
inference.run(n_iter=10000)
