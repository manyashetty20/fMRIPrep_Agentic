"""
Deterministic Vision/QA verdict.

The verdict is a pure function of logged inputs (file-existence flags, voxel
metrics when present, configured thresholds, and applied repair impacts).
Identical inputs always produce the same (summary, qualifier, reasons, checks).
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence


VerdictDict = dict[str, Any]


def _check(
    name: str,
    value: Any,
    threshold: Any,
    status: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "value": value,
        "threshold": threshold,
        "status": status,
        "reason": reason,
    }


def decide_qa_verdict(
    *,
    output_found: bool,
    report_found: bool,
    mni_found: bool,
    brain_mask_found: bool,
    retention_ratio: float | None,
    skull_strip_reduction: float | None,
    min_retention: float,
    max_retention: float,
    min_reduction: float,
    max_reduction: float,
    check_boundary_clipping: bool = False,
    edge_fraction: float | None = None,
    max_boundary_slice_fraction: float = 0.02,
    voxel_metrics_available: bool = True,
    repair_impacts: Sequence[str] | None = None,
) -> VerdictDict:
    """
    Compute PASS / WARN / FAIL and a qualifier.

    Screening-proxy voxel ratios are only scored when a brain mask exists.
    Missing mask must not be treated as 100% retention.
    """
    checks: list[dict[str, Any]] = []
    reasons: list[str] = []

    if output_found:
        checks.append(_check("output_found", True, True, "pass", "Expected preprocessed T1w output exists."))
    else:
        checks.append(_check("output_found", False, True, "fail", "Expected preprocessed T1w output is missing."))
        reasons.append("output_missing")

    if report_found:
        checks.append(_check("report_found", True, True, "pass", "Subject HTML report exists."))
    else:
        checks.append(_check("report_found", False, True, "warn", "Subject HTML report is missing."))
        reasons.append("html_report_missing")

    if mni_found:
        checks.append(_check("mni_found", True, True, "pass", "MNI-space anatomical derivative exists."))
    else:
        checks.append(_check("mni_found", False, True, "warn", "No MNI-space anatomical derivative was found."))
        reasons.append("mni_derivative_missing")

    if brain_mask_found:
        checks.append(_check("brain_mask_found", True, True, "pass", "Brain mask derivative exists."))
    else:
        checks.append(
            _check(
                "brain_mask_found",
                False,
                True,
                "warn",
                "Brain mask derivative is missing; retention/reduction screening proxies are not scored.",
            )
        )
        reasons.append("brain_mask_missing")

    if not voxel_metrics_available:
        checks.append(
            _check(
                "voxel_metrics",
                None,
                "required_for_pass_when_outputs_exist",
                "warn",
                "Voxel metrics were not computed (library error or missing arrays).",
            )
        )
        reasons.append("voxel_metrics_unavailable")

    if brain_mask_found and voxel_metrics_available and retention_ratio is not None:
        in_band = min_retention <= retention_ratio <= max_retention
        status = "pass" if in_band else "fail"
        if not in_band:
            reasons.append("retention_out_of_band")
        checks.append(
            _check(
                "brain_mask_retention_ratio",
                retention_ratio,
                {"min": min_retention, "max": max_retention},
                status,
                (
                    "Mask-vs-preprocessed retention ratio is inside the configured QA band."
                    if in_band
                    else (
                        f"Mask-vs-preprocessed retention ratio ({retention_ratio:.1%}) "
                        f"falls outside configured band [{min_retention:.1%}, {max_retention:.1%}]."
                    )
                ),
            )
        )
        checks.append(
            _check(
                "retention_reduction_proxy",
                True,
                None,
                "pass",
                "Retention/reduction is a screening proxy only, not independent quality evidence.",
            )
        )

    if brain_mask_found and voxel_metrics_available and skull_strip_reduction is not None:
        in_band = min_reduction <= skull_strip_reduction <= max_reduction
        status = "pass" if in_band else "fail"
        if not in_band:
            reasons.append("reduction_out_of_band")
        checks.append(
            _check(
                "skull_strip_reduction",
                skull_strip_reduction,
                {"min": min_reduction, "max": max_reduction},
                status,
                (
                    "Mask-vs-preprocessed voxel reduction is inside the configured QA band."
                    if in_band
                    else (
                        f"Mask-vs-preprocessed voxel reduction ({skull_strip_reduction:.1%}) "
                        f"falls outside configured band [{min_reduction:.1%}, {max_reduction:.1%}]."
                    )
                ),
            )
        )

    if check_boundary_clipping and brain_mask_found and edge_fraction is not None:
        clipped = edge_fraction > max_boundary_slice_fraction
        if clipped:
            reasons.append("boundary_clipping")
        checks.append(
            _check(
                "boundary_clipping",
                edge_fraction,
                {"max": max_boundary_slice_fraction},
                "fail" if clipped else "pass",
                (
                    f"Brain mask touches FOV boundary slices "
                    f"({edge_fraction:.2%} > {max_boundary_slice_fraction:.2%})."
                    if clipped
                    else f"Brain mask is fully contained within FOV boundaries ({edge_fraction:.2%} edge voxels)."
                ),
            )
        )

    fail_count = sum(1 for c in checks if c["status"] == "fail")
    warn_count = sum(1 for c in checks if c["status"] == "warn")
    if fail_count:
        summary = "FAIL"
    elif warn_count:
        summary = "WARN"
    else:
        summary = "PASS"

    impacts = [str(x) for x in (repair_impacts or []) if str(x).strip()]
    if impacts:
        qualifier = "DEGRADED: " + "; ".join(impacts)
        reasons.append("repair_degraded_outputs")
    else:
        qualifier = "CLEAN"

    display = f"{summary} ({qualifier})" if qualifier != "CLEAN" else summary

    return {
        "summary": summary,
        "qualifier": qualifier,
        "display": display,
        "status": "completed",
        "checks": checks,
        "reasons": reasons,
        "qa_warn_count": warn_count,
        "qa_fail_count": fail_count,
    }


def verdict_from_metrics(metrics: Mapping[str, Any], repair_impacts: Iterable[str] | None = None) -> VerdictDict:
    """Recompute a verdict from a persisted qa_metrics / qa_completed payload."""
    thresholds = metrics.get("qa_thresholds") or metrics.get("thresholds_used") or {}
    return decide_qa_verdict(
        output_found=bool(metrics.get("output_found")),
        report_found=bool(metrics.get("report_found")),
        mni_found=bool(metrics.get("mni_found")),
        brain_mask_found=bool(metrics.get("brain_mask_found")),
        retention_ratio=_maybe_float(metrics.get("brain_mask_retention_ratio")),
        skull_strip_reduction=_maybe_float(metrics.get("skull_strip_reduction")),
        min_retention=float(thresholds.get("min_brain_mask_retention_ratio", 0.05)),
        max_retention=float(thresholds.get("max_brain_mask_retention_ratio", 0.25)),
        min_reduction=float(thresholds.get("min_skull_strip_reduction", 0.75)),
        max_reduction=float(thresholds.get("max_skull_strip_reduction", 0.95)),
        check_boundary_clipping=metrics.get("boundary_edge_fraction") is not None,
        edge_fraction=_maybe_float(metrics.get("boundary_edge_fraction")),
        voxel_metrics_available=metrics.get("raw_nonzero_voxels") is not None,
        repair_impacts=list(repair_impacts or []),
    )


def _maybe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
