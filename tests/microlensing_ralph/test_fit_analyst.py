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
    "event_name": "ulwdc1_040",
    "ra": 267.715,
    "dec": -28.3235,
    "analyst_path": os.path.join(ralph_output, "fit_analyst"),
    "lc_analyst": {"acceptable_mag_range":
                       {"upper_limit": -5, "lower_limit": 30},
                   "max_acceptable_err": 1.0,
                   "hampel": {
                       "window": "4D",
                       "n_sigma": 2.0,
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
                "window": "7D",
                "n_sigma": 3.0,
                "use_weighted": True,
            },
        },
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
                    "loss_function" : "chi2",
                },
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
            "1S2L_no_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "fitting_method_args": {
                    "loss_function" : "chi2",
                },
                "boundaries": {
                    "u0": [0.0, 2.5],
                }
            },
            "1S2L_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "fitting_method_args": {
                    "loss_function" : "chi2",
                },
                "boundaries": {
                    "u0": [0.0, 2.5],
                }
            },
            "1S2L_no_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "fitting_method_args": {
                    "loss_function": "chi2",
                },
            },
            "1S2L_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "fitting_method_args": {
                    "loss_function": "chi2",
                },
            },
        },
    },
    "light_curves": [
        {
            "survey": "Roman",
            "band": "W149",
            "path": os.path.join(ralph_light_curves, "ulwdc1_040_W149.txt"),
        },
    ],
}

