from array import array
from PyEMD import EMD
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
import numpy as np
from scipy.signal import hilbert
from PyEMD.compact import filt6, pade6
from matplotlib.pyplot import MultipleLocator

# Visualisation is an optional module. To minimise installation, `matplotlib` is not added
# by default. Please install extras with `pip install -r requirement-extra.txt`.
try:
    import pylab as plt
except ImportError:
    pass


class Visualisation(object):
    """Simple visualisation helper.

    This class is for quick and simple result visualisation.
    """

    PLOT_WIDTH = 6
    PLOT_HEIGHT_PER_IMF = 1.5

    def __init__(self, emd_instance=None):
        self.emd_instance = emd_instance

        self.imfs = None
        self.residue = None

        if emd_instance is not None:
            self.imfs, self.residue = self.emd_instance.get_imfs_and_residue()

    def _check_imfs(self, imfs, residue, include_residue):
        """Checks for passed imfs and residue."""
        imfs = imfs if imfs is not None else self.imfs
        residue = residue if residue is not None else self.residue

        if imfs is None:
            raise AttributeError("No imfs passed to plot")

        if include_residue and residue is None:
            raise AttributeError("Requested to plot residue but no residue provided")

        return imfs, residue

    def plot_imfs(self, imfs=None, residue=None, t=None, include_residue=True):
        """Plots and shows all IMFs.

        All parameters are optional since the `emd` object could have been passed when instantiating this object.

        The residual is an optional and can be excluded by setting `include_residue=False`.
        """
        imfs, residue = self._check_imfs(imfs, residue, include_residue)

        num_rows, t_length = imfs.shape
        num_rows += include_residue is True

        t = t if t is not None else range(t_length)

        fig, axes = plt.subplots(num_rows, 1, figsize=(self.PLOT_WIDTH, num_rows * self.PLOT_HEIGHT_PER_IMF))

        if num_rows == 1:
            axes = list(axes)

        axes[0].set_title("Time series")

        for num, imf in enumerate(imfs):
            ax = axes[num]
            ax.plot(t, imf)
            ax.set_ylabel("IMF " + str(num + 1))

        if include_residue:
            ax = axes[-1]
            ax.plot(t, residue)
            ax.set_ylabel("Res")

        # Making the layout a bit more pleasant to the eye
        plt.tight_layout()


    def plot_instant_freq(self, t, imfs=None, order=False, alpha=None):
        """Plots and shows instantaneous frequencies for all provided imfs.

        The necessary parameter is `t` which is the time array used to compute the EMD.
        One should pass `imfs` if no `emd` instances is passed when creating the Visualisation object.

        Parameters
        ----------

        order : bool (default: False)
            Represents whether the finite difference scheme is
            low-order (1st order forward scheme) or high-order (6th order
            compact scheme). The default value is False (low-order)

        alpha : float (default: None)
            Filter intensity. Default value is None, which
            is equivalent to `alpha` = 0.5, meaning that no filter is applied.
            The `alpha` values must be in between -0.5 (fully active) and 0.5
            (no filter).
        """
        if alpha is not None:
            assert -0.5 < alpha < 0.5, "`alpha` must be in between -0.5 and 0.5"

        imfs, _ = self._check_imfs(imfs, None, False)
        num_rows = imfs.shape[0]

        imfs_inst_freqs = self._calc_inst_freq(imfs, t, order=order, alpha=alpha)

        fig, axes = plt.subplots(num_rows, 1, figsize=(self.PLOT_WIDTH, num_rows * self.PLOT_HEIGHT_PER_IMF))

        if num_rows == 1:
            axes = fig.axes

        axes[0].set_title("Instantaneous frequency")

        for num, imf_inst_freq in enumerate(imfs_inst_freqs):
            ax = axes[num]
            ax.plot(t, imf_inst_freq)
            ax.set_ylabel("IMF {} [Hz]".format(num + 1))

        # Making the layout a bit more pleasant to the eye
        plt.tight_layout()


    def _calc_inst_phase(self, sig, alpha):
        """Extract analytical signal through the Hilbert Transform."""
        analytic_signal = hilbert(sig)  # Apply Hilbert transform to each row
        if alpha is not None:
            assert -0.5 < alpha < 0.5, "`alpha` must be in between -0.5 and 0.5"
            real_part = np.array([filt6(row.real, alpha) for row in analytic_signal])
            imag_part = np.array([filt6(row.imag, alpha) for row in analytic_signal])
            analytic_signal = real_part + 1j * imag_part
        phase = np.unwrap(np.angle(analytic_signal))  # Compute angle between img and real
        if alpha is not None:
            phase = np.array([filt6(row, alpha) for row in phase])  # Filter phase
        return phase

    def calc_inst_freq(self, sig, t, order, alpha):
        """Extracts instantaneous frequency through the Hilbert Transform."""
        inst_phase = self._calc_inst_phase(sig, alpha=alpha)
        if order is False:
            inst_freqs = np.diff(inst_phase) / (2 * np.pi * (t[1] - t[0]))
            inst_freqs = np.concatenate((inst_freqs, inst_freqs[:, -1].reshape(inst_freqs[:, -1].shape[0], 1)), axis=1)
        else:
            inst_freqs = [pade6(row, t[1] - t[0]) / (2.0 * np.pi) for row in inst_phase]
        if alpha is None:
            return np.array(inst_freqs)
        else:
            return np.array([filt6(row, alpha) for row in inst_freqs])  # Filter freqs

    def show(self):
        plt.show()


