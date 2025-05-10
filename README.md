# Tolerance Interval Constructor

A simple application to construct tolerance intervals from measurement data based on desired confidence and proportion of interest. Specification limits may also be provided and plotted with the data.

## Inputs
The operator supplies a .csv or .xlsx file having measurement data of length n in a single column. The column should have a header with the measurment units.

The operator specifies:
1) the alpha level, α, to determine the level of confidence (1-α) of the tolerance interval
2) the proportion, p, of the population to calculate a tolerance interval around
3) Whether they are interested in a one-sided upper, one-sided lower, or two sided tolerance
4) whether there are any specification limits, and if there are, what those limts are

## Outputs
The script will output, and save at the operators discretion:
1) A plot of the tolerance interval with any specified limits
2) A summary of the tolerance interval data in a .csv file