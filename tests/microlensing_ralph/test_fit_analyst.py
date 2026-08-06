import json
import os
from pathlib import Path

import numpy as np
import pytest

from microlensing_ralph.analyst.fit_analyst import FitAnalyst
from microlensing_ralph.toolbox import input_tools, logs


ralph_output = os.path.join("tests", "microlensing_ralph", "data", "output")
ralph_input = os.path.join("tests", "microlensing_ralph", "data", "input")
ralph_light_curves = os.path.join(ralph_input, "light_curves")

scenario_gaia = {
    "analyst_path": os.path.join(ralph_output, "fit_analyst"),
    "event_name": "GDR3_ULENS_025",
    "ra": 260.8781,
    "dec": -27.3788,
    "fit_analyst": {
        "ongoing_magnification_threshold": 1.10,
        "ongoing_amplitude_threshold": 1.0,
        "return_all_models": True,
        "model_fit_configuration": {
            "1S1L_no_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "DE",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "1S1L_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "1S1L_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "fitting_method_args": {
                    "loss_function" : "soft_l1",
                },
                "boundaries": {
                    "u0": [0.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
            "1S1L_no_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
        }
    },
    "light_curves": [
        {
            "survey": "Gaia",
            "band": "G",
            "ephemeris": os.path.join(ralph_input, "ephemeris","gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_Gaia_G.dat"),
        },
        {
            "survey": "Gaia",
            "band": "BP",
            "ephemeris": os.path.join(ralph_input, "ephemeris","gaia_jpl_horizons_results.txt"),
            "path":  os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_Gaia_BP.dat"),
        },
        {
            "survey": "Gaia",
            "band": "RP",
            "ephemeris": os.path.join(ralph_input, "ephemeris","gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_Gaia_RP.dat"),
        },
        {
            "survey": "OGLE",
            "band": "I",
            "path": os.path.join(ralph_light_curves, "GaiaDR3_ULENS_025_OGLE.dat"),
        },
    ],
    "fit_result": os.path.join(ralph_input, "test_results", "gdr3_ulens_025_fit_results.json"),
}

scenario_gsa = {
    "event_name": "Gaia24amo",
    "ra": 249.14892083,
    "dec": -53.74991944,
    "analyst_path": os.path.join(ralph_output, "fit_analyst"),
    "lc_analyst": {
    },
    "fit_analyst": {
        "ongoing_magnification_threshold": 1.10,
        "ongoing_amplitude_threshold": 1.0,
        "return_all_models": True,
        "model_fit_configuration": {
            "1S1L_no_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "DE",
                "fitting_method_args": {
                    "DE_population" : 10,
                    "loss_function" : "soft_l1",
                },
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "1S1L_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                }
            },
            "1S1L_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "DE",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
            "1S1L_no_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "DE",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
        }
    },
    "light_curves": [
        {
            "survey": "Gaia",
            "band": "G",
            "ephemeris": os.path.join(ralph_input, "ephemeris","gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_light_curves, "Gaia24amo_Gaia_G.dat"),
        },
        {
            "survey": "LCO",
            "band": "g",
            "path": os.path.join(ralph_light_curves, "cleaned_Gaia24amo_LCO_g.dat"),
        },
        {
            "survey": "LCO",
            "band": "r",
            "path": os.path.join(ralph_light_curves, "cleaned_Gaia24amo_LCO_r.dat"),
        },
        {
            "survey": "LCO",
            "band": "i",
            "path": os.path.join(ralph_light_curves, "cleaned_Gaia24amo_LCO_i.dat"),
        },
    ],
    "fit_result": os.path.join(ralph_input, "test_results", "gaia24amo_fit_results.json"),
}

scenario_roman = {
    "event_name": "ulwdc1_018",
    "ra": 267.871,
    "dec": -29.6712,
    "analyst_path": os.path.join(ralph_output, "fit_analyst"),
    "lc_analyst": {"acceptable_mag_range":
                       {"upper_limit": -5, "lower_limit": 30},
                   "max_acceptable_err": 1.0,
                   "hampel": {
                       "window": "1D",
                       "n_sigma": 3.0,
                       "use_weighted": False,
                   },
                   "save_outlier_results": True,
                   "to_MJD": True,
                   },
    "fit_analyst": {
        "ongoing_magnification_threshold": 1.10,
        "ongoing_amplitude_threshold": 1.0,
        "return_all_models": True,
        "anomaly_finder": {
            "method": "hampel",
            "fitting_package": "pyLIMA",
            "min_seq_length": 5,
            "save_results": True,
            "to_MJD": True,
            "af_setup": {
                "window": "3D",
                "n_sigma": 2.0,
                "use_weighted": True,
            },
        },
        "model_fit_configuration": {
            "1S1L_no_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "1S1L_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "1S1L_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
            "1S1L_no_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
            "1S2L_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
        },
    },
    "light_curves": [
        {
            "survey": "Roman",
            "band": "W149",
            "path": os.path.join(ralph_light_curves, "ulwdc1_018_W149.txt"),
        },
    ],
}

class FitAnalystTest:
    """
    Class with tests
    """

    def __init__(self, scenario):
        self.scenario = scenario

    def setup(self):
        config = {
            "event_name": self.scenario.get("event_name"),
            "ra": self.scenario.get("ra"),
            "dec": self.scenario.get("dec"),
        }

        fit_params = self.scenario.get("fit_analyst")

        config["fit_analyst"] = {
            "ongoing_magnification_threshold": fit_params.get("ongoing_magnification_threshold"),
            "ongoing_amplitude_threshold": fit_params.get("ongoing_amplitude_threshold"),
            "return_all_models": fit_params.get("return_all_models", True),
            "anomaly_finder": fit_params.get("anomaly_finder", None),
        }

        model_params = fit_params.get("model_fit_configuration")
        params = {}
        for model in model_params:
            params[model] = model_params.get(model)
        config["fit_analyst"]["model_fit_configuration"] = params

        config["light_curves"] = self.scenario.get("light_curves")

        path_outputs = self.scenario.get("analyst_path")

        light_curves = []
        for entry in config["light_curves"]:
            survey = entry["survey"]
            band = entry["band"]
            data = input_tools.load_light_curve_from_path(entry["path"])

            ephemeris = None
            if entry == "ephemeris":
                ephemeris = input_tools.load_ephemeris_from_path(
                    entry["ephemeris"],
                    usecols=(0, 1, 2, 3),
                )

            light_curves.append(
                {
                    "light_curve": data,
                    "ephemeris": ephemeris,
                    "survey": survey,
                    "band": band,
                }
            )

        return path_outputs, config, light_curves

    def test_parse_config(self):
        """
        Test if parsing configuration file works.
        """

        path_outputs, config, light_curves = self.setup()
        fit_params = self.scenario.get("fit_analyst")

        log = logs.start_log(path_outputs, "debug", event_name=config["event_name"], stream=True)
        analyst = FitAnalyst(config["event_name"], path_outputs, light_curves, log, config_dict=config)
        on_mag_t_config = analyst.config["ongoing_magnification_threshold"]
        on_ampl_t_config = analyst.config["ongoing_amplitude_threshold"]
        model_fit_config = analyst.config["model_fit_configuration"]
        af_config = analyst.config["anomaly_finder"]

        logs.close_log(log)

        assert on_mag_t_config == fit_params.get("ongoing_magnification_threshold")
        assert on_ampl_t_config == fit_params.get("ongoing_amplitude_threshold")

        model_params = fit_params.get("anomaly_finder")
        print("======================")
        print(model_params)
        print(analyst.config)
        for entry in af_config:
            param = af_config[entry]
            if type(param) == dict:
                for key in param:
                    assert model_params[entry][key] == param.get(key)
            else:
                assert param == model_params[entry]

        model_params = fit_params.get("model_fit_configuration")
        for model in model_fit_config:
            params = model_fit_config[model]
            for key in params:
                assert model_params[model][key] == params.get(key)

    def test_check_ongoing(self):
        """
        Check if testing for an ongoing event works.
        """

        path_outputs, config, light_curves = self.setup()

        log = logs.start_log(path_outputs, "debug", event_name=config["event_name"], stream=False)
        analyst = FitAnalyst(config["event_name"], path_outputs, light_curves, log, config_dict=config)
        status, t0 = analyst.perform_ongoing_check()
        logs.close_log(log)

        if config['event_name'] == "Gaia24amo":
            assert status
        elif config['event_name'] == "GDR3_ULENS_025":
            assert not status

    def test_fit(self):
        """
        Test if fitting works.
        """

        path_outputs, config, light_curves = self.setup()

        log = logs.start_log(path_outputs, "debug", event_name=config["event_name"], stream=False)
        analyst = FitAnalyst(config["event_name"], path_outputs, light_curves, log, config_dict=config)
        result = analyst.perform_fit()

        with open(self.scenario.get("fit_result"), "r") as file:
            expected_fit_result = json.load(file)

        for model in expected_fit_result:
            if model != "1S1L_no_blend_no_piE":
                model_result = result[model]
                expected_result = expected_fit_result[model]
                for key in expected_result:
                    expected = float(expected_result[key])
                    received = float(model_result[key])
                    if not np.isnan(expected):
                        assert pytest.approx(expected, 2) == pytest.approx(received, 2)

        logs.close_log(log)

    def test_return_best_only(self):
        """
        Test if returning only best-fitting model works.
        """

        path_outputs, config, light_curves = self.setup()

        log = logs.start_log(path_outputs, "debug", event_name=config["event_name"], stream=False)
        analyst = FitAnalyst(config["event_name"], path_outputs, light_curves, log, config_dict=config)
        result = analyst.perform_fit()

        n_models = 0
        best_model = None
        for model in result:
            n_models += 1
            best_model = model

        assert n_models == 1
        assert best_model == self.scenario.get("best_model_key")

        logs.close_log(log)

    def test_1s2l_fit(self):
        """
        Test if single source-binary lens fitting works.
        """

        path_outputs, config, light_curves = self.setup()

        log = logs.start_log(path_outputs, "debug", event_name=config["event_name"], stream=False)
        analyst = FitAnalyst(config["event_name"], path_outputs, light_curves, log, config_dict=config)
        result = analyst.perform_fit()

        # with open(self.scenario.get("fit_result"), "r") as file:
        #     expected_fit_result = json.load(file)

        # for model in expected_fit_result:
        #     if model != "1S1L_no_blend_no_piE":
        #         model_result = result[model]
        #         expected_result = expected_fit_result[model]
        #         for key in expected_result:
        #             expected = float(expected_result[key])
        #             received = float(model_result[key])
        #             if not np.isnan(expected):
        #                 assert pytest.approx(expected, 2) == pytest.approx(received, 2)

        logs.close_log(log)


def test_run():
    """
    Run all tests.
    """

    test = FitAnalystTest(scenario_roman)
    test.test_parse_config()
    test.test_1s2l_fit()

    # for case in [scenario_gaia, scenario_gsa]:
    #     test = FitAnalystTest(case)
    #     test.test_parse_config()
    #     test.test_check_ongoing()
    #     if case.get("event_name") == "GDR3_ULENS_025":
    #         test.test_fit()
    #
    # scenario_best_only = scenario_gaia.copy()
    # scenario_best_only["fit_analyst"]["return_all_models"] = False
    # scenario_best_only["fit_result"] = None
    # scenario_best_only["best_model_key"] = "1S1L_blend_piE_n"
    #
    # test = FitAnalystTest(scenario_best_only)
    # test.test_return_best_only()
    #
    # for case in [scenario_gaia, scenario_gsa, scenario_best_only]:
    #     analyst_path = case.get("analyst_path")
    #     event_name = case.get("event_name")
    #
    #     fpath = os.path.join(analyst_path, "fit_results.json")
    #     output = Path(fpath)
    #     if output.exists():
    #         os.remove(output)
    #
    #     fpath = os.path.join(analyst_path, "fit_stats.txt")
    #     output = Path(fpath)
    #     if output.exists():
    #         os.remove(output)
    #
    #     fpath = os.path.join(analyst_path, event_name + "_analyst.log")
    #     output = Path(fpath)
    #     if output.exists():
    #         os.remove(output)
    #
    #     files = [
    #         "1S1L_no_blend_no_piE.html",
    #         "1S1L_blend_no_piE.html",
    #         "1S1L_blend_piE.html",
    #         "1S1L_blend_piE_p.html",
    #         "1S1L_blend_piE_n.html",
    #     ]
    #     for element in files:
    #         fpath = os.path.join(analyst_path, element)
    #         output = Path(fpath)
    #         if output.exists():
    #             os.remove(output)