def DataEMD(data:array, **kwargs):
    '''
    实现sEMG和IMU的数据模态分解

    args:
    data:数据
        kwargs:
            max_imf:最多的分解数目，默认值-1
            order : bool (default: False)
            Represents whether the finite difference scheme is low-order (1st order forward scheme) or high-order (6th order compact scheme). The default value is False (low-order)

            alpha : float (default: None)
            Filter intensity. Default value is None, which  is equivalent to `alpha` = 0.5, meaning that no filter is applied.
            The `alpha` values must be in between -0.5 (fully active) and 0.5
                (no filter).
     '''
    max_imf = kwargs.get("max_imf",-1)
    order = kwargs.get("order",None)
    alpha = kwargs.get("alpha",None)
    channel = data.shape[1]
    IMFS = []
    RES = []
    INSTANT_FREQ = []
    emd = EMD()
    vis = Visualisation()

    for i in range(channel):
        emd.emd(data[:,i], max_imf=max_imf)
        imfs, res = emd.get_imfs_and_residue()
        imfs_inst_freqs = vis.calc_inst_freq(imfs, np.arange(len(data)),order=order, alpha=alpha)
        # print(imfs.shape)
        IMFS.append(imfs)
        RES.append(res)
        INSTANT_FREQ.append(imfs_inst_freqs)

    return np.array(IMFS), np.array(RES), np.array(INSTANT_FREQ)


def DataEMDShow(IMFS, RES, INSTANT_FREQ):
    t = np.arange(IMFS.shape[1])
    fig = plt.figure(len(IMFS) *2)
    for i in range(len(IMFS)):
        ax1 = plt.subplot(len(IMFS), 2, 2*i+1)
        ax1.set_title("IMF-" + str(i+1), fontsize = 25)
        ax1.plot(t, IMFS[i])
        ax=plt.gca()
        x_major_locator=MultipleLocator(200)
        ax.xaxis.set_major_locator(x_major_locator)
        plt.xticks( fontsize = 20)  # 去x坐标刻度
        plt.yticks( fontsize = 20)  # 去y坐标刻度
        plt.xlim(left=0, right=len(t))

        ax2 = plt.subplot(len(INSTANT_FREQ), 2, 2*i+2)
        ax2.set_title("IFQ-" + str(i+1), fontsize = 25)
        ax2.plot(t, INSTANT_FREQ[i])
        ax=plt.gca()
        x_major_locator=MultipleLocator(200)
        ax.xaxis.set_major_locator(x_major_locator)
        plt.xticks( fontsize = 20)  # 去x坐标刻度
        plt.yticks( fontsize = 20)  # 去y坐标刻度
        plt.xlim(left=0, right=len(t))
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.6)
    

    plt.show()