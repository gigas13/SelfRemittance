# SelfRemittance

STREAMILIT DASHBOARD

script to pick out a combintation of items (invoices) that matches a target number (payment)
displayed through python library "streamlit"
receives in input:
  2 columns ['Invoice', 'Value'] dataframe from a csv file;
  1 target value (a theoretical payment)
Check out 1 combination of values that match the target
Display the succsesfull dataframe (a subset of the original one)

# The performances drop significantly  proportionally to the length of the dataframe