answers_roman = {
    "best_model": "1S1L_blend_piE_p",
    "best_results": {
    "1S1L_no_blend_no_piE": {
            "t0_par": 0.0,
            "t0": 2459806.339,
            "t0_error": 250.688,
            "u0": 1.16217,
            "u0_error": 0.36303,
            "tE": 21.951,
            "tE_error": 18.488,
            "fsource_Roman_W149": 433.34238,
            "fsource_Roman_W149_error": 1.15646,
            "fsource_Roman_W149_mag": 20.808,
            "fsource_Roman_W149_mag_error": 0.003,
            "chi2": 29903.145,
            "source_magnitude": 20.808,
            "source_mag_error": 0.003,
            "baseline_magnitude": 20.808,
            "baseline_mag_error": 0.003,
            "red_chi2": 0.81,
            "sw_test": 0.995,
            "ad_test": 30.585,
            "ks_test": 0.02,
            "aic_test": 29911.145,
            "bic_test": 29945.212
        },
        "1S1L_blend_piE_p": {
            "t0_par": 2459807,
            "t0": 2459807.777,
            "t0_error": 0.298,
            "u0": 1.28867,
            "u0_error": 0.29066,
            "tE": 20.946,
            "tE_error": 2.862,
            "piEN": 1.28348,
            "piEN_error": 0.89741,
            "piEE": -0.49666,
            "piEE_error": 0.4909,
            "fsource_Roman_W149": 546.62527,
            "fsource_Roman_W149_error": 293.64902,
            "fsource_Roman_W149_mag": 20.556,
            "fsource_Roman_W149_mag_error": 0.583,
            "ftotal_Roman_W149": 433.35323,
            "ftotal_Roman_W149_error": 0.02018,
            "ftotal_Roman_W149_mag": 20.808,
            "ftotal_Roman_W149_mag_error": 0.0,
            "chi2": 29898.308,
            "fblend_Roman_W149": -113.27204,
            "fblend_Roman_W149_error": 293.6490206933999,
            "fblend_Roman_W149_mag": np.nan,
            "fblend_Roman_W149_mag_error": 2.815,
            "source_magnitude": 20.556,
            "source_mag_error": 0.583,
            "blend_magnitude": np.nan,
            "blend_mag_error": 2.815,
            "baseline_magnitude": 20.808,
            "baseline_mag_error": 0.0,
            "red_chi2": 0.81,
            "sw_test": 0.995,
            "ad_test": 30.726,
            "ks_test": 0.02,
            "aic_test": 29912.308,
            "bic_test": 29971.925
        },
        "1S1L_blend_no_piE": {
            "t0_par": 0.0,
            "t0": 2459807.67,
            "t0_error": 0.235,
            "u0": 1.01855,
            "u0_error": 0.08646,
            "tE": 23.095,
            "tE_error": 1.151,
            "fsource_Roman_W149": 322.68081,
            "fsource_Roman_W149_error": 58.48191,
            "fsource_Roman_W149_mag": 21.128,
            "fsource_Roman_W149_mag_error": 0.197,
            "ftotal_Roman_W149": 433.36453,
            "ftotal_Roman_W149_error": 0.02249,
            "ftotal_Roman_W149_mag": 20.808,
            "ftotal_Roman_W149_mag_error": 0.0,
            "chi2": 29899.842,
            "fblend_Roman_W149": 110.68372,
            "fblend_Roman_W149_error": 58.481914324414866,
            "fblend_Roman_W149_mag": 22.29,
            "fblend_Roman_W149_mag_error": 0.574,
            "source_magnitude": 21.128,
            "source_mag_error": 0.197,
            "blend_magnitude": 22.29,
            "blend_mag_error": 0.574,
            "baseline_magnitude": 20.808,
            "baseline_mag_error": 0.0,
            "red_chi2": 0.81,
            "sw_test": 0.995,
            "ad_test": 30.638,
            "ks_test": 0.02,
            "aic_test": 29909.842,
            "bic_test": 29952.426
        },
    },
    "outlier_results_path": os.path.join(ralph_input, "test_results", "ulwdc1_040_outlier_results.npz"),
    "outlier_seqs": {
        "Roman_W149": [
            {
                "t_start": 2458348.288254,
                "t_end": 2458348.309307,
                "sequence_length": 2
            },
            {
                "t_start": 2458353.55577,
                "t_end": 2458353.576823,
                "sequence_length": 2
            },
            {
                "t_start": 2458354.111995,
                "t_end": 2458354.143575,
                "sequence_length": 3
            },
            {
                "t_start": 2458359.839326,
                "t_end": 2458359.860379,
                "sequence_length": 2
            },
            {
                "t_start": 2458362.011596,
                "t_end": 2458362.032649,
                "sequence_length": 2
            },
            {
                "t_start": 2458366.143935,
                "t_end": 2458366.164987,
                "sequence_length": 2
            },
            {
                "t_start": 2458369.837512,
                "t_end": 2458369.858564,
                "sequence_length": 2
            },
            {
                "t_start": 2458379.363683,
                "t_end": 2458379.384736,
                "sequence_length": 2
            },
            {
                "t_start": 2458381.544806,
                "t_end": 2458381.565859,
                "sequence_length": 2
            },
            {
                "t_start": 2458388.982919,
                "t_end": 2458389.003971,
                "sequence_length": 2
            },
            {
                "t_start": 2458393.316932,
                "t_end": 2458393.337985,
                "sequence_length": 2
            },
            {
                "t_start": 2458398.814355,
                "t_end": 2458398.835408,
                "sequence_length": 2
            },
            {
                "t_start": 2458405.12949,
                "t_end": 2458405.150543,
                "sequence_length": 2
            },
            {
                "t_start": 2458528.766369,
                "t_end": 2458528.787422,
                "sequence_length": 2
            },
            {
                "t_start": 2458548.153883,
                "t_end": 2458548.174936,
                "sequence_length": 2
            },
            {
                "t_start": 2458552.842448,
                "t_end": 2458552.8635,
                "sequence_length": 2
            },
            {
                "t_start": 2458554.123321,
                "t_end": 2458554.144374,
                "sequence_length": 2
            },
            {
                "t_start": 2458571.12971,
                "t_end": 2458571.150763,
                "sequence_length": 2
            },
            {
                "t_start": 2458572.451016,
                "t_end": 2458572.472069,
                "sequence_length": 2
            },
            {
                "t_start": 2458572.965136,
                "t_end": 2458572.986188,
                "sequence_length": 2
            },
            {
                "t_start": 2458574.014428,
                "t_end": 2458574.035481,
                "sequence_length": 2
            },
            {
                "t_start": 2458579.606589,
                "t_end": 2458579.657548,
                "sequence_length": 2
            },
            {
                "t_start": 2458583.582705,
                "t_end": 2458583.633664,
                "sequence_length": 2
            },
            {
                "t_start": 2458587.390399,
                "t_end": 2458587.411452,
                "sequence_length": 2
            },
            {
                "t_start": 2458588.166006,
                "t_end": 2458588.187058,
                "sequence_length": 2
            },
            {
                "t_start": 2458588.366007,
                "t_end": 2458588.38706,
                "sequence_length": 2
            },
            {
                "t_start": 2458714.615591,
                "t_end": 2458714.636644,
                "sequence_length": 2
            },
            {
                "t_start": 2458719.053195,
                "t_end": 2458719.074248,
                "sequence_length": 2
            },
            {
                "t_start": 2458730.016462,
                "t_end": 2458730.037515,
                "sequence_length": 2
            },
            {
                "t_start": 2458733.478459,
                "t_end": 2458733.499512,
                "sequence_length": 2
            },
            {
                "t_start": 2458743.843395,
                "t_end": 2458743.864448,
                "sequence_length": 2
            },
            {
                "t_start": 2458755.341835,
                "t_end": 2458755.362887,
                "sequence_length": 2
            },
            {
                "t_start": 2458759.075844,
                "t_end": 2458759.096897,
                "sequence_length": 2
            },
            {
                "t_start": 2458761.678023,
                "t_end": 2458761.699075,
                "sequence_length": 2
            },
            {
                "t_start": 2458767.93,
                "t_end": 2458767.951052,
                "sequence_length": 2
            },
            {
                "t_start": 2458775.483902,
                "t_end": 2458775.504955,
                "sequence_length": 2
            },
            {
                "t_start": 2458782.428948,
                "t_end": 2458782.45,
                "sequence_length": 2
            },
            {
                "t_start": 2459623.233745,
                "t_end": 2459623.254798,
                "sequence_length": 2
            },
            {
                "t_start": 2459632.926666,
                "t_end": 2459632.947719,
                "sequence_length": 2
            },
            {
                "t_start": 2459634.521657,
                "t_end": 2459634.54271,
                "sequence_length": 2
            },
            {
                "t_start": 2459635.288411,
                "t_end": 2459635.309463,
                "sequence_length": 2
            },
            {
                "t_start": 2459636.169281,
                "t_end": 2459636.190334,
                "sequence_length": 2
            },
            {
                "t_start": 2459645.369134,
                "t_end": 2459645.390187,
                "sequence_length": 2
            },
            {
                "t_start": 2459648.013419,
                "t_end": 2459648.034471,
                "sequence_length": 2
            },
            {
                "t_start": 2459649.996213,
                "t_end": 2459650.017266,
                "sequence_length": 2
            },
            {
                "t_start": 2459650.299806,
                "t_end": 2459650.320858,
                "sequence_length": 2
            },
            {
                "t_start": 2459654.821621,
                "t_end": 2459654.842674,
                "sequence_length": 2
            },
            {
                "t_start": 2459665.58656,
                "t_end": 2459665.607613,
                "sequence_length": 2
            },
            {
                "t_start": 2459669.80311,
                "t_end": 2459669.824163,
                "sequence_length": 2
            },
            {
                "t_start": 2459677.199117,
                "t_end": 2459677.220169,
                "sequence_length": 2
            },
            {
                "t_start": 2459678.752003,
                "t_end": 2459678.773056,
                "sequence_length": 2
            },
            {
                "t_start": 2459679.580241,
                "t_end": 2459679.601294,
                "sequence_length": 2
            },
            {
                "t_start": 2459680.671639,
                "t_end": 2459680.692692,
                "sequence_length": 2
            },
            {
                "t_start": 2459830.474329,
                "t_end": 2459830.525288,
                "sequence_length": 2
            },
            {
                "t_start": 2459855.56812,
                "t_end": 2459855.955924,
                "sequence_length": 34
            },
            {
                "t_start": 2459865.713675,
                "t_end": 2459865.734728,
                "sequence_length": 2
            },
            {
                "t_start": 2459869.091461,
                "t_end": 2459869.112513,
                "sequence_length": 2
            },
            {
                "t_start": 2459869.395053,
                "t_end": 2459869.416106,
                "sequence_length": 2
            },
            {
                "t_start": 2459875.720714,
                "t_end": 2459875.741767,
                "sequence_length": 2
            },
            {
                "t_start": 2459997.271208,
                "t_end": 2459997.292261,
                "sequence_length": 2
            },
            {
                "t_start": 2460016.648195,
                "t_end": 2460016.669248,
                "sequence_length": 2
            },
            {
                "t_start": 2460030.243547,
                "t_end": 2460030.2646,
                "sequence_length": 2
            },
            {
                "t_start": 2460039.611823,
                "t_end": 2460039.632875,
                "sequence_length": 2
            },
            {
                "t_start": 2460042.559699,
                "t_end": 2460042.580752,
                "sequence_length": 2
            },
            {
                "t_start": 2460052.831571,
                "t_end": 2460052.852624,
                "sequence_length": 2
            },
            {
                "t_start": 2460056.902425,
                "t_end": 2460056.923477,
                "sequence_length": 2
            },
            {
                "t_start": 2460057.353386,
                "t_end": 2460057.374439,
                "sequence_length": 2
            }
        ]
    }
}

