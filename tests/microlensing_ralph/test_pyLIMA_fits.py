import os
from pathlib import Path

import pytest

from microlensing_ralph.fitting_support.pylima.fit_pylima import FitPylima
from microlensing_ralph.toolbox import input_tools, logs

ralph_output = os.path.join("tests", "microlensing_ralph", "data", "output")
ralph_input = os.path.join("tests", "microlensing_ralph", "data", "input")
ralph_light_curves = os.path.join(ralph_input, "light_curves")

scenario = {
    "event_name": "GDR3_ULENS_025",
    "ra": 260.8781,
    "dec": -27.3788,
    "light_curves": [
        {
            "survey": "Gaia",
            "band": "G",
            "ephemeris": os.path.join(ralph_input, "ephemeris", "gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_Gaia_G.dat"),
        },
        {
            "survey": "Gaia",
            "band": "BP",
            "ephemeris": os.path.join(ralph_input, "ephemeris", "gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_Gaia_BP.dat"),
        },
        {
            "survey": "Gaia",
            "band": "RP",
            "ephemeris": os.path.join(ralph_input, "ephemeris", "gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_Gaia_RP.dat"),
        },
        {
            "survey": "OGLE",
            "band": "I",
            "path": os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_OGLE.dat"),
        },
    ],
}

scenario_roman = {
    "event_name": "ulwdc1_040",
    "ra": 267.715,
    "dec": -28.3235,
    "analyst_path": os.path.join(ralph_output, "fit_analyst"),
    "light_curves": [
        {
            "survey": "Roman",
            "band": "W149",
            "path": os.path.join(ralph_light_curves, "ulwdc1_040_W149.txt"),
        },
    ],
}

model_roman = {
    "best_results": {
        "1S1L_no_blend_no_piE": {
            "t0_par": 0.0,
            "t0": 2459805.628,
            "t0_error": 367.374,
            "u0": 1.16008,
            "u0_error": 0.35924,
            "tE": 22.066,
            "tE_error": 21.221,
            "fsource_Roman_W149": 433.34169,
            "fsource_Roman_W149_error": 1.13359,
            "fsource_Roman_W149_mag": 20.808,
            "fsource_Roman_W149_mag_error": 0.003,
            "fsource_Roman_Z087": 112.84108,
            "fsource_Roman_Z087_error": 0.29438,
            "fsource_Roman_Z087_mag": 22.269,
            "fsource_Roman_Z087_mag_error": 0.005,
            "chi2": 31163.112,
            "source_magnitude": 20.808,
            "source_mag_error": 0.003,
            "baseline_magnitude": 20.808,
            "baseline_mag_error": 0.003,
            "red_chi2": 0.826,
            "sw_test": 0.995,
            "sw_test_result": 0,
            "ad_test": 30.578,
            "ad_test_result": 0,
            "ks_test": 0.02,
            "ks_test_result": 0,
            "aic_test": 31173.112,
            "bic_test": 31215.801
        },
    },
}

