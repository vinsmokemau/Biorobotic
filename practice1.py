import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Points of the polygon
x = (7 - 5) * np.random.random(1000) + 5
y = (4 - 2) * np.random.random(1000) + 2
x2 = (9 - 7) * np.random.random(1000) + 7
y2 = (4 - 2) * np.random.random(1000) + 2
x3 = (9 - 7) * np.random.random(1000) + 7
y3 = (6 - 4) * np.random.random(1000) + 4

# Range to move the vector between 0 to 359 degrees
pi_range = np.linspace(0, 2 * np.pi, 360, endpoint=False)

# Create a figure to plot
fig, ax = plt.subplots()

# Plot 3 squares to create the polygon
ax.scatter(x, y, marker='.', color='b')
ax.scatter(x2, y2, marker='.', color='b')
ax.scatter(x3, y3, marker='.', color='b')

# The start of the vector
xfixdata, yfixdata = 0, 0

# The final of the vector that is going to move depending on a circumference
xdata, ydata = None, None

# Store the data to plot
ln, = plt.plot([], [], 'r-', animated=True)

# Counter of the first quadrant angles
counter = [0]

# List to store the invalid angles
angles = []


def init():
    ax.set_xlim(-9.5, 9.5)
    ax.set_ylim(-9.5, 9.5)
    return ln,


def circle(phi):
    """Circle equation in polar range."""
    return np.array([9 * np.cos(phi), 9 * np.sin(phi)])


def update(frame):
    """Function to update the vector."""
    # Get the points of the circle depending on the frame
    xdata, ydata = circle(frame)
    # Add the new point
    ln.set_data([xfixdata, xdata], [yfixdata, ydata])
    # This conditional is to check the valid angles in the first quadrant
    if xdata >= 0 and ydata >= 0:
        # Get the equation of the vector's line
        coefficients = np.polyfit([xfixdata, xdata], [yfixdata, ydata], 1)
        polynomial = np.poly1d(coefficients)
        # Get the 50 points of the equation between 0 to 9
        x_axis = np.linspace(0, 9, 50)
        y_axis = polynomial(x_axis)
        # If one of the points is inside the polygon add the current angle to the invalid list
        for x_value, y_value in zip(x_axis, y_axis):
            if ((5 <= x_value <= 9) and (2 <= y_value <= 4)) or ((7 <= x_value <= 9) and (4 <= y_value <= 6)):
                angles.append(counter[0])
                break
        counter[0] += 1
    return ln,


ani = FuncAnimation(
    fig,
    update,
    interval=10,
    frames=pi_range,
    init_func=init,
    repeat=False,
    blit=True,
)

plt.show()

print(f'From {angles[0]}° to {angles[-1]}° are invalid angles to work.')

while True:
    loop = input('Do yo want to enter an angle to corroborate the work zone? [y/n]\n').lower()
    if loop == 'y':
        try:
            angle = int(input('Give me an angle between 0 and 359: '))
            if 0 <= angle <= 359:
                fig, ax = plt.subplots()
                ax.set_xlim(-9.5, 9.5)
                ax.set_ylim(-9.5, 9.5)
                ax.scatter(x, y, marker='.', color='b')
                ax.scatter(x2, y2, marker='.', color='b')
                ax.scatter(x3, y3, marker='.', color='b')
                x_position, y_position = circle(pi_range[angle])
                ax.plot([0, x_position], [0, y_position], 'r')
                plt.show()
            else:
                print('The number that you enter is out of range')
        except ValueError:
            print('The data you enter is not a integer')
        except:
            print('Something is wrong...')
    else:
        print('Bye, bye!')
        break
