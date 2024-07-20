import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (18,10)
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['axes.linewidth'] = 1

font = {'size': 16}
plt.rc('font', **font)

# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "sans-serif",
#     "font.serif": ["Computer Modern Serif"],
#     })

plt.rcParams['font.sans-serif'] = "Arial"

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.spines.left'] = True
plt.rcParams['axes.spines.right'] = False

plt.rcParams['axes.linewidth'] = 0.5

font = {'size': 12}
plt.rc('font', **font)

plt.rc('lines', linewidth=1.2)

plt.rcParams['ytick.direction'] = 'out'
plt.rcParams['xtick.direction'] = 'out'

plt.rc('ytick.major', size=7)
plt.rc('xtick.major', size=7)

plt.rc('ytick.minor', size=5)
plt.rc('xtick.minor', size=5)
plt.rc('ytick.minor', width=0.5)
plt.rc('xtick.minor', width=0.5)

plt.rc('ytick.major', width=0.5)
plt.rc('xtick.major', width=0.5)

plt.rcParams['xtick.major.pad']= 5
plt.rcParams['ytick.major.pad']= 5

