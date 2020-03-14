
import scc
import numpy as np

# First, let's generate some data.
# Arguments: initial value, number of data points, cel slope, variability as n-100%)
cor_cond_1 = scc.gen_data(5, 30, 1, 40)
cor_cond_2 = scc.gen_data(5, 20, 1.2, 40)
corrects = cor_cond_1 + cor_cond_2

err_cond_1 = scc.gen_data(5, 30, 1, 40)
err_cond_2 = scc.gen_data(5, 20, 0.8, 40)
errors = err_cond_1 + err_cond_2

minutes = 1
position = np.arange(1, len(corrects) + 1)   # Generate x coordinates. Remember to start at 1.
record_floor = [minutes] * len(corrects)  # Generate record floor

# The length of these arrays need to the the same! Pad shorter arrays with None.
# If errors are not counted, pad error array with None values. For example: errors = [None] * len(corrects)
data = [position, corrects, errors, record_floor]

scc.daily("2020-03-14",  # Start date. The scc will select the closest Sunday before this date.
          width=10,  # Modify the size of your chart. Height is automatically calculated.
          PosCorErrRec=data,  # Your data. PosCorErrRec stands for Position-Corrects-Errors-Record floor.
          show=True,  # Display graph. There is also a save_to_file option.
          phase_lin=[(30, 600, "behaviorist magic")],  # Add phase lines as list of tuples. Supply the x and y coordinates and text.
          aimstars=[(50, 150)],  # Add aim stars also as list of tuples. Supply the x and y coordinates of each aim.
          title="example_chart",  # Add title to your chart.
          save_to=r"C:\Users\Johan\Desktop\Personal Quant")  # Directory to save your chart.




