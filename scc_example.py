
import scc
import random

# Let's generate some data.
# Loop structure: [(base * slope ** exp) * bounce for exp in range(data_points)]
cor_cond_1 = [(30 * 1.01 ** exp) * random.randrange(50, 100)/100 for exp in range(20)]
cor_cond_2 = [(30 * 1.2 ** exp) * random.randrange(50, 100)/100 for exp in range(20)]
err_cond_1 = [(30 * 1.01 ** exp) * random.randrange(50, 100)/100 for exp in range(20)]
err_cond_2 = [(30 * 0.8 ** exp) * random.randrange(50, 100)/100 for exp in range(20)]

# Join data
corrects = cor_cond_1 + cor_cond_2
errors = err_cond_1 + err_cond_2

record_floor = len(corrects) * [2]  # Generate record floor
position = [*range(1, len(corrects) + 1)]  # Generate x coordinates. Remember to start at 1.

# The length of these arrays need to be the same! Pad shorter arrays with None.
# If errors are not counted, pad error array with None values. For example: errors = [None] * len(corrects)
data = scc.freq_calc([position, corrects, errors, record_floor])  # Calculate frequencies based on count and time

scc.daily("2020-03-14",  # Start date. The scc will select the closest Sunday before this date.
          width=9,  # Modify the size of your chart. Height is automatically calculated.
          PosCorErrRec=data,  # Your data. PosCorErrRec stands for Position-Corrects-Errors-Record floor.
          show=True,  # Display graph. There is also a save_to_file option.
          phase_lin=[(20, 600, "Intervention")],  # Add phase lines as list of tuples. Supply the x and y coordinates and text.
          aimstars=[(40, 400)],  # Add aim stars also as list of tuples. Supply the x and y coordinates of each aim.
          title="example",  # Add title to your chart.
          save_to=r"C:\Users\Johan\Desktop\Personal Quant",  # Directory to save your chart.
          legend=True)  # Add legend


