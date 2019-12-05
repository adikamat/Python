import matplotlib.pyplot as plt

# Constants
DEAD_TIME = 0.1  # seconds
RAMP_TIME = 0.3  # seconds
DECEL_MAX = 10  # m/s^2

initial_velocity = 10.0 * 5 / 18  # Speed in kmph converted to m/s
TTC = 0.35  # time to collide
timestamp = [x * 0.001 for x in range(0, 500)]

# Calculate distance of GVT (object/car in front)
s_obj = TTC * initial_velocity

# Calculate distance covered in deceleration profile dead-time
s_dead = DEAD_TIME * initial_velocity

s_ramp = (s_dead + (DECEL_MAX * DEAD_TIME ** 2 / 2)) + \
         (initial_velocity * RAMP_TIME) - \
         (DECEL_MAX / 6 / RAMP_TIME * ((DEAD_TIME + RAMP_TIME) ** 3 - DEAD_TIME ** 3))

v_ramp = initial_velocity - (DECEL_MAX / 2 / RAMP_TIME *
                             ((RAMP_TIME + DEAD_TIME) ** 2 - DEAD_TIME ** 2))

distance_covered = []
for t in timestamp:
    s_t = s_ramp - (v_ramp * (DEAD_TIME + RAMP_TIME)) - (DECEL_MAX * (DEAD_TIME + RAMP_TIME) ** 2 / 2) + \
          (v_ramp + (DECEL_MAX * (DEAD_TIME + RAMP_TIME))) * t - \
          (DECEL_MAX * t ** 2 / 2)

    distance_covered.append(s_t)


plt.figure()
plt.plot(timestamp, distance_covered)
plt.show()
