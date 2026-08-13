scenario_roman_bin_star = {
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
                "fitting_method_args": {
                    "loss_function" : "chi2",
                },
                "boundaries": {
                    "u0": [0.0, 2.5],
                }
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
            "path": os.path.join(ralph_light_curves, "ulwdc1_018_W149.txt"),
        },
    ],
}

answers_roman_bin_star = {
    "best_model": "1S1L_blend_piE_p",
    "best_results": {
        "1S1L_blend_piE_p": {
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
        "1S1L_blend_no_piE": {
            "t0_par": 0.0,
            "t0": 2458749.39,
            "t0_error": 0.057,
            "u0": 0.3,
            "u0_error": 0.05,
            "tE": 14.8,
            "tE_error": 4.288,
            "fsource_Roman_W149": 352515.59,
            "fsource_Roman_W149_error": 4000.0,
            "ftotal_Roman_W149": 992.76,
            "ftotal_Roman_W149_error": 0.06583,
        },
    },
    "outlier_results_path": os.path.join(ralph_input, "test_results", "ulwdc1_018_outlier_results.npz"),
    "outlier_seqs": {
        "Roman_W149": [{
            "t_start": 2458743.874974,
            "t_end": 2458744.146987,
            "sequence_length": 23
        }]
    }
}