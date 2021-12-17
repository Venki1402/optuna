from typing import cast

import pytest

from optuna.distributions import FloatDistribution
from optuna.study import create_study
from optuna.trial import create_trial
from optuna.visualization import is_available
from optuna.visualization._utils import _check_plot_args
from optuna.visualization._utils import _is_log_scale


def test_is_log_scale() -> None:

    study = create_study()
    study.add_trial(
        create_trial(
            value=0.0,
            params={"param_linear": 1.0},
            distributions={"param_linear": FloatDistribution(0.0, 3.0)},
        )
    )
    study.add_trial(
        create_trial(
            value=2.0,
            params={"param_linear": 2.0, "param_log": 1e-3},
            distributions={
                "param_linear": FloatDistribution(0.0, 3.0),
                "param_log": FloatDistribution(1e-5, 1.0, log=True),
            },
        )
    )
    assert _is_log_scale(study.trials, "param_log")
    assert not _is_log_scale(study.trials, "param_linear")


def _is_plotly_available() -> bool:

    try:
        import plotly  # NOQA

        available = True
    except Exception:
        available = False
    return available


def test_visualization_is_available() -> None:

    assert is_available() == _is_plotly_available()


def test_check_plot_args() -> None:

    study = create_study(directions=["minimize", "minimize"])
    with pytest.raises(ValueError):
        _check_plot_args(study, None, "Objective Value")

    with pytest.warns(UserWarning):
        _check_plot_args(study, lambda t: cast(float, t.value), "Objective Value")
