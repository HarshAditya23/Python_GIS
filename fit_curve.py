# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 16:49:17 2022

@author: gaurh
"""

import numpy as np
from scipy import optimize

lst0 = 20
delta_lst = 40
tau = 365*24*3600*1000
phi = 2*np.pi*4*30.5*3600*1000/tau


def fit_func(t, lst0, delta_lst, tau, phi):
    return lst0 + (delta_lst/2)*np.sin(2*np.pi*t/tau + phi)


x_axis_urban = np.asanyarray(Urban_df['time'].apply(float))
x_axis_rural = np.asanyarray(Rural_df['time'].apply(float))

y_axis_urban = np.asanyarray(Urban_df['LST_Day_1km'].apply(float))
y_axis_rural = np.asanyarray(Rural_df['LST_Day_1km'].apply(float))

params_u, params_covariance_u = optimize.curve_fit(
        fit_func, x_axis_urban, y_axis_urban, p0=[lst0, delta_lst, tau, phi])
params_r, params_covariance_r = optimize.curve_fit(
        fit_func, x_axis_rural, y_axis_rural, p0=[lst0, delta_lst, tau, phi])
