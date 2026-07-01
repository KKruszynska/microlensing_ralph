import json
import os
from pathlib import Path

import numpy as np
import pytest

from microlensing_ralph.analyst.event_analyst import EventAnalyst
from microlensing_ralph.analyst.fit_analyst import FitAnalyst

ralph_output = os.path.join("tests", "microlensing_ralph", "data", "output")
ralph_input = os.path.join("tests", "microlensing_ralph", "data", "input")
ralph_light_curves = os.path.join(ralph_input, "light_curves")

scenario_file_cat = {
    "event_name": "GDR3_ULENS_025",
    "ra": 260.8781,
    "dec": -27.3788,
    "analyst_path": os.path.join(ralph_output, "event_analyst", "GDR3_ULENS_025"),
    "fit_result": os.path.join(ralph_input, "test_results", "gdr3_ulens_025_fit_results_best.json"),
    "config_final": {
        "event_name": "GDR3_ULENS_025",
        "ra": 260.8781,
        "dec": -27.3788,
        "analyst_path": os.path.join(ralph_output, "event_analyst" "GDR3_ULENS_025"),
        "lc_analyst": {
             "acceptable_mag_range": {
                 "upper_limit": -10,
                 "lower_limit": 30
             },
        },
        "fit_analyst": {
            "ongoing_magnification_threshold": 1.10,
            "ongoing_amplitude_threshold": 1.0,
            "return_all_models": False,
            "model_fit_configuration": {
                "PSPL_no_blend_no_piE": {
                    "fitting_package": "pyLIMA",
                    "fitting_method": "DE",
                    "fitting_method_args": {
                        "DE_population": 10,
                        "loss_function": "soft_l1",
                    },
                    "boundaries": {
                        "u0": [0.0, 2.0],
                    }
                },
                "PSPL_blend_no_piE": {
                    "fitting_package": "pyLIMA",
                    "fitting_method": "TRF",
                    "boundaries": {
                        "u0": [0.0, 2.0],
                    }
                },
                "PSPL_blend_piE": {
                    "fitting_package": "pyLIMA",
                    "fitting_method": "TRF",
                    "boundaries": {
                        "u0": [0.0, 2.0],
                        "piEN": [-1.0, 1.0],
                        "piEE": [-1.0, 1.0],
                    }
                },
                "PSPL_no_blend_piE": {
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
        "cmd_analyst": {
            "catalogues": [
                {
                    "name": "Gaia_DR3",
                    "band": ["Gaia_G", "Gaia_BP", "Gaia_RP"],
                    "cmd_path":
                        os.path.join("tests","microlensing_ralph","data","input","cmd","gdr3_ulens_025_result.csv"),
                    "cmd_separator": ",",
                },
            ]
        },
    },
    "final_files": {
        "event_folder": "GDR3_ULENS_025",
        "analyst_log": "GDR3_ULENS_025_analyst.log",
        "model_plots": [
            "PSPL_blend_piE_n.html",
        ],
        "cmd_plots": [
            "GDR3_ULENS_025_PSPL_blend_piE_n_CMD_Gaia_DR3_Gaia_BP.html",
            "GDR3_ULENS_025_PSPL_blend_piE_n_CMD_Gaia_DR3_Gaia_G.html",
            "GDR3_ULENS_025_PSPL_blend_piE_n_CMD_Gaia_DR3_Gaia_RP.html",
        ],
    },
}

scenario_gsa = {
    "event_name": "Gaia24amo",
    "ra": 249.14892083,
    "dec": -53.74991944,
    "analyst_path": os.path.join(ralph_output, "event_analyst", "Gaia24amo"),
    "lc_analyst": {
        "acceptable_mag_range": {
            "upper_limit": -10,
            "lower_limit": 30
        },
    },
    "fit_analyst": {
        "ongoing_magnification_threshold": 1.10,
        "ongoing_amplitude_threshold": 1.0,
        "return_all_models": True,
        "model_fit_configuration": {
            "PSPL_no_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "DE",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "PSPL_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "PSPL_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
            "PSPL_no_blend_piE": {
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
            "ephemeris": os.path.join(ralph_input, "ephemeris", "gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_input, "light_curves", "Gaia24amo_Gaia_G.dat"),
        },
        {
            "survey": "LCO",
            "band": "g",
            "path": os.path.join(ralph_input, "light_curves", "cleaned_Gaia24amo_LCO_g.dat"),
        },
        {
            "survey": "LCO",
            "band": "r",
            "path": os.path.join(ralph_input, "light_curves", "cleaned_Gaia24amo_LCO_r.dat"),
        },
        {
            "survey": "LCO",
            "band": "i",
            "path": os.path.join(ralph_input, "light_curves", "cleaned_Gaia24amo_LCO_i.dat"),
        },
    ],
    "final_files": {
        "event_folder": "Gaia24amo",
        "analyst_log": "Gaia24amo_analyst.log",
        "model_plots": [
            "PSPL_no_blend_no_piE.html",
            "PSPL_blend_no_piE.html",
            "PSPL_blend_piE.html",
        ],
    },
}

scenario_kwu = {
    "event_name": "AT2024kwu",
    "ra": 102.93358333,
    "dec": 44.352166666,
    "analyst_path": os.path.join(ralph_output, "event_analyst", "AT2024kwu/"),
    "lc_analyst": {
        "acceptable_mag_range": {
            "upper_limit": -10,
            "lower_limit": 30
        },
    },
    "fit_analyst": {
        "ongoing_magnification_threshold": 1.10,
        "ongoing_amplitude_threshold": 1.0,
        "model_fit_configuration": {
            "PSPL_no_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "DE",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "PSPL_blend_no_piE": {
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
            "PSPL_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "DE",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
            "PSPL_no_blend_piE": {
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
            "ephemeris": os.path.join(ralph_input, "ephemeris", "gaia_jpl_horizons_results.txt"),
            "path": os.path.join(ralph_input, "light_curves", "AT2024kwu_Gaia_G.dat"),
        },
        {
            "survey": "LCO",
            "band": "g",
            "path": os.path.join(ralph_input, "light_curves", "AT2024kwu_LCO_g.dat"),
        },
        {
            "survey": "LCO",
            "band": "r",
            "path": os.path.join(ralph_input, "light_curves", "AT2024kwu_LCO_r.dat"),
        },
        {
            "survey": "LCO",
            "band": "i",
            "path": os.path.join(ralph_input, "light_curves", "AT2024kwu_LCO_i.dat"),
        },
        {
            "survey": "ZTF",
            "band": "g",
            "path": os.path.join(ralph_input, "light_curves", "AT2024kwu_ZTF_g.dat"),
        },
        {
            "survey": "ZTF",
            "band": "r",
            "path": os.path.join(ralph_input, "light_curves", "AT2024kwu_ZTF_r.dat"),
        },
    ],
    "final_files": {
        "event_folder": "AT2024kwu",
        "analyst_log": "AT2024kwu_analyst.log",
        "model_plots": [
            "PSPL_no_blend_no_piE.html",
            "PSPL_blend_no_piE.html",
            "PSPL_blend_piE.html",
        ],
    },
}

scenario_roman = {
    "analyst_path": os.path.join(ralph_output, "fit_analyst"),
    "event_name": "ulwdc1_018_W149",
    "ra": 267.871,
    "dec": -29.6712,
    "lc_analyst": {"acceptable_mag_range":
                       {"upper_limit": -5, "lower_limit": 30},
                   "max_acceptable_err": 1.0,
                   "hampel": {
                       "window": "1D",
                       "n_sigma": 3.0,
                       "use_weighted": False,
                   },
                   "save_outlier_results": True,
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
            "af_setup": {
                "window": "3D",
                "n_sigma": 2.0,
                "use_weighted": True,
            },
        },
        "model_fit_configuration": {
            "PSPL_no_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "PSPL_blend_no_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [0.0, 2.0],
                }
            },
            "PSPL_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
                }
            },
            "PSPL_no_blend_piE": {
                "fitting_package": "pyLIMA",
                "fitting_method": "TRF",
                "boundaries": {
                    "u0": [-2.0, 2.0],
                    "piEN": [-1.0, 1.0],
                    "piEE": [-1.0, 1.0],
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
    "best_model": "PSPL_blend_piE_p",
    "best_results": {
        "PSPL_blend_piE_p": {
            "t0_par": 2458752,
            "t0": 2458743.906,
            "t0_error": 0.026,
            "u0": 0.01155,
            "u0_error": 0.00092,
            "tE": 1000.0,
            "tE_error": 79.807,
            "piEN": -0.40413,
            "piEN_error": 0.03165,
            "piEE": -0.17856,
            "piEE_error": 0.01415,
            "fsource_Roman_W149": 2.92895,
            "fsource_Roman_W149_error": 0.23624,
            "fsource_Roman_W149_mag": 26.233,
            "fsource_Roman_W149_mag_error": 0.088,
            "ftotal_Roman_W149": 991.89766,
            "ftotal_Roman_W149_error": 0.07052,
            "ftotal_Roman_W149_mag": 19.909,
            "ftotal_Roman_W149_mag_error": 0.0,
            "chi2": 180988.529,
            "fblend_Roman_W149": 988.96871,
            "fblend_Roman_W149_error": 0.24654088504749067,
            "fblend_Roman_W149_mag": 19.912,
            "fblend_Roman_W149_mag_error": 0.0,
            "source_magnitude": 26.233,
            "source_mag_error": 0.088,
            "blend_magnitude": 19.912,
            "blend_mag_error": 0.0,
            "baseline_magnitude": 19.909,
            "baseline_mag_error": 0.0,
            "red_chi2": 4.716,
            "sw_test": 0.45,
            "ad_test": 2922.717,
            "ks_test": 0.024,
            "aic_test": 181002.529,
            "bic_test": 181062.417
        },
    },
}

class EventAnalystTest:
    """
    Class with Event Analyst tests
    """

    def __init__(self, scenario):
        self.scenario = scenario

    def test_parse_config(self):
        """
        Test if configuration is parsed correctly.
        """

        event_name = self.scenario.get("event_name")
        analyst_path = self.scenario.get("analyst_path")
        event_analyst = EventAnalyst(
            event_name,
            analyst_path,
            "debug",
            config_path=os.path.join(analyst_path, "config.yaml"),
            stream=True
        )
        event_analyst.parse_config(os.path.join(analyst_path, "config.yaml"))

        assert type(event_analyst.config) is type(self.scenario.get("config_final"))

        for element in event_analyst.config:
            assert event_analyst.config[element] == self.scenario.get("config_final")[element]

    def test_run_analyst_file(self):
        """
        Test running a single event analyst with config from a file.
        """

        event_name = self.scenario.get("event_name")
        analyst_path = self.scenario.get("analyst_path")
        event_analyst = EventAnalyst(
            event_name,
            analyst_path,
            "debug",
            config_path=os.path.join(analyst_path, "config.yaml"),
            stream=False
        )
        event_analyst.run_single_analyst()

        # Check if expected files exist
        fpath = os.path.join(analyst_path, "fit_results.json")
        output = Path(fpath)
        assert output.exists() is True
        assert output.is_file() is True

        fpath = os.path.join(analyst_path, "fit_stats.txt")
        output = Path(fpath)
        assert output.exists() is True
        assert output.is_file() is True

        final_files = self.scenario.get("final_files")
        for element in final_files:
            if element == "event_folder":
                output = Path(analyst_path)
                assert output.exists() is True
                assert output.is_dir() is True

            if element == "analyst_log":
                fpath = os.path.join(analyst_path, final_files[element])
                output = Path(fpath)
                assert output.exists() is True
                assert output.is_file() is True

            if element == "model_plots":
                for file_path in final_files[element]:
                    fpath = os.path.join(analyst_path, file_path)
                    output = Path(fpath)
                    assert output.exists() is True
                    assert output.is_file() is True

            if element == "cmd_plots":
                for file_path in final_files[element]:
                    fpath = os.path.join(analyst_path, file_path)
                    output = Path(fpath)
                    assert output.exists() is True
                    assert output.is_file() is True

        with open(self.scenario.get("fit_result"), "r") as file:
            expected_fit_result = json.load(file)

        fpath = os.path.join(analyst_path, "fit_results.json")
        with open(fpath, "r") as file:
            received_fit_result = json.load(file)

        for model in expected_fit_result:
            if model != "PSPL_no_blend_no_piE":
                model_result = received_fit_result[model]
                expected_result = expected_fit_result[model]
                for key in expected_result:
                    expected = float(expected_result[key])
                    received = float(model_result[key])
                    if not np.isnan(expected):
                        assert pytest.approx(received, 2) == pytest.approx(expected, 2)

    def test_run_analyst_dict(self):
        """
        Test running a single event analyst with a config from a dictionary.
        """

        event_name = self.scenario.get("event_name")
        analyst_path = self.scenario.get("analyst_path")
        event_analyst = EventAnalyst(
            event_name, analyst_path, "debug", config_dict=self.scenario, stream=False
        )
        event_analyst.run_single_analyst()

        # Check if expected files exist
        fpath = os.path.join(analyst_path, "fit_results.json")
        output = Path(fpath)
        assert output.exists() is True
        assert output.is_file() is True

        fpath = os.path.join(analyst_path, "fit_stats.txt")
        output = Path(fpath)
        assert output.exists() is True
        assert output.is_file() is True

        final_files = self.scenario.get("final_files")
        for element in final_files:
            if element == "event_folder":
                output = Path(analyst_path)
                assert output.exists() is True
                assert output.is_dir() is True

            if element == "analyst_log":
                fpath = os.path.join(analyst_path, final_files[element])
                output = Path(fpath)
                assert output.exists() is True
                assert output.is_file() is True

            if element == "model_plots":
                for file_path in final_files[element]:
                    fpath = os.path.join(analyst_path, file_path)
                    output = Path(fpath)
                    assert output.exists() is True
                    assert output.is_file() is True

            if element == "cmd_plots":
                for file_path in final_files[element]:
                    fpath = os.path.join(analyst_path, file_path)
                    output = Path(fpath)
                    assert output.exists() is True
                    assert output.is_file() is True

        # Testing if the PSPL_blend_no_piE model makes sense
        fpath = os.path.join(analyst_path, "fit_results.json")
        with open(fpath, "r") as file:
            received_fit_result = json.load(file)

        expected_range = {
            "t0": [2457000.0, 2460600.0],
            "u0": [-2.0, 2.0],
            "tE": [1.0, 500.0]
        }
        model_result = received_fit_result["PSPL_blend_no_piE"]
        for key in ["t0", "u0", "tE"]:
            received = float(model_result[key])
            lower = expected_range[key][0]
            upper = expected_range[key][1]
            if not np.isnan(received):
                assert (lower <= received <= upper)

    def test_anomaly_finder(self):
        """
        Test running an anomaly finder with Hampel filter.
        """

        event_name = self.scenario.get("event_name")
        analyst_path = self.scenario.get("analyst_path")
        event_analyst = EventAnalyst(
            event_name, analyst_path, "debug", config_dict=self.scenario, stream=False
        )
        event_analyst.run_lc_analyst()
        fit_analyst = FitAnalyst(
            event_analyst.event_name, event_analyst.analyst_path, event_analyst.light_curves, event_analyst.log,
            outlier_results=event_analyst.outlier_results, outlier_seqs=event_analyst.outlier_seqs,
            config_dict=event_analyst.config
        )

        for entry in fit_analyst.light_curves:
            # extract np array with the light curve
            lc_tag = f"{entry["survey"]}_{entry["band"]}"
            lc = np.array(entry["light_curve"])
            if lc_tag in fit_analyst.outlier_results:
                outlier_flags =  fit_analyst.outlier_results[lc_tag]["is_outlier"]
                entry["light_curve_with_outliers"] = lc
                entry["light_curve"] = lc[~outlier_flags]

        fit_analyst.best_model = self.scenario.get("best_model")
        fit_analyst.best_results = self.scenario.get("best_results")

        fit_analyst.perform_anomaly_finding()



    @pytest.mark.skip(reason="This test is for debugging code only")
    def test_no_config(self):
        """
        Test if an error is raised when there is no configuration
        for the Event Analyst.
        """

        event_analyst = EventAnalyst(
            "no_config", "tests/microlensing_ralph/data/output/event_analyst/no_config/",
            "debug", config_dict=self.scenario, stream=True
        )


def test_run():
    """
    Run all tests.
    """

    # case = scenario_file_cat
    # test = EventAnalystTest(case)
    # test.test_parse_config()
    # test.test_run_analyst_file()
    #
    # for case in [scenario_kwu, scenario_gsa]:
    #     test = EventAnalystTest(case)
    #     test.test_run_analyst_dict()

    test = EventAnalystTest(scenario_roman)
    test.test_anomaly_finder()

    # # Remove created files
    # for case in [scenario_file_cat, scenario_kwu, scenario_gsa]:
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
    #     files_to_remove = [
    #         "PSPL_no_blend_no_piE.html",
    #         "PSPL_blend_no_piE.html",
    #         "PSPL_blend_piE.html",
    #         "PSPL_blend_piE_p.html",
    #         "PSPL_blend_piE_n.html",
    #         "PSPL_no_blend_piE.html",
    #     ]
    #     for element in files_to_remove:
    #         fpath = os.path.join(analyst_path, element)
    #         output = Path(fpath)
    #         if output.exists():
    #             os.remove(output)
    #
    #     if event_name == "GDR3_ULENS_025":
    #         files_to_remove = [
    #             "GDR3_ULENS_025_PSPL_blend_piE_n_CMD_Gaia_DR3_Gaia_BP.html",
    #             "GDR3_ULENS_025_PSPL_blend_piE_n_CMD_Gaia_DR3_Gaia_G.html",
    #             "GDR3_ULENS_025_PSPL_blend_piE_n_CMD_Gaia_DR3_Gaia_RP.html",
    #         ]
    #         for element in files_to_remove:
    #             fpath = os.path.join(analyst_path, element)
    #             output = Path(fpath)
    #             if output.exists():
    #                 os.remove(output)
