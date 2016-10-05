
import numpy as np
from matplotlib import pyplot as plt

flogname = '/home/acp/work/aws/mcatch/slog.txt'

a = np.loadtxt( flogname )

Ss = np.transpose(a)

plt.figure()
for r in Ss:
    plt.plot( r )
plt.show()
