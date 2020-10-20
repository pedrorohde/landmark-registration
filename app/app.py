from utils import *
from matplotlib import pyplot as plt
import streamlit as st
import time
import seaborn as sns
import copy
sns.set()


# @st.cache
# def _data_run():

#     N = 5
#     x = np.linspace([0],[1],101)
#     dx = np.diff(x, axis=0).mean()

#     data, params = n_random_double_logistic(N, x)
#     max_slope, dt, max_value = params

#     landmarks = inflection_points(data, dx)
#     landmarks_mean = landmarks.mean(axis=1)

#     registered_data, warpings = landmark_registration(x, data, landmarks, landmarks_mean)

#     return N, x, dx, data, params, landmarks, landmarks_mean, registered_data, warpings

# @st.cache
# def data_plot(N, x, dx, data, params, landmarks, landmarks_mean, registered_data, warpings):
#     fig, ax = plt.subplots(1,2, figsize=(20,5))

#     data_line = ax[0].plot(x,data,alpha=0.5)
#     ax[0].set_prop_cycle(None)
#     landmark_data_points = ax[0].plot(landmarks, data[np.round(landmarks/dx).astype(np.int), range(N)], 'o')
#     mean_line = ax[0].plot(x,data.mean(axis=1),'--k',label='cross-sectional mean')
#     ax[0].set_ylim([0,1])
#     ax[0].set_title(f'{N} random double logistic functions')
#     ax[0].set_xlabel(r'$t$'); ax[0].set_ylabel(r'$g(t)$')
#     ax[0].legend()

#     warping_line = ax[1].plot([np.nan] * len(x), [np.nan] * len(x))
#     ax[1].set_prop_cycle(None)
#     landmark_warping_points = ax[1].plot(landmarks,landmarks,'o')
#     ax[1].set_xlabel(r'chronological time $t$')
#     ax[1].set_ylabel(r'registered time $h(t)$')
#     ax[1].set_xlim([0,1]); ax[1].set_ylim([0,1])
#     ax[1].set_aspect('equal', 'box')

#     the_plot = st.pyplot(fig)

#     return fig, ax


st.title('Functional Data Analysis')
st.subheader('Curve alignment through landmark registration')

# N, x, dx, data, params, landmarks, landmarks_mean, registered_data, warpings = _data_run()

# out_copy = copy.deepcopy(_data_run())
# N, x, dx, data, params, landmarks, landmarks_mean, registered_data, warpings = out_copy

@st.cache
def _init(N):
    N = 5
    x = np.linspace([0],[1],101)
    dx = np.diff(x, axis=0).mean()

    data, params = n_random_double_logistic(N, x)
    max_slope, dt, max_value = params

    landmarks = inflection_points(data, dx)

    return x, dx, data, params, landmarks

N = 5
x, dx, data, params, landmarks = copy.deepcopy(_init(N))

plot = st.line_chart(data)

# fig, ax = plt.subplots(1,2, figsize=(20,5))

# data_line = ax[0].plot(x,data,alpha=0.5)
# ax[0].set_prop_cycle(None)
# landmark_data_points = ax[0].plot(landmarks, data[np.round(landmarks/dx).astype(np.int), range(N)], 'o')
# mean_line = ax[0].plot(x,data.mean(axis=1),'--k',label='cross-sectional mean')
# ax[0].set_ylim([0,1])
# ax[0].set_title(f'{N} random double logistic functions')
# ax[0].set_xlabel(r'$t$'); ax[0].set_ylabel(r'$g(t)$')
# ax[0].legend()

# warping_line = ax[1].plot([np.nan] * len(x), [np.nan] * len(x))
# ax[1].set_prop_cycle(None)
# landmark_warping_points = ax[1].plot(landmarks,landmarks,'o')
# ax[1].set_xlabel(r'chronological time $t$')
# ax[1].set_ylabel(r'registered time $h(t)$')
# ax[1].set_xlim([0,1]); ax[1].set_ylim([0,1])
# ax[1].set_aspect('equal', 'box')

tmp = st.empty()

def _align(plot, data, landmarks, tmp, steps=100):

    landmarks_mean = landmarks.mean(axis=1).reshape(-1,1)
    new_landmarks = landmarks
    step = (landmarks_mean-landmarks)/steps

    for i in range(1,steps+1):
        new_landmarks = landmarks + i/steps*(landmarks_mean-landmarks)
        warpings = warping(x, landmarks, new_landmarks)
        warped_data = compose(x, data, warpings)
        plot.line_chart(warped_data)
        tmp.text(f'{round(i/steps*100)}%')

    return warped_data

if st.button('Align'):
    data = _align(plot, data, landmarks, tmp, 100)
    st.write('done')


# # fig,ax = plt.subplots()
# # ax.plot(x, data)
# # ax.set_ylim([0,1])
# # ax.set_title(f'{N} random double logistic functions')
# # ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$g(t)$')

# # st.pyplot(fig)


# fig,ax = plt.subplots()
# ax.plot(x,data,alpha=0.5)
# ax.plot(x,data.mean(axis=1),'--k',label='cross-sectional mean')
# ax.set_ylim([0,1])
# ax.set_title(f'{N} random double logistic functions')
# ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$g(t)$')
# ax.legend()

# st.pyplot(fig)



# fig,ax = plt.subplots()
# ax.plot(landmarks_mean,landmarks,'o')
# ax.set_xlabel(r'chronological time $t$')
# ax.set_ylabel(r'registered time $h(t)$')
# ax.set_xlim([0,1]); ax.set_ylim([0,1])
# ax.set_aspect('equal', 'box')

# st.pyplot(fig)



# fig,ax = plt.subplots()
# ax.plot(x,warpings)
# ax.set_prop_cycle(None)
# ax.plot(landmarks_mean,landmarks,'o')
# ax.plot(x,x,'--k')
# ax.set_xlabel(r'chronological time $t$')
# ax.set_ylabel(r'registered time $h(t)$')
# ax.set_xlim([0,1]); ax.set_ylim([0,1])
# ax.set_aspect('equal', 'box')

# st.pyplot(fig)


# fig,ax = plt.subplots();
# ax.plot(x,registered_data);
# ax.plot(x,registered_data.mean(axis=1),'--k',label='cross-sectional mean');
# ax.set_ylim([0,1])
# ax.set_title(f'{N} registered double logistic functions');
# ax.legend();

# st.pyplot(fig)
