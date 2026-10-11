#!/usr/bin/env python3
"""The Deterministic Fog - reference implementation. Instance in output.json.

The "noise" of this LWE instance is not random: it is produced by a public
linear congruential generator

        x_{i+1} = (mult * x_i + inc) mod 2^mod_bits

seeded by a secret 48-bit state.  The device also logs a short *calibration*
trace of its noise source (the high bits of the first few states), published
alongside the instance.  Everything the generator does is exact integer
arithmetic -- there is no floating point and nothing to reproduce bit-for-bit
by luck.
"""

import json
from pathlib import Path

SEED_BITS = 48


def _lcg(cfg):
    s = cfg["sampler"]
    return s["mult"], s["inc"], 1 << s["mod_bits"], s["hide"], s["calib"]


def calibration_trace(seed, cfg):
    """High bits (>> hide) of states x_0 .. x_{calib-1}."""
    mult, inc, M, hide, calib = _lcg(cfg)
    x = seed % M
    out = [x >> hide]
    for _ in range(calib - 1):
        x = (mult * x + inc) % M
        out.append(x >> hide)
    return out


class StreamSampler:
    """Continues the LCG from state x_{calib}; emits centered noise."""

    def __init__(self, seed, cfg):
        self.mult, self.inc, self.M, _, calib = _lcg(cfg)
        self.bound = int(cfg["params"]["bound"])
        x = seed % self.M
        for _ in range(calib):                 # advance x_0 -> x_{calib}
            x = (self.mult * x + self.inc) % self.M
        self.x = x

    def sample(self):
        v = self.x % (2 * self.bound + 1) - self.bound
        self.x = (self.mult * self.x + self.inc) % self.M
        return v


def dot(a, b, q):
    return sum(x * y for x, y in zip(a, b)) % q


def make_public_samples(A, secret, sampler, q):
    samples = []
    for row in A:
        noise = sampler.sample()
        samples.append((dot(row, secret, q) + noise) % q)
    return samples


def seal(message, rows, secret, sampler, q):
    bits = [
        (byte >> shift) & 1
        for byte in message
        for shift in range(7, -1, -1)
    ]
    if len(rows) != len(bits):
        raise ValueError("row count does not match message length")

    ciphertext = []
    for bit, row in zip(bits, rows):
        noise = sampler.sample()
        phase = dot(row, secret, q)
        encoded = bit * (q // 2)
        ciphertext.append((phase + noise + encoded) % q)
    return ciphertext


def build_session(message, A, rows, secret, config, seed):
    q = config["params"]["q"]
    sampler = StreamSampler(seed, config)

    b = make_public_samples(A, secret, sampler, q)
    ciphertext = seal(message, rows, secret, sampler, q)

    return {
        "params": config["params"],
        "sampler": config["sampler"],
        "calibration": calibration_trace(seed, config),
        "A": A,
        "b": b,
        "R": rows,
        "ciphertext": ciphertext,
    }


def load_instance(filename="output.json"):
    path = Path(filename)
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def inspect_instance(data):
    params = data["params"]
    A = data["A"]
    R = data["R"]

    if len(A) != params["m"]:
        raise ValueError("invalid row count")
    if any(len(row) != params["n"] for row in A):
        raise ValueError("invalid column count")
    if len(data["b"]) != params["m"]:
        raise ValueError("invalid sample count")
    if len(R) != len(data["ciphertext"]):
        raise ValueError("invalid encryption row count")
    if any(len(row) != params["n"] for row in R):
        raise ValueError("invalid encryption column count")

    return {
        "n": params["n"],
        "m": params["m"],
        "q": params["q"],
        "bound": params["bound"],
        "calibration": len(data.get("calibration", [])),
        "ciphertext_size": len(data["ciphertext"]),
    }


if __name__ == "__main__":
    instance = load_instance()
    info = inspect_instance(instance)
    print("The Deterministic Fog")
    print(f"dimension:   {info['n']}")
    print(f"samples:     {info['m']}")
    print(f"modulus:     {info['q']}")
    print(f"bound:       {info['bound']}")
    print(f"calibration: {info['calibration']}")
    print(f"ciphertext:  {info['ciphertext_size']}")