class TestPylima:
    """
    Testing pyLIMA fitting implementation.
    """

    def __init__(self, scenario, model_params=None):
        self.ra = scenario["ra"]
        self.dec = scenario["dec"]
        light_curves = []
        for lc in scenario["light_curves"]:
            lc_dict = {}
            lc_dict["survey"] = lc["survey"]
            lc_dict["band"] = lc["band"]

            if "ephemeris" in lc:
                lc_dict["ephemeris"] = input_tools.load_ephemeris_from_path(
                    lc["ephemeris"],
                    # skip_header = 94,
                    # skip_footer = 4159,
                    usecols=(0, 1, 2, 3),
                )

            data = input_tools.load_light_curve_from_path(lc["path"])

            lc_dict["light_curve"] = data

            light_curves.append(lc_dict)

        self.light_curves = light_curves
        self.event_name = scenario["event_name"]
        self.model_params = model_params

    def test_create_event(self):
        """
        Test setting up event instance with pyLIMA.
        """
        log = logs.start_log(os.path.join(ralph_output, "pyLIMA" ),
                             "debug",
                             event_name="test_pylima_fits_event")

        event_name = self.event_name

        log.info("Creating FitPylima instance.")
        fit_pspl = FitPylima(log)
        log.info("Setting up event.")

        event = fit_pspl.setup_event(event_name, self.ra, self.dec, self.light_curves)

        log.info("Event set up.")
        logs.close_log(log)

        assert event.name == event_name
        assert event.ra == self.ra
        assert event.dec == self.dec

    def test_fit_pspl(self):
        """
        Test fitting with pyLIMA for PSPL without secondary effects.
        """
        log = logs.start_log(os.path.join(ralph_output, "pyLIMA" ),
                             "debug",
                             event_name="test_pylima_fits_pspl")

        fit_pspl = FitPylima(log)
        log.info("Fitting event.")
        starting_params = {
            "ra": self.ra,
            "dec": self.dec,
            "t0": 2457492.0,
            "u0": 0.1,
            "tE": 40.0,
        }

        params = fit_pspl.fit_pspl("PSPL_no_piE", self.light_curves, starting_params, False, True)

        log.info("Fitting finished.")
        log.debug(
            f"Fitted parameters: t_0 = {params['t0']:.2f} +- {params['t0_error']:.2f},  \n"
            f"u_0 = {params['u0']:.3f} +- {params['u0_error']:.3f},  \n"
            f"t_E = {params['tE']:.2f} +- {params['tE_error']:.2f}\n"
        )

        assert pytest.approx(params["t0"], abs=0.01) == 2457491.75
        assert pytest.approx(params["u0"], abs=0.01) == 0.194
        assert pytest.approx(params["tE"], abs=0.01) == 120.81
        logs.close_log(log)

    def test_fit_parallax(self):
        """
        Testing pylima parallax model fit implementation.
        """
        log = logs.start_log(os.path.join(ralph_output, "pyLIMA"),
                             "debug",
                             event_name="test_pyLIMA_fits_pie")

        fit_pspl = FitPylima(log)
        log.info("Fitting event.")
        starting_params = {
            "ra": self.ra,
            "dec": self.dec,
            "t0": 2457492.0,
            "u0": 0.1,
            "tE": 40.0,
            "piEN": 0.0,
            "piEE": 0.0,
        }

        params = fit_pspl.fit_pspl("PSPL_piE", self.light_curves, starting_params, True, True)

        log.info("Fitting finished.")
        log.debug(
            f"Fitted parameters: t_0 = {params['t0']:.2f} +- {params['t0_error']:.2f}, \n"
            f"u_0 = {params['u0']:.3f} +- {params['u0_error']:.3f}, \n"
            f"t_E = {params['tE']:.2f} +- {params['tE_error']:.2f}, \n"
            f"piEN = {params['piEN']:.3f} +- {params['piEN_error']:.3f}, \n"
            f"piEE = {params['piEE']:.3f} +- {params['piEE_error']:.3f}\n"
        )

        assert pytest.approx(params["t0"], abs=0.01) == 2457487.76
        assert pytest.approx(params["u0"], abs=0.01) == 0.119
        assert pytest.approx(params["tE"], abs=0.01) == 176.20
        assert pytest.approx(params["piEN"], abs=0.01) == 0.582
        assert pytest.approx(params["piEE"], abs=0.01) == 0.305

        logs.close_log(log)

    def test_redo_stats_and_plots(self):
        """
                Testing pylima parallax model fit implementation.
                """
        log = logs.start_log(os.path.join(ralph_output, "pyLIMA"),
                             "debug",
                             event_name=self.event_name
                             )

        fit_model = FitPylima(log)

        if self.model_params is not None:
            for model_label in self.model_params["best_results"]:
                parameters = self.model_params["best_results"].get(model_label)
                updated_params = fit_model.redo_stats_and_plots(model_label,
                                     self.ra, self.dec,
                                     parameters,
                                     self.light_curves
                                     )
                print("=====================")
                print(updated_params)

        logs.close_log(log)


def test_run():
    """
    Run pylima fitting tests.
    """

    # test = TestPylima(scenario)
    # test.test_create_event()
    # test.test_fit_pspl()
    # test.test_fit_parallax()
    test_roman = TestPylima(scenario_roman, model_params=model_roman)
    test_roman.test_redo_stats_and_plots()

    # analyst_path = os.path.join(ralph_output, "pyLIMA" )
    # event_names = ["test_pyLIMA_fits_pie", "test_pylima_fits_event", "test_pylima_fits_pspl"]
    #
    # for event in event_names:
    #     fpath = os.path.join(analyst_path, event + "_analyst.log")
    #     output = Path(fpath)
    #     if output.exists():
    #         os.remove(output)
