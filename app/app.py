from utils import *
from matplotlib import pyplot as plt
import streamlit as st
import seaborn as sns
sns.set()


st.title('Functional Data Analysis')
st.write('Curve alignment through _landmark_ registration')

N = 5
x = np.linspace([0],[1],101)
dx = np.diff(x, axis=0).mean()

data, params = n_random_double_logistic(N, x)
max_slope, dt, max_value = params


# fig,ax = plt.subplots()
# ax.plot(x, data)
# ax.set_ylim([0,1])
# ax.set_title(f'{N} random double logistic functions')
# ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$g(t)$')

# st.pyplot(fig)


fig,ax = plt.subplots()
ax.plot(x,data,alpha=0.5)
ax.plot(x,data.mean(axis=1),'--k',label='cross-sectional mean')
ax.set_ylim([0,1])
ax.set_title(f'{N} random double logistic functions')
ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$g(t)$')
ax.legend()

st.pyplot(fig)


landmarks = inflection_points(data, dx)
landmarks_mean = landmarks.mean(axis=1)


fig,ax = plt.subplots()
ax.plot(landmarks_mean,landmarks,'o')
ax.set_xlabel(r'chronological time $t$')
ax.set_ylabel(r'registered time $h(t)$')
ax.set_xlim([0,1]); ax.set_ylim([0,1])
ax.set_aspect('equal', 'box')

st.pyplot(fig)


registered_data, warpings = landmark_registration(x, data, landmarks, landmarks_mean)

fig,ax = plt.subplots()
ax.plot(x,warpings)
ax.set_prop_cycle(None)
ax.plot(landmarks_mean,landmarks,'o')
ax.plot(x,x,'--k')
ax.set_xlabel(r'chronological time $t$')
ax.set_ylabel(r'registered time $h(t)$')
ax.set_xlim([0,1]); ax.set_ylim([0,1])
ax.set_aspect('equal', 'box')

st.pyplot(fig)


fig,ax = plt.subplots();
ax.plot(x,registered_data);
ax.plot(x,registered_data.mean(axis=1),'--k',label='cross-sectional mean');
ax.set_ylim([0,1])
ax.set_title(f'{N} registered double logistic functions');
ax.legend();

st.pyplot(fig)

