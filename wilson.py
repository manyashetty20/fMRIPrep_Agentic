"""Wilson score interval for binomial proportions."""

from __future__ import annotations

import math
from typing import NamedTuple


class WilsonCI(NamedTuple):
    n: int
    k: int
    rate: float | None
    low: float | None
    high: float | None

    def as_dict(self) -> dict:
        return {
            "n": self.n,
            "k": self.k,
            "rate": self.rate,
            "wilson_low": self.low,
            "wilson_high": self.high,
        }


def wilson_interval(k: int, n: int, z: float = 1.96) -> WilsonCI:
    """
    Return a Wilson 95% CI (default z=1.96) for k successes in n trials.

    When n==0, rate and bounds are None. Bounds are clipped to [0, 1].
    """
    if n <= 0:
        return WilsonCI(n=int(n), k=int(k), rate=None, low=None, high=None)
    k = int(k)
    n = int(n)
    p = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    margin = (z * math.sqrt((p * (1.0 - p) + z2 / (4.0 * n)) / n)) / denom
    low = max(0.0, center - margin)
    high = min(1.0, center + margin)
    return WilsonCI(n=n, k=k, rate=p, low=low, high=high)


def format_rate_ci(ci: WilsonCI, digits: int = 3) -> str:
    if ci.rate is None:
        return f"n={ci.n} (undefined)"
    return (
        f"{ci.rate:.{digits}f} [{ci.low:.{digits}f}, {ci.high:.{digits}f}] "
        f"(k={ci.k}/n={ci.n})"
    )
