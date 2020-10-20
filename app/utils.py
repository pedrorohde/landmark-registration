import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator


def logistic(x, x0=0, L=1, k=1):
    return L/(1+np.exp(-k*(x-x0)))


def double_logistic(x, x0=[0,1], L=1, k=[1,1]):
    return logistic(x, x0[0], L, k[0]) - logistic(x, x0[1], L, k[1])


def n_random_double_logistic(N, x):

    max_slope = np.random.uniform(4, 8, [2,N])
    dt = np.random.uniform([[0.1], [0.5]], [[0.5], [0.9]], [2,N])
    max_value = np.random.uniform(0.5, 1, [1,N])

    return double_logistic(x, dt, max_value, 4*max_slope/max_value), (max_slope, dt, max_value)

def inflection_points(data, dx):

    dmax = np.diff(data,n=1,axis=0).argmax(axis=0)*dx
    dmin = np.diff(data,n=1,axis=0).argmin(axis=0)*dx

    return np.concatenate([[dmax], [dmin]])


def landmark_registration(x, data, landmarks, new_landmarks):
    
    tmin = x[0, 0]
    tmax = x[-1, 0]
    N = data.shape[1]
    
    t = np.concatenate([[tmin], new_landmarks, [tmax]])
    ht = np.concatenate([tmin*np.ones([1,N]), landmarks, tmax*np.ones([1,N])])

    warpings = PchipInterpolator(t,ht,axis=0)(x).squeeze()
    registered_data = np.array([CubicSpline(x.squeeze(),data[:,i],axis=0)(warpings[:,i]).squeeze() for i in range(N)]).T

    return registered_data, warpings


def warping(x, landmarks, new_landmarks):

    tmin = x[0, 0]
    tmax = x[-1, 0]
    N = landmarks.shape[1]

    t =  np.concatenate([tmin*np.ones([1,N]), new_landmarks, tmax*np.ones([1,N])])
    ht = np.concatenate([tmin*np.ones([1,N]), landmarks,     tmax*np.ones([1,N])])

    warpings = np.hstack([PchipInterpolator(t[:,i], ht[:,i])(x) for i in range(N)])

    return warpings


def compose(x, data, warpings):

    N = data.shape[1]
    composition = np.array([CubicSpline(x.squeeze(),data[:,i],axis=0)(warpings[:,i]).squeeze() for i in range(N)]).T
    
    return composition