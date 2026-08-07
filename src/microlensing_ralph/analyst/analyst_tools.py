
import numpy as np
import pandas as pd
import weightedstats as wst

from astropy.table import QTable
from astropy.time import Time
from astropy.timeseries import TimeSeries, aggregate_downsample
from astropy import units as u

from microlensing_ralph.fitting_support.pylima import fit_pylima

def get_baseline_mag(mag_source, err_source, mag_blend, err_blend, fit_package, log):
    """
    Returns baseline magnitude based on source and blend magnitude.

    :param mag_source: Source brightness in magnitudes.
    :type mag_source: float

    :param err_source: Source uncertainty in magnitudes.
    :type err_source: float

    :param mag_blend: Blend brightness in magnitudes.
    :type mag_blend: float

    :param err_blend: blend uncertainty in magnitudes.
    :type err_blend: float

    :param fit_package: Name of the package used for fitting events.
    :type fit_package: str

    :param log: A logger instance started by the Event Analyst.
    :type log: logging.Logger

    :return: Baseline brightness and its uncertainty in magnitudes.
    :rtype: [float, float]
    """
    baseline_mag, err_baseline_mag = None, None

    if not np.isnan(mag_source) and not np.isnan(mag_blend):
        if fit_package.lower() == "pylima":
            baseline_mag, err_baseline_mag = fit_pylima.return_baseline_mag(
                mag_source, err_source, mag_blend, err_blend, log
            )
        else:
            placeholder(10)

    return [baseline_mag, err_baseline_mag]


def get_blend_mag(mag_source, err_source, mag_base, err_base, fit_package, log):
    """
    Returns blend magnitude based on source and baseline magnitude.

    :param mag_source: Source brightness in magnitudes.
    :type mag_source: float

    :param err_source: Source uncertainty in magnitudes.
    :type err_source: float

    :param mag_base: Baseline brightness in magnitudes.
    :type mag_base: float

    :param err_base: Baseline uncertainty in magnitudes.
    :type err_base: float

    :param fit_package: The name of the package used for fitting events.
    :type fit_package: str

    :param log: A logger instance started by the Event Analyst.
    :type log: logging.Logger

    :return: Baseline brightness and its uncertainty in magnitudes.
    :rtype: [float, float]
    """
    blend_mag, err_blend_mag = None, None

    if not np.isnan(mag_source) and not np.isnan(mag_base):
        if fit_package.lower() == "pylima":
            blend_mag, err_blend_mag = fit_pylima.return_blend_mag(
                mag_source, err_source, mag_base, err_base, log
            )
        else:
            placeholder(10)

    return [blend_mag, err_blend_mag]


def placeholder(n_max):
    """
    Placeholder function to put in parts of the code that are not complete.
    It counts to the number of n_max end then ends.

    :param n_max: A maximum number of the counter.
    :type n_max: int

    :return: Counted number, equal to n_max.
    :rtype: int
    """

    count = 0
    for _i in range(n_max):
        count += 1

    return count


def find_time_of_peak(light_curves, bin_size):
    """
    Finds the time of peak among all the light curves.

    :param light_curves: A list of  dictionaries containing light curves.
    :type light_curves: list

    :return: time of peak in JD
    :rtype: float
    """

    time_of_peak = 0.0
    max_amplitude = 0.0
    for entry in light_curves:
        lc = np.asarray(entry["light_curve"])
        time = Time(lc[:,0], format='jd')
        mag, err = lc[:,1] * u.mag, lc[:,2] * u.mag
        lc = QTable(
            data=[time, mag, err],
            names=['time', 'mag', 'err'],
        )
        time_series = TimeSeries(lc)
        lc_binned = aggregate_downsample(
            time_series,
            time_bin_size=bin_size * u.day,
            aggregate_func=np.nanmedian
        )

        idx_max = np.nanargmin(lc_binned['mag'])
        amplitude = np.nanmax(lc_binned['mag']) - lc_binned['mag'][idx_max]
        time_max = lc_binned['time_bin_start'][idx_max]

        if max_amplitude < amplitude:
            time_of_peak, max_amplitude = time_max, amplitude

    return time_of_peak.jd


def check_ongoing_time(model_params, time_now):
    """
    Checks if based on current time and model, the event reached baseline.
    This check is passed if current time is smaller than the sum of the time
    of peak and Einstein time.

    :param model_params: A dictionary containing model parameters.
    :type model_params: dict

    :param time_now: Julian Date of the latest data point.
    :type time_now: float

    :return: A flag, `True` if time of the latest data point is larger than the sum
        of the base point source-point lens model's time of peak and Einstein timescale,
        `False` otherwise.
    :rtype: bool
    """
    ongoing = False
    t_0, t_e = model_params["t0"], model_params["tE"]

    if t_0 + t_e > time_now:
        ongoing = True

    return ongoing


