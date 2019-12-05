import numpy as np
import math

# Constants
DEAD_TIME = 0.1  # seconds
RAMP_TIME = 0.3  # seconds
DECEL_MAX = 10.0  # m/s^2


def calculate_impact_velocity(TTC, initial_velocity):

    # Calculate distance of GVT (object/car in front)
    s_obj = TTC * initial_velocity

    # Calculate distance covered in deceleration profile dead-time
    s_dead = DEAD_TIME * initial_velocity

    # Check if collision occurs in dead time
    if s_dead > s_obj:
        print "Collision occured in dead time"
        v_impact = initial_velocity

    else:

        # Collision has not occurred yet ( after dead time)
        # Calculate distance covered at end of ramp time
        s_ramp = (s_dead + (DECEL_MAX * DEAD_TIME ** 2 / 2)) + \
                 (initial_velocity * RAMP_TIME) - \
                 (DECEL_MAX / 6 / RAMP_TIME *
                  ((DEAD_TIME + RAMP_TIME) ** 3 - DEAD_TIME ** 3))

        # Check if collision has occurred in ramp phase
        if s_ramp > s_obj:
            print "Collision occurs in ramp phase"

            # Find the time at which collision occurs
            a = (DECEL_MAX / 6 / RAMP_TIME)
            b = 0
            c = -(initial_velocity + (DECEL_MAX * DEAD_TIME**2 / 2 / RAMP_TIME))
            d = -(s_dead - s_obj - (initial_velocity * DEAD_TIME) -
                  (DECEL_MAX * DEAD_TIME**3 / 3 / RAMP_TIME))
            eqn_roots = np.roots([a, b, c, d])
            print "Roots for cubic equation", eqn_roots

            # Get the roots that lie between dead time and ramp time
            t_collision = None
            for r in eqn_roots:
                if DEAD_TIME <= r <= RAMP_TIME + DEAD_TIME:
                    t_collision = r

            if t_collision is None:
                print "Unable to find roots for cubic equation that lie between dead time and ramp time"
                # Assuming max value in ramp phase
                # This will give less impact velocity than actual
                t_collision = DEAD_TIME + RAMP_TIME

            # print "Collision Time = ", t_collision
            # print (DECEL_MAX / 2 / RAMP_TIME * (t_collision ** 2 - DEAD_TIME ** 2))
            # print initial_velocity

            # Calculate the velocity at the time of impact
            v_impact = initial_velocity - (DECEL_MAX / 2 / RAMP_TIME *
                                           (t_collision ** 2 - DEAD_TIME ** 2))

        else:

            # Collision does not occur in ramp phase
            # Calculate velocity of VUT (car in motion) at end of ramp phase
            v_ramp = initial_velocity - (DECEL_MAX / 2 / RAMP_TIME *
                                         ((RAMP_TIME + DEAD_TIME) ** 2 - DEAD_TIME ** 2))

            # Calculate time of collision
            discriminant = (v_ramp / DECEL_MAX)**2 + (2 * (s_ramp - s_obj) / DECEL_MAX)
            if discriminant >= 0.0:
                b = ((v_ramp / DECEL_MAX) + DEAD_TIME + RAMP_TIME)
                t_collision = b - math.sqrt(discriminant)
                if t_collision < 0.0:
                    t_collision = b + math.sqrt(discriminant)

                print "Discriminant", discriminant, " Roots =", b + math.sqrt(discriminant), b - math.sqrt(discriminant)

                # Calculate final velocity at time = TTC
                # If final velocity is 0 or negative, no collision occured
                # Else, collision occured and impact velocity is final velocity
                # v_final = v_ramp - (DECEL_MAX * (TTC - RAMP_TIME - DEAD_TIME))
                v_final = v_ramp - (DECEL_MAX * (t_collision - RAMP_TIME - DEAD_TIME))

                if v_final <= 0.0:
                    print "No Collision. Vehicle comes to a stop at t =", \
                        (v_ramp / DECEL_MAX) + DEAD_TIME + RAMP_TIME, "sec"
                    v_impact = 0.0
                    t_stop = (v_ramp / DECEL_MAX) + DEAD_TIME + RAMP_TIME
                    s_t = s_ramp - (v_ramp * (DEAD_TIME + RAMP_TIME)) - (DECEL_MAX * (DEAD_TIME + RAMP_TIME)**2 / 2) + \
                        (v_ramp + (DECEL_MAX * (DEAD_TIME + RAMP_TIME))) * t_stop - \
                        (DECEL_MAX * t_stop**2 / 2)
                    print "Distance traveled =", s_t, " Object Distance =", s_obj, " final velocity", v_final
                else:
                    print "Collision occurred in constant deceleration phase at t=", t_collision
                    v_impact = v_final

            else:
                print "No Collision. Vehicle comes to a stop at t =", (v_ramp / DECEL_MAX) + DEAD_TIME + RAMP_TIME, \
                    "sec"
                v_impact = 0.0
                t_stop = (v_ramp / DECEL_MAX) + DEAD_TIME + RAMP_TIME

                s_t = s_ramp - (v_ramp * (DEAD_TIME + RAMP_TIME)) - (DECEL_MAX * (DEAD_TIME + RAMP_TIME) ** 2 / 2) + \
                    (v_ramp + (DECEL_MAX * (DEAD_TIME + RAMP_TIME))) * t_stop - \
                    (DECEL_MAX * t_stop ** 2 / 2)
                print "Distance traveled =", s_t, " Object Distance =", s_obj

    return v_impact


if __name__ == "__main__":

    # print calculate_impact_velocity(0.30, 10.0 * 5 / 18) * 18 / 5, "km/h"
    print calculate_impact_velocity(0.8725, 50.0 * 5 / 18) * 18 / 5, 'kph'
    print calculate_impact_velocity(0.38, 10.0 * 5 / 18) * 18 / 5, 'kph'
    print calculate_impact_velocity(0.3513, 10.0 * 5 / 18) * 18 / 5, 'kph'
    print calculate_impact_velocity(0.65, 10.0 * 5 / 18) * 18 / 5, 'kph'