class FitAnalystTest:
    """
    Class with tests
    """

    def __init__(self, scenario, answers=None):
        self.scenario = scenario
        if answers is not None:
            self.answer = answers

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

        log = logs.start_log(path_outputs,
                             "debug",
                             event_name=config["event_name"],
                             to_file=False,
                             to_stream=True
                             )
        analyst = FitAnalyst(config["event_name"], path_outputs, light_curves, log, config_dict=config)
        on_mag_t_config = analyst.config["ongoing_magnification_threshold"]
        on_ampl_t_config = analyst.config["ongoing_amplitude_threshold"]
        model_fit_config = analyst.config["model_fit_configuration"]
        af_config = analyst.config.get("anomaly_finder", None)

        logs.close_log(log)

        assert on_mag_t_config == fit_params.get("ongoing_magnification_threshold")
        assert on_ampl_t_config == fit_params.get("ongoing_amplitude_threshold")

        model_params = fit_params.get("anomaly_finder")
        if af_config is not None:
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
        data = np.load(self.answer.get("outlier_results_path"), allow_pickle=True)
        outlier_results = data["arr_0"][()]

        log = logs.start_log(path_outputs,
                             "debug",
                             event_name=config["event_name"],
                             to_stream=False)
        analyst = FitAnalyst(config["event_name"],
                             path_outputs,
                             light_curves,
                             log,
                             config_dict=config,
                             outlier_results=outlier_results,
                             outlier_seqs=self.answer.get("outlier_seqs"),
                             )

        analyst.best_model = self.answer.get("best_model")
        analyst.best_results = self.answer.get("best_results")

        anomaly_found = analyst.perform_anomaly_finding("single_finished_test")
        assert anomaly_found

        starting_params = {
            "ra": config["ra"],
            "dec": config["dec"],
            "t0": 2459807.97,
            "u0": 0.95,
            "log_tE": np.log10(24.0),
            "log_rho": np.log10(0.0013),
            "log_separation": np.log10(0.39),
            "log_mass_ratio": np.log10(0.00075),
            "alpha": 6.14,
            "piEN": 0.0,
            "piEE": 0.0
        }
        analyst.fit_1s2l_finished(start_params=starting_params)
        analyst.best_model = analyst.evaluate_models()
        if analyst.config.get("anomaly_finder", None) is not None:
            anomaly_found = analyst.perform_anomaly_finding("multiple_finished")
            if anomaly_found:
                analyst.log.debug(f"Anomaly found. Pass relevant information to somewhere.")

        analyst.log.debug("Fit Analyst: Best models:")
        for model in analyst.best_results:
            params = analyst.best_results[model]
            parameters_to_log = ["t0", "u0", "tE", "piEN", "piEE", "log_tE", "log_rho", "log_separation",
                                 "log_mass_ratio", "alpha"]
            log_statement = ""
            for parameter in params:
                if parameter in parameters_to_log:
                    log_statement += f"{parameter}: {params[parameter]:.2f} \n"

            analyst.log.debug(
                f"Fit Analyst: {model:s} : \n"
                f"{log_statement}"
            )

        # Find best fitting model
        analyst.log.debug("Fit Analyst: Find best-fitting model.")
        analyst.best_model = analyst.evaluate_models()
        analyst.log.info(f"Fit Analyst: Best fitting model: {analyst.best_model}")

        # Save best results statistics
        file_name = os.path.join(analyst.analyst_path, "fit_stats.txt")
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(
                f"{'# name':<20s} : {'chi2':<9s} {'red_chi2':<9s} "
                f"{'SW':<9s} {'SW_res':<9s} {'AD':<9s} {'AD_res':<9s} "
                f"{'KS':<9s} {'KS_res':<9s} {'AIC':<9s} {'BIC':<9s}\n"
            )
            file.write("#------------------------------------------------------------------------------------------\n")
            for model in analyst.best_results:
                params = analyst.best_results[model]
                file.write(
                    f"{model:20s} : {params['chi2']:9.2f} {params['red_chi2']:9.2f}"
                    f"{params['sw_test']:9.2f} {params['sw_test_result']:9.2f} "
                    f"{params['ad_test']:9.2f} {params['ad_test_result']:9.2f} "
                    f"{params['ks_test']:9.2f} {params['ks_test_result']:9.2f} "
                    f"{params['aic_test']:9.2f} {params['bic_test']:9.2f}\n"
                )


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

    test = FitAnalystTest(scenario_roman, answers=answers_roman)
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
