import json
import os
from pathlib import Path

import numpy as np
import pytest

from microlensing_ralph.controller.controller import Controller

ralph_tests_home = os.path.join("tests", "microlensing_ralph", "data")

config_finished = {
            "python_compiler": "python",
            "group_processing_limit": 2,
            "events_path": os.path.join(ralph_tests_home, "input", "controller"),
            "software_dir": os.path.join("src", "microlensing_ralph", "analyst"),
            "config_type": "yaml",
            "log_stream": False,
            "log_location": os.path.join(ralph_tests_home, "output", "controller_launch"),
            "log_level": "debug",
        }

config_ongoing = {
            "python_compiler": "python",
            "group_processing_limit": 2,
            "config_type": "yaml",
            "events_path": os.path.join(ralph_tests_home, "input", "controller"),
            "software_dir": os.path.join("src", "microlensing_ralph", "analyst"),
            "log_stream": False,
            "log_location": os.path.join(ralph_tests_home, "output", "controller_analysts"),
            "log_level": "debug",
        }


class ControllerTest:
    """
    Tests to check if controller works.
    """

    def __init__(self, event_list, config, expected_results):
        self.event_list = event_list
        self.config = config
        self.expected_results = expected_results

    def set_up(self):
        controller = Controller(self.event_list , config_dict=self.config)
        controller.launch_analysts()

    def check_results(self):
        # Check if expected files exist
        # Controller log
        controller_log_path = self.config.get("log_location")
        output = Path(os.path.join(controller_log_path, "controller.log"))
        assert output.exists() is True
        assert output.is_file() is True

        # Analyst output files
        analyst_home = self.config.get("events_path")
        for event in self.event_list:
            analyst_path = os.path.join(analyst_home, event)

            output = Path(analyst_path)
            assert output.exists() is True
            assert output.is_dir() is True

            output = Path(os.path.join(analyst_path, "fit_results.json"))
            assert output.exists() is True
            assert output.is_file() is True

            output = Path(os.path.join(analyst_path, "fit_stats.txt"))
            assert output.exists() is True
            assert output.is_file() is True

            output = Path(os.path.join(analyst_path, event + "_analyst.log"))
            assert output.exists() is True
            assert output.is_file() is True

            if event == "AT2024kwu":
                model_plots = [
                    "PSPL_no_blend_no_piE",
                    "PSPL_blend_no_piE",
                    "PSPL_blend_piE",
                ]
            else:
                model_plots = [
                    "PSPL_no_blend_no_piE",
                    "PSPL_blend_no_piE",
                    "PSPL_blend_piE_p",
                    "PSPL_blend_piE_n",
                ]

            for file_path in model_plots:
                output = Path(os.path.join(analyst_path, file_path + ".html"))
                assert output.exists() is True
                assert output.is_file() is True

            if event == "GDR3_ULENS_025":
                bands = [
                    "_CMD_Gaia_DR3_Gaia_G",
                    "_CMD_Gaia_DR3_Gaia_BP",
                    "_CMD_Gaia_DR3_Gaia_RP",
                ]
                for model in model_plots:
                    for band in bands:
                        output = Path(os.path.join(analyst_path, event + "_" + model + band + ".html"))
                        assert output.exists() is True
                        assert output.is_file() is True

            expected_result_path = self.expected_results.get(event, None)
            keys_to_check = ["t0", "u0", "tE", "piEN", "piEE"]
            if expected_result_path is not None:
                with open(expected_result_path, "r") as file:
                    expected_fit_result = json.load(file)

                with open(os.path.join(analyst_path, "fit_results.json"), "r") as file:
                    received_fit_result = json.load(file)

                for model in expected_fit_result:
                    model_result = received_fit_result[model]
                    expected_result = expected_fit_result[model]

                    for key in keys_to_check:
                        if key in expected_result:
                            expected = float(expected_result[key])
                            received = float(model_result[key])
                            if not np.isnan(expected):
                                assert pytest.approx(received, rel=1e-1) == pytest.approx(expected, rel=1e-1)

def test_run():
    """
    Run all tests.
    """

    expected_fit_results = {
        "GDR3_ULENS_025": os.path.join(ralph_tests_home, "input", "test_results", "gdr3_ulens_025_fit_results.json"),
        "GDR3_ULENS_018": os.path.join(ralph_tests_home, "input", "test_results", "gdr3_ulens_018_fit_results.json"),
    }

    event_list = ["GDR3_ULENS_025"]
    test = ControllerTest(event_list, config_finished, expected_fit_results)
    test.set_up_controller()
    test.check_results()

    event_list = ["AT2024kwu", "Gaia18cbf", "GDR3_ULENS_018"]
    test = ControllerTest(event_list, config_ongoing, expected_fit_results)
    test.set_up_controller()
    test.check_results()

    controller_log_path = [
        os.path.join(ralph_tests_home, "output", "controller_launch"),
        os.path.join(ralph_tests_home, "output", "controller_analysts"),
    ]

    for controller_path in controller_log_path:
        output = Path(os.path.join(controller_path, "controller.log"))
        if output.exists():
            os.remove(output)

    analyst_home = os.path.join(ralph_tests_home, "input", "controller")

    test_events = [
        "AT2024kwu",
        "GDR3_ULENS_018",
        "GDR3_ULENS_025",
        "Gaia18cbf",
    ]

    for event in test_events:
        analyst_path = os.path.join(analyst_home, event)

        output = Path(os.path.join(analyst_path, "fit_results.json"))
        if output.exists():
            os.remove(output)

        output = Path(os.path.join(analyst_path,  "fit_stats.txt"))
        if output.exists():
            os.remove(output)

        fpath = os.path.join(analyst_path, event + "_analyst.log")
        output = Path(fpath)
        if output.exists():
            os.remove(output)

        model_plots = [
            "PSPL_no_blend_no_piE",
            "PSPL_blend_no_piE",
            "PSPL_blend_piE",
            "PSPL_blend_piE_p",
            "PSPL_blend_piE_n",
            "PSPL_no_blend_piE",
            "PSPL_no_blend_piE_p",
            "PSPL_no_blend_piE_n"
        ]

        for file_path in model_plots:
            output = Path(os.path.join(analyst_path, file_path + ".html"))
            if output.exists():
                os.remove(output)

        bands = [
            "_CMD_Gaia_DR3_Gaia_G",
            "_CMD_Gaia_DR3_Gaia_BP",
            "_CMD_Gaia_DR3_Gaia_RP",
        ]
        for model in model_plots:
            for band in bands:
                output = Path(os.path.join(analyst_path, event + "_" + model + band + ".html"))
                if output.exists():
                    os.remove(output)
