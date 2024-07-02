import warnings

# Ignore specific FutureWarning from plotly express
warnings.filterwarnings("ignore", category=FutureWarning, message="When grouping with a length-1 list-like, you will need to pass a length-1 tuple to get_group in a future version of pandas")
