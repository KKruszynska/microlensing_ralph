import json
import os
import time
from pathlib import Path

import numpy as np

from microlensing_ralph.analyst import analyst_tools
from microlensing_ralph.analyst.analyst import BaseAnalyst
from microlensing_ralph.fitting_support import pylima

from microlensing_ralph.toolbox.output_tools import plot_outlier_results

def fit_1S1L(
    self,
    fit_name,
    light_curves,
    starting_params,
    parallax,
    blend,
    return_norm_lc=False,
    use_boundaries=None,
    fitting_method=None,
    **kwargs,
):
    """
    Perform a point source-point lens model fit.

    :param fit_name: A label, but in fact a path to which the plot with
        the best-fitting model will be saved.
    :type fit_name: str

    :param light_curves: A list of dictionaries with event name, light curve, survey name,
        filter name, and, if available, an ephemeris of the space observatory which was
        used to obtain the observations.
    :type light_curves: list

    :param starting_params: A dictionary containing starting parameters.
    :type starting_params: dict

    :param parallax: If `True` microlensing parallax effect will be included in the model,
        if `False` it will not.
    :type parallax: bool

    :param blend: If `True` blending will be fitted for this event, if `False`, the model
        will assume that all light is coming from the source.
    :type blend: bool

    :param return_norm_lc: If `True`, this method will return a light curve and residuals
        aligned to the best-fitting model it found.
    :type return_norm_lc: bool, optional

    :param use_boundaries: A dictionary containing upper and lower limits for specific
        model parameters, defined by the User.
    :type use_boundaries: dict, optional

    :param fitting_method: A label of the type of fitting method used in pyLIMA;
        Available options: TRF, DE.
    :type fitting_method: str, optional

    :param kwargs: Optional keyword arguments holding information about fitting method set up
    :type kwargs: dict, optional

    :return: A dictionary with the parameters of the best-fitting model, and, if available,
        a list with a light curve aligned to it and its residuals.
    :rtype: list
    """

    # Setup event
    with capture_prints(self.log, capture_stderr=True):
        event_name = fit_name
        ra, dec = float(starting_params["ra"]), float(starting_params["dec"])
        event = self.setup_event(event_name, ra, dec, light_curves)

        blend_param = "ftotal" if blend else "noblend"

        if parallax:
            self.log.info("Fit Analyst -- pyLIMA: Fitting with microlensing parallax.")
            pspl = PSPL_model.PSPLmodel(
                event, parallax=["Full", int(starting_params["t0"])], blend_flux_parameter=blend_param
            )
        else:
            self.log.info("Fit Analyst -- pyLIMA: Fitting without microlensing parallax.")
            pspl = PSPL_model.PSPLmodel(event, parallax=["None", 0.0], blend_flux_parameter=blend_param)

        DE_population, loss_function = None, None
        for key, value in kwargs.items():
            if key == "DE_population":
                DE_population = int(value)
            if key == "loss_function":
                loss_function = value

        if fitting_method is not None:
            self.log.info(f"Fit Analyst -- pyLIMA: Fitting method: {fitting_method}.")
            if loss_function is None:
                loss_function = "soft_l1"
            if fitting_method == "DE":
                if DE_population is None:
                    DE_population = 10
                self.log.debug(f"Fit Analyst -- pyLIMA: Fitting method set up: DE_pop={DE_population}.")
                self.log.debug(f"Fit Analyst -- pyLIMA: Fitting method set up: loss_fun={loss_function}.")
                fit_event = DE_fit.DEfit(pspl, DE_population_size=DE_population, loss_function=loss_function)
            elif fitting_method == "TRF":
                self.log.debug(f"Fit Analyst -- pyLIMA: Fitting method set up: loss_fun={loss_function}.")
                fit_event = TRF_fit.TRFfit(pspl, loss_function=loss_function)
        else:
            self.log.info("Fit Analyst -- pyLIMA: Using default fitting method (TRF).")
            fit_event = TRF_fit.TRFfit(pspl, loss_function="soft_l1")

        # Use boundries like in mop.toolbox.fittools
        if use_boundaries is None:
            self.log.info("Fit Analyst -- pyLIMA: Using boundaries default for microlensing_ralph.")
            delta_t0 = 50.0
            default_t0_lower = fit_event.fit_parameters["t0"][1][0]
            default_t0_upper = fit_event.fit_parameters["t0"][1][1]
            fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]
            fit_event.fit_parameters["tE"][1] = [0.0, 1000.0]
            fit_event.fit_parameters["u0"][1] = [0.0, 2.0]
            if parallax:
                fit_event.fit_parameters["piEN"][1] = [-2.0, 2.0]
                fit_event.fit_parameters["piEE"][1] = [-2.0, 2.0]
        else:
            self.log.info("Fit Analyst -- pyLIMA: Using boundaries passed by the User.")
            if "t0" not in use_boundaries:
                delta_t0 = 50.0
                default_t0_lower = fit_event.fit_parameters["t0"][1][0]
                default_t0_upper = fit_event.fit_parameters["t0"][1][1]
                fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]
            for key in use_boundaries:
                self.log.debug(f"Fit Analyst -- pyLIMA: Boundaries for {key} = {use_boundaries[key]}.")
                fit_event.fit_parameters[key][1] = [use_boundaries[key][0], use_boundaries[key][1]]
            if "t0" not in use_boundaries:
                delta_t0 = 50.0
                default_t0_lower = fit_event.fit_parameters["t0"][1][0]
                default_t0_upper = fit_event.fit_parameters["t0"][1][1]
                fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]

        for key in fit_event.fit_parameters:
            self.log.debug(
                f"Fit Analyst -- pyLIMA: Final boundaries for {key} = {fit_event.fit_parameters[key][1]}."
            )
        self.log.info(f"Fit Analyst -- pyLIMA: Adding starting parameters:")
        start_guess = []
        for key in fit_event.fit_parameters:
            if key in starting_params:
                self.log.info(
                    f"Fit Analyst -- pyLIMA: Adding starting parameters: {key} = {starting_params[key]}"
                )
                start_guess.append(starting_params[key])
        fit_event.model_parameters_guess = start_guess

        self.log.info("Fit Analyst -- pyLIMA: Starting fit.")
        fit_event.fit()
        self.log.info("Fit Analyst -- pyLIMA: Fitting finished")

        # This will have to be modified to be compatible with MOP
        self.log.debug("Fit Analyst -- pyLIMA: Convert model parameters to dictionary.")
        model_parameters = self.gather_parameters(event, fit_event, fitting_method=fitting_method)

        # Produce fit outputs here
        plots_pylima.plot_pylima(event, fit_event, self.log)

        if return_norm_lc:
            norm_lc, residuals = self.get_aligned_data(pspl, fit_event.fit_results["best_model"])
            return model_parameters, norm_lc, residuals

    return model_parameters

    # def fit_2S1L(
    #     self,
    #     fit_name,
    #     light_curves,
    #     starting_params,
    #     parallax,
    #     blend,
    #     return_norm_lc=False,
    #     use_boundaries=None,
    #     fitting_method=None,
    #     **kwargs
    # ):
    #     """
    #     Perform a binary source-point lens model fit.
    #
    #     :param fit_name: A label, but in fact a path to which the plot with
    #         the best-fitting model will be saved.
    #     :type fit_name: str
    #
    #     :param light_curves: A list of dictionaries with event name, light curve, survey name,
    #         filter name, and, if available, an ephemeris of the space observatory which was
    #         used to obtain the observations.
    #     :type light_curves: list
    #
    #     :param starting_params: A dictionary containing starting parameters.
    #     :type starting_params: dict
    #
    #     :param parallax: If `True` microlensing parallax effect will be included in the model,
    #         if `False` it will not.
    #     :type parallax: bool
    #
    #     :param blend: If `True` blending will be fitted for this event, if `False`, the model
    #         will assume that all light is coming from the source.
    #     :type blend: bool
    #
    #     :param return_norm_lc: If `True`, this method will return a light curve and residuals
    #         aligned to the best-fitting model it found.
    #     :type return_norm_lc: bool, optional
    #
    #     :param use_boundaries: A dictionary containing upper and lower limits for specific
    #         model parameters, defined by the User.
    #     :type use_boundaries: dict, optional
    #
    #     :param fitting_method: A label of the type of fitting method used in pyLIMA;
    #         Available options: TRF, DE.
    #     :type fitting_method: str, optional
    #
    #     :param kwargs: Optional keyword arguments holding information about fitting method set up
    #     :type kwargs: dict, optional
    #
    #     :return: A dictionary with the parameters of the best-fitting model, and, if available,
    #         a list with a light curve aligned to it and its residuals.
    #     :rtype: list
    #     """
    #
    #     # Setup event
    #     event_name = fit_name
    #     ra, dec = float(starting_params["ra"]), float(starting_params["dec"])
    #     event = self.setup_event(event_name, ra, dec, light_curves)
    #
    #     blend_param = "ftotal" if blend else "noblend"
    #
    #     if parallax:
    #         self.log.info("Fit Analyst -- pyLIMA: Fitting with microlensing parallax.")
    #         bspl = PSPL_model.PSPLmodel(
    #             event, parallax=["Full", int(starting_params["t0"])], blend_flux_parameter=blend_param
    #         )
    #     else:
    #         self.log.info("Fit Analyst -- pyLIMA: Fitting without microlensing parallax.")
    #         pspl = PSPL_model.PSPLmodel(event, parallax=["None", 0.0], blend_flux_parameter=blend_param)
    #
    #     DE_population, loss_function = None, None
    #     for key, value in kwargs.items():
    #         if key == "DE_population":
    #             DE_population = int(value)
    #         if key == "loss_function":
    #             loss_function = value
    #
    #     if fitting_method is not None:
    #         self.log.info(f"Fit Analyst -- pyLIMA: Fitting method: {fitting_method}.")
    #         if loss_function is None:
    #             loss_function = "soft_l1"
    #         if fitting_method == "DE":
    #             if DE_population is None:
    #                 DE_population = 10
    #             self.log.debug(
    #                 f"Fit Analyst -- pyLIMA: Fitting method set up: DE_pop={DE_population}."
    #             )
    #             self.log.debug(
    #                 f"Fit Analyst -- pyLIMA: Fitting method set up: loss_fun={loss_function}."
    #             )
    #             fit_event = DE_fit.DEfit(pspl,
    #                                      DE_population_size=DE_population,
    #                                      loss_function=loss_function
    #                                      )
    #         elif fitting_method == "TRF":
    #             self.log.debug(
    #                 f"Fit Analyst -- pyLIMA: Fitting method set up: loss_fun={loss_function}."
    #             )
    #             fit_event = TRF_fit.TRFfit(pspl, loss_function=loss_function)
    #     else:
    #         self.log.info("Fit Analyst -- pyLIMA: Using default fitting method (TRF).")
    #         fit_event = TRF_fit.TRFfit(pspl, loss_function="soft_l1")
    #
    #     # Use boundries like in mop.toolbox.fittools
    #     if use_boundaries is None:
    #         self.log.info("Fit Analyst -- pyLIMA: Using boundaries default for microlensing_ralph.")
    #         delta_t0 = 50.0
    #         default_t0_lower = fit_event.fit_parameters["t0"][1][0]
    #         default_t0_upper = fit_event.fit_parameters["t0"][1][1]
    #         fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]
    #         fit_event.fit_parameters["tE"][1] = [0.0, 1000.0]
    #         fit_event.fit_parameters["u0"][1] = [0.0, 2.0]
    #         if parallax:
    #             fit_event.fit_parameters["piEN"][1] = [-2.0, 2.0]
    #             fit_event.fit_parameters["piEE"][1] = [-2.0, 2.0]
    #     else:
    #         self.log.info("Fit Analyst -- pyLIMA: Using boundaries passed by the User.")
    #         if "t0" not in use_boundaries:
    #             delta_t0 = 50.0
    #             default_t0_lower = fit_event.fit_parameters["t0"][1][0]
    #             default_t0_upper = fit_event.fit_parameters["t0"][1][1]
    #             fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]
    #         for key in use_boundaries:
    #             self.log.debug(
    #                 f"Fit Analyst -- pyLIMA: Boundaries for {key} = {use_boundaries[key]}."
    #             )
    #             fit_event.fit_parameters[key][1] = [use_boundaries[key][0], use_boundaries[key][1]]
    #         if "t0" not in use_boundaries:
    #             delta_t0 = 50.0
    #             default_t0_lower = fit_event.fit_parameters["t0"][1][0]
    #             default_t0_upper = fit_event.fit_parameters["t0"][1][1]
    #             fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]
    #
    #     for key in fit_event.fit_parameters:
    #         self.log.debug(
    #             f"Fit Analyst -- pyLIMA: Final boundaries for {key} = {fit_event.fit_parameters[key][1]}."
    #         )
    #     self.log.info(f"Fit Analyst -- pyLIMA: Adding starting parameters:")
    #     start_guess = []
    #     for key in fit_event.fit_parameters:
    #         if key in starting_params:
    #             self.log.info(
    #                 f"Fit Analyst -- pyLIMA: Adding starting parameters: {key} = {starting_params[key]}"
    #             )
    #             start_guess.append(starting_params[key])
    #     fit_event.model_parameters_guess = start_guess
    #
    #     self.log.info("Fit Analyst -- pyLIMA: Starting fit.")
    #     fit_event.fit()
    #     self.log.info("Fit Analyst -- pyLIMA: Fitting finished")
    #
    #     # This will have to be modified to be compatible with MOP
    #     self.log.debug("Fit Analyst -- pyLIMA: Convert model parameters to dictionary.")
    #     model_parameters = self.gather_parameters(event, fit_event, fitting_method=fitting_method)
    #
    #     # Produce fit outputs here
    #     plots_pylima.plot_pylima(event, fit_event, self.log)
    #
    #     if return_norm_lc:
    #         norm_lc, residuals = self.get_aligned_data(pspl, fit_event.fit_results["best_model"])
    #         return model_parameters, norm_lc, residuals
    #
    #     return model_parameters