def check_ongoing_amplitude(threshold, aligned_data, residuals, baseline_mag):
    """
    Checks if the event is over or not, comparing baseline magnitude, magnitude
    of the last point aligned with the model and the standard deviation of the
    model residuals.

    :param threshold: Threshold for the amplitude; if the amplitude is larger than
        the threshold amount of standard deviation of the light curve, then the event
        is considered ongoing.
    :type threshold: float

    :param aligned_data: An array containing photometric data aligned to
        a microlensing model.
    :type aligned_data: numpy array

    :param residuals: An array containing residuals of the microlensing model.
    :type residuals: numpy array

    :param baseline_mag: The baseline magnitude of the microlensing model.
    :type baseline_mag: float

    :return: A flag of the amplitude check and the Julian Date of the latest data point.
        The flag is `True` if the amplitude at the lastest data point is above
        the threshold times standard deviation from the baseline, `False` otherwise.
    :rtype: bool, float
    """
    ongoing = False

    # find standard deviation
    sigmas = []
    for data in residuals:
        sigmas.append(np.std(data[:, 1]))
    sigmas = np.asarray(sigmas)
    std_mag = np.sqrt(np.sum(sigmas**2))

    # Find last data point
    t_last = 0
    for data in aligned_data:
        if data[-1, 0] > t_last:
            t_last = data[-1, 0]
            if np.abs(data[-1, 1] - baseline_mag) > threshold * std_mag:
                ongoing = True

    return ongoing, t_last


def check_ongoing_magnification(threshold, model_params, time_now):
    """
    Checks if the event is ongoing based on microlensing model's magnification.

    :param threshold: A threshold for microlensing model's magnification, if larger
                       the event is considered ongoing.
    :type threshold: float

    :param model_params: A dictionary containing microlensing model parameters.
    :type model_params: dict

    :param time_now: Julian Date of the latest data point.
    :type time_now: float

    :return: A flag, `True` if the magnification of the base point source-point lens model
        at the latest data point is larger than the threshold, `False` otherwise.
    :rtype: bool
    """
    ongoing = False
    t_0, u_0, t_e = model_params["t0"], model_params["u0"], model_params["tE"]

    tau = (time_now - t_0) / t_e
    u = np.sqrt(u_0**2 + tau**2)
    magnification = (u**2 + 2) / (u * np.sqrt(u**2 + 4))

    if magnification > threshold:
        ongoing = True

    return ongoing

def hampel_filter(light_curve, window='3D', n_sigma=5.0, use_weighted=False):
    """
    A Hampel filter with a time-based window. More about Hampel filter can be
    found [here](https://medium.com/@migueloteropedrido/hampel-filter-with-python-17db1d265375).
    This method was created with the help of Claude.ai, and modified to resemble the output
    of the [hampel](https://github.com/MichaelisTrofficus/hampel_filter/tree/master) package.

    :param light_curve: An array containing Julian Days, magnitudes and errors
            for the whole light curve.
    :type light_curve: numpy ndarray

    :param window: Window size (in days), as a `pandas` offset string (e.g. '3D' is 3 days),
        half of this is applied on each side of each point.
    :type window: str

    :param n_sigma: Number of standard deviations to use for Hampel filter, used as a threshold in
        scaled Median Absolute Deviation for flagging outliers.
    :type n_sigma: float

    :param use_weighted: If `True` weighted median is used.
    :type use_weighted: bool

    :return: A dictionary with the light curve, an array of points marked as outliers, array of
        (weighted) medians for each window, array of MADs for each window, and array
        of thresholds for each window.
    thresholds for each window.
    :rtype: dict
    """
    datetime = pd.to_datetime(light_curve[:, 0], origin='julian', unit='D')
    series = pd.Series(light_curve[:, 1], index=datetime)
    series = series.sort_index()
    times = series.index
    values = series.to_numpy()
    half_window = pd.Timedelta(window) / 2
    k = 1.4826  # scales MAD to be comparable to std dev for normal data

    is_outlier = np.zeros(len(values), dtype=bool)
    medians = np.zeros(len(values), dtype=float)
    mads = np.zeros(len(values), dtype=float)
    thresholds = np.zeros(len(values), dtype=float)
    weights = 1.0 / (light_curve[:, 2]**2)

    for i, t in enumerate(times):
        left = times.searchsorted(t - half_window, side='left')
        right = times.searchsorted(t + half_window, side='right')
        window_vals = values[left:right]

        if use_weighted:
            window_weights = weights[left:right]
            med = wst.numpy_weighted_median(window_vals, weights=window_weights)
        else:
            med = np.median(window_vals)

        mad = k * np.median(np.abs(window_vals - med))
        thresh = n_sigma * mad

        if mad > 0 and np.abs(values[i] - med) > thresh:
            is_outlier[i] = True

        medians[i] = med
        mads[i] = mad
        thresholds[i] = thresh

    result = {
        'light_curve': light_curve,
        'is_outlier': is_outlier,
        'medians': medians,
        'mads': mads,
        'thresholds': thresholds,
    }

    return result

