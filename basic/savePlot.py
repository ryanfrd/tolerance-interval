import matplotlib.pyplot as plt

# Save the figure
# Provide a figure name (figname), and optionally width (w) and height (h) of the figure
# figname: string
# w: float
# h: float
def savePlot(figname,w=11,h=8):
    fig = plt.gcf()
    fig.set_size_inches(w,h)
    plt.savefig(figname + ".jpg", dpi = 600)
    plt.close()