def fit_1S2L(
    self,
    fit_name,
    light_curves,
    starting_params,
    parallax,
    blend,
    return_norm_lc=False,
    use_boundaries=None,
    fitting_method=None,
    **kwargs,
):
    """
    Perform a single source-binary lens model fit.

    :param fit_name: A label, but in fact a path to which the plot with
        the best-fitting model will be saved.
    :type fit_name: str

    :param light_curves: A list of dictionaries with event name, light curve, survey name,
        filter name, and, if available, an ephemeris of the space observatory which was
        used to obtain the observations.
    :type light_curves: list

    :param starting_params: A dictionary containing starting parameters.
    :type starting_params: dict

    :param parallax: If `True` microlensing parallax effect will be included in the model,
        if `False` it will not.
    :type parallax: bool

    :param blend: If `True` blending will be fitted for this event, if `False`, the model
        will assume that all light is coming from the source.
    :type blend: bool

    :param return_norm_lc: If `True`, this method will return a light curve and residuals
        aligned to the best-fitting model it found.
    :type return_norm_lc: bool, optional

    :param use_boundaries: A dictionary containing upper and lower limits for specific
        model parameters, defined by the User.
    :type use_boundaries: dict, optional

    :param fitting_method: A label of the type of fitting method used in pyLIMA;
        Available options: TRF, DE.
    :type fitting_method: str, optional

    :param kwargs: Optional keyword arguments holding information about fitting method set up
    :type kwargs: dict, optional

    :return: A dictionary with the parameters of the best-fitting model, and, if available,
        a list with a light curve aligned to it and its residuals.
    :rtype: list
    """

    # Setup event
    with capture_prints(self.log, capture_stderr=True):
        event_name = fit_name
        ra, dec = float(starting_params["ra"]), float(starting_params["dec"])
        event = self.setup_event(event_name, ra, dec, light_curves)

        blend_param = "ftotal" if blend else "noblend"

        fancy = pyLIMA_fancy_parameters.StandardFancyParameters()

        if parallax:
            self.log.info("Fit Analyst -- pyLIMA: Fitting with microlensing parallax.")
            usbl = USBL_model.USBLmodel(
                event,
                fancy_parameters=fancy,
                parallax=["Full", int(starting_params["t0"])],
                blend_flux_parameter=blend_param,
            )
        else:
            self.log.info("Fit Analyst -- pyLIMA: Fitting without microlensing parallax.")
            usbl = USBL_model.USBLmodel(
                event, fancy_parameters=fancy, parallax=["None", 0.0], blend_flux_parameter=blend_param
            )

        DE_population, loss_function = None, None
        for key, value in kwargs.items():
            if key == "DE_population":
                DE_population = int(value)
            if key == "loss_function":
                loss_function = value

        if fitting_method is not None:
            self.log.info(f"Fit Analyst -- pyLIMA: Fitting method: {fitting_method}.")
            if loss_function is None:
                loss_function = "soft_l1"
            if fitting_method == "DE":
                if DE_population is None:
                    DE_population = 10
                self.log.debug(f"Fit Analyst -- pyLIMA: Fitting method set up: DE_pop={DE_population}.")
                self.log.debug(f"Fit Analyst -- pyLIMA: Fitting method set up: loss_fun={loss_function}.")
                fit_event = DE_fit.DEfit(usbl, DE_population_size=DE_population, loss_function=loss_function)
            elif fitting_method == "TRF":
                self.log.debug(f"Fit Analyst -- pyLIMA: Fitting method set up: loss_fun={loss_function}.")
                fit_event = TRF_fit.TRFfit(usbl, loss_function=loss_function)
        else:
            self.log.info("Fit Analyst -- pyLIMA: Using default fitting method (TRF).")
            fit_event = TRF_fit.TRFfit(usbl, loss_function="soft_l1")

        # Use boundries like in mop.toolbox.fittools
        if use_boundaries is None:
            self.log.info("Fit Analyst -- pyLIMA: Using boundaries default for microlensing_ralph.")
            delta_t0 = 50.0
            default_t0_lower = fit_event.fit_parameters["t0"][1][0]
            default_t0_upper = fit_event.fit_parameters["t0"][1][1]
            fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]
            fit_event.fit_parameters["u0"][1] = [0.0, 2.0]
            fit_event.fit_parameters["log_tE"][1] = [-1.0, 3.5]
            fit_event.fit_parameters["log_rho"][1] = [-5.0, 1.0]
            fit_event.fit_parameters["log_separation"][1] = [-4.0, 2.0]
            fit_event.fit_parameters["log_mass_ratio"][1] = [-5.0, 1.0]
            fit_event.fit_parameters["alpha"][1] = [0.0, 2 * np.pi]
            if parallax:
                fit_event.fit_parameters["piEN"][1] = [-2.0, 2.0]
                fit_event.fit_parameters["piEE"][1] = [-2.0, 2.0]
        else:
            self.log.info("Fit Analyst -- pyLIMA: Using boundaries passed by the User.")
            if "t0" not in use_boundaries:
                delta_t0 = 50.0
                default_t0_lower = fit_event.fit_parameters["t0"][1][0]
                default_t0_upper = fit_event.fit_parameters["t0"][1][1]
                fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]
            for key in use_boundaries:
                self.log.debug(f"Fit Analyst -- pyLIMA: Boundaries for {key} = {use_boundaries[key]}.")
                fit_event.fit_parameters[key][1] = [use_boundaries[key][0], use_boundaries[key][1]]
            if "t0" not in use_boundaries:
                delta_t0 = 50.0
                default_t0_lower = fit_event.fit_parameters["t0"][1][0]
                default_t0_upper = fit_event.fit_parameters["t0"][1][1]
                fit_event.fit_parameters["t0"][1] = [default_t0_lower, default_t0_upper + delta_t0]

        for key in fit_event.fit_parameters:
            self.log.debug(
                f"Fit Analyst -- pyLIMA: Final boundaries for {key} = {fit_event.fit_parameters[key][1]}."
            )
        self.log.info(f"Fit Analyst -- pyLIMA: Adding starting parameters:")

        start_guess = []
        for key in fit_event.fit_parameters:
            if key in starting_params:
                self.log.info(
                    f"Fit Analyst -- pyLIMA: Adding starting parameters: {key} = {starting_params[key]}"
                )
                start_guess.append(starting_params[key])

        fit_event.model_parameters_guess = start_guess

        self.log.info("Fit Analyst -- pyLIMA: Starting fit.")
        fit_event.fit()
        self.log.info("Fit Analyst -- pyLIMA: Fitting finished")

        # This will have to be modified to be compatible with MOP
        self.log.debug("Fit Analyst -- pyLIMA: Convert model parameters to dictionary.")
        model_parameters = self.gather_parameters(event, fit_event, fitting_method=fitting_method)

        # Produce fit outputs here
        plots_pylima.plot_pylima(event, fit_event, self.log)

        if return_norm_lc:
            norm_lc, residuals = self.get_aligned_data(usbl, fit_event.fit_results["best_model"])
            return model_parameters, norm_lc, residuals

        return model_parameters