def vet_outliers(light_curve, is_outlier, log):
    """
    Function that checks if found outliers form a sequence of consecutive points
    in the light curve. Doesn't take into time-skips between data.

    :param light_curve: An array containing Julian Days, magnitudes and errors
            for the whole light curve.
    :type light_curve: numpy ndarray

    :param is_outlier: An array indicating whether point at this index is considered
        an outlier by the outlier flagging procedure
        (e.g., :meth:`microlensing_ralph.analyst.light_curve_analyst.LightCurveAnalyst.hampel_filter`).

    :return: A list of dictionaries with all found sequences of outliers, marking their
        start time, end time and length of the sequence.
    """
    groups = []
    n_seqs = 0
    n_pts_in_seq = 0
    t_start, t_end = 0.0, 0.0
    total_points = 0
    for i in range(len(light_curve[:, 0])):
        if is_outlier[i]:
            n_pts_in_seq += 1
            if n_pts_in_seq == 1:
                t_start = light_curve[i, 0]
        else:
            t_end = light_curve[i, 0]
            if n_pts_in_seq > 1:
                n_seqs += 1
                new_sequence = {
                    't_start': t_start,
                    't_end': t_end,
                    'sequence_length': n_pts_in_seq,
                }
                groups.append(new_sequence)
                total_points += n_pts_in_seq
            n_pts_in_seq = 0

    log.debug(f"Vet outliers: Found {total_points} in total, among {n_seqs} sequences.")
    return groups

def get_anomaly_information(anomaly_seqs, residuals):
    """
    Get information necessary about the anomaly to calculate starting parameters.

    :param anomaly_seqs: A dictionary with list sequences of candidate anomalous points for each filter.
    :type anomaly_seqs: dict

    :param residuals: A dictionary with JD, residuals and errors for each filter.
    :type residuals: dict

    :return: A dictionary with information about the anomaly, containing following keywords:
        * `t_anomaly`
        * `duration_anomaly`
        * `ampl_anomaly`
    """

    t_start = np.inf
    t_end = 0.
    for band in anomaly_seqs:
        for seq in anomaly_seqs[band]:
            if t_start > seq["t_start"]:
                t_start = seq["t_start"]
            if t_end < seq["t_end"]:
                t_end = seq["t_end"]

    amplitude = 0.0
    t_anomaly = np.nan
    for band in residuals:
        lc = residuals[band]
        anomalous_idx = np.intersect1d(np.where(lc[:, 0] > t_start), np.where(lc[:, 0] < t_end))
        anomalous_res = lc[anomalous_idx, :]

        max_idx = np.argmax(np.abs(anomalous_res[:,1]))
        ampl = 0 - anomalous_res[max_idx, 1]

        if np.abs(ampl) > np.abs(amplitude):
            amplitude = ampl
            t_anomaly = anomalous_res[max_idx, 0]

        result = {
            "t_anomaly": t_anomaly,
            "duration_anomaly": t_end - t_start,
            "ampl_anomaly": amplitude,
        }

    return result



def get_binary_starting_params(t0, u0, tE, t_anomaly, duration_anomaly, ampl_anomaly):
    """
    Get starting parameters for binary lens fitting.

    :param t0: Time of peak of the 1S1L model without second-order effects.
    :type t0: float

    :param u0: Impact parameter of the 1S1L model without second-order effects.
    :type u0: float

    :param tE: Einstein timescale of the 1S1L model without second-order effects.
    :type tE: float

    :param t_anomaly: Time of peak of the anomaly.
    :type t_anomaly: float

    :param duration_anomaly: How long anomaly lasts, in days.
    :type duration_anomaly: float

    :param ampl_anomaly: Amplitude of the anomaly.
    :type ampl_anomaly: float

    :return: A dictionary with the following keys:
        * `log_rho` -- log10 of source angular radius in Einstein radii;
        * `log_mass_ratio` -- log10 of mass ratio;
        * `log_separation` -- log10 of components separation in Einstein radii;
        * `alpha` -- angle between
    """

    # Rho
    rho = duration_anomaly / tE

    # Mass ratio
    mass_ratio = np.abs(ampl_anomaly) * rho**2 / 2.0

    # Separation
    tau = np.abs((t_anomaly - t0) / tE)
    u = np.sqrt(tau**2 + u0**2)
    y_plus = 0.5 * np.sqrt(u**2 + 4.0) + u
    y_minus = 0.5 * np.sqrt(u**2 + 4.0) - u

    if ampl_anomaly > 0:
        separation = y_plus
    else:
        separation = y_minus

    #Alpha
    alpha = np.atan(u0 / tau)

    result = {
        "log_rho": np.log10(rho),
        "log_mass_ratio": np.log10(mass_ratio),
        "log_separation": np.log10(separation),
        "alpha": alpha
    }
    return result