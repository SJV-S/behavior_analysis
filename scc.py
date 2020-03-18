
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


def gen_data(start, num, cel, bounce):
    value = start
    a_list = []
    for i in range(num):
        value = value * cel
        a_list.append(value * (random.randrange(bounce, 100)/100))

    return a_list


def scc_format(entry, floor=False):
    if floor:
        if type(entry) == str or entry is None:
            return None
        elif entry <= 0:
            return None
        else:
            return 1/entry

    resp, time = entry
    if type(resp) == str or resp is None:
        return None
    if resp <= 0 or (1/time) > resp/time:
        return (1/time)*0.7
    else:
        return resp/time


def freq_calc(all_data):
    position, corrects, errors, record_floor = all_data
    same_length = len(position) == len(corrects) == len(errors) == len(record_floor)
    if same_length:

        record_floor_freq = list(map(lambda x: scc_format(x, floor=True), record_floor))
        correct_freq = list(map(scc_format, zip(corrects, record_floor)))
        error_freq = list(map(scc_format, zip(errors, record_floor)))

        return position, correct_freq, error_freq, record_floor_freq
    else:
        raise Warning("Arrays are not of same length. Check your data.")


def daily(start_date,
          PosCorErrRec=None,
          width=10, show=False,
          save_to=None,
          phase_lin=None,
          aimstars=None,
          title="",
          y_label="Count per Minute",
          cor_label="Correct freq",
          err_label="Error freq"):

    # Definition of a, b and c of the exponential function y = ab^(x/c).
    a = 0.001  # y-intercept.
    b = 2  # y-increase factor.
    c = 7  # x-increase per y-increase factor.
    angle = 34  # desired visual slope of the function graph, in degrees.
    xmin = 0  # x-axis minimum value.
    xmax = 140  # x-axis maximum value.
    ymin = 0.00069  # y-axis minimum value.
    ymax = 1000  # y-axis maximum value.
    x = np.arange(xmin, xmax)
    y = a * pow(b, x / c) # Calculate y-values for visual angle testing.
    font = "Arial"

    # Calculate and set height of the figure based on referenced width.
    height = width * np.tan(angle / 180 * np.pi) * np.log10(ymax / ymin) / (xmax - xmin) * c / np.log10(b)
    fig, ax = plt.subplots(figsize=(width, height))

    plt.subplots_adjust(left=0.15, right=0.85, bottom=0.15, top=0.85)  # Surround plot with more white space

    # Define axis ticks and labels
    left_y_ticks = [10**e for e in [np.log10(i) for i in [0.001, 0.005, 0.01, 0.05, 0.1, 1, 5, 10, 50, 100, 500, 1000]]]
    left_y_labels = ["0.001", "0.005", "0.01", "0.05", "0.1", "1", "5", "10", "50", "100", "500", "1000"]
    right_y_ticks = [1/m for m in [10/60, 15/60, 20/60, 30/60, 1, 2, 5, 10, 20, 60, 60*2, 60*4, 60*8, 60*16]]
    right_y_labels = ['10" sec', '15"', '20"', '30"', "1' min", "2'", "5'", "10'", "20'", "1 - h", "2 - h", "4 - h",
                         "8 - h", "16 - h"]
    if width < 8:
        bottom_x_inc = 14
        top_x_inc = 28
    else:
        bottom_x_inc = 7
        top_x_inc = 7
    bottom_x_ticks = np.arange(0, 141, bottom_x_inc)
    top_x_ticks = np.arange(0, 141, top_x_inc)

    start_date = pd.to_datetime(start_date)  # Convert to pandas datetime format.
    first_sunday = start_date - pd.Timedelta(start_date.dayofweek + 1, unit="D")  # Find last Sunday.
    dates = pd.date_range(first_sunday, periods=21, freq="W").strftime("%d-%m-%y")  # Get date labels for top x-axis.

    # Set up up top x-axis.
    ax2 = plt.twiny()
    ax2.set_xticks(top_x_ticks)
    ax2.set_xticklabels(dates, rotation=45, fontsize=9, fontname=font)
    ax2.tick_params(axis='both', which='both', length=0)
    plt.setp(ax2.xaxis.get_majorticklabels(), ha="left", rotation_mode="anchor")

    # Set up right y-axis.
    ax3 = plt.twinx()
    ax3.set_ylim(ymin, ymax)
    ax3.set_yscale("log")
    ax3.set_yticks(right_y_ticks)
    ax3.set_yticklabels(right_y_labels, fontsize=8, fontname=font)
    ax3.tick_params(axis='both', which='minor', length=0)

    # Move bottom x-axis down slightly for ax and remove bottom spine for ax2 and ax3.
    ax.spines["bottom"].set_position(("axes", -0.03))  # Move down.
    ax2.spines["bottom"].set_visible(False)  # Delete ax2 spine.
    ax3.spines["bottom"].set_visible(False)  # Delete ax3 spine.

    # Set up main axes: left y and bottom x.
    ax.set_yscale("log")
    ax.set_ylim(0.00069, 1000)
    ax.tick_params(axis='both', which='minor', length=0)
    ax.set_xlim(0, 140)
    ax.set_xticks(bottom_x_ticks)
    ax.set_xticklabels([str(tick) for tick in bottom_x_ticks], fontsize=9, fontname=font)
    ax.set_yticks(left_y_ticks)
    ax.set_yticklabels(left_y_labels, fontsize=9, fontname=font)

    # Draw grid lines.
    custom_grid_color = "turquoise"
    ax.grid(which="both", color=custom_grid_color, linewidth=0.3)
    for sun in [i for i in range(7, 141, 7)]:
        ax.axvline(sun, color=custom_grid_color, linewidth=1)
    for power in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
        ax.axhline(power, color=custom_grid_color, linewidth=1)

    # Color spines (the frame around the plot). The axes all have their own spines, so we have to color each.
    color = "teal"
    for position in ax.spines.keys():
        ax.spines[position].set_color(color)
        ax2.spines[position].set_color(color)
        ax3.spines[position].set_color(color)

    # Set axis labels and title
    ax.set_ylabel(y_label, fontname=font, fontsize=13)
    ax.set_xlabel("Successive Calendar Days", fontname=font, fontsize=13)
    plt.title(title)
    ax.text(0.05, 0.05, 'By SJV', transform=plt.gcf().transFigure, fontname=font, fontsize=7)

    # Calculate frequency based on count and record floor.
    if PosCorErrRec:
        position, correct_freq, error_freq, record_floor_freq = freq_calc(PosCorErrRec)

        ax.plot(position, correct_freq, "ko", markersize=3, label=cor_label)
        ax.plot(position, error_freq, "kx", markersize=5, label=err_label)
        ax.plot(position, record_floor_freq, marker="_", markersize=5, color="k", linestyle="", label="Record floor", markeredgewidth=3)
        # ax.plot(x, y, 'r', label="34 degree angle")  # Uncomment to test for a 34 degree visual angle.)

        if aimstars:
            for aim in aimstars:
                if type(aim) is not tuple:
                    raise Warning("Aimstar must be a list of tuples.")
                x_aim, y_aim = aim
                ax.plot(x_aim, y_aim, label="Aim", marker="*", markersize=9, color="firebrick", linestyle="")

        if phase_lin:
            for phase in phase_lin:
                if type(phase) is not tuple:
                    raise Warning("Phase_lin must be a list of tuples.")
                x_cor, y_cor, text = phase
                ax.axvline(x_cor, color="k", linestyle="--")
                ax.text(x_cor + 2, y_cor, text, fontname=font, bbox=dict(facecolor='white', edgecolor='black'))

        ax.legend(loc="upper right")

    if save_to:
        plt.savefig(save_to + "\\" + title)
    if show:
        plt.show()
    plt.close()
