import matplotlib.pyplot as plt

DECEL = 10.0  # m/s^2
DEAD_TIME = 0.1  # seconds
RAMP_TIME = 0.3  # seconds
TIME_STEP = 0.001  # seconds


def calculate_impact_velocity(ttc_time, test_speed):
    # Convert to m/s
    test_speed_m_s = test_speed * 5 / 18
    
    s_dead = test_speed_m_s * DEAD_TIME
    s_total = test_speed_m_s * ttc_time
    
    t = DEAD_TIME
    s_t = s_dead
    v_t = test_speed_m_s
    velocity = []
    time = []
    while s_t < s_total and v_t > 0:
        if t > RAMP_TIME + DEAD_TIME:
            # Constant Deceleration Phase
            u = v_t
            v_t -= DECEL * TIME_STEP
            s_t += (u * TIME_STEP) - (DECEL * TIME_STEP ** 2 / 2)
        else:
            # Ramp Phase
            decel_t = DECEL / RAMP_TIME * (t - DEAD_TIME)
            u = v_t
            v_t -= decel_t * TIME_STEP
            s_t += (u * TIME_STEP) - (decel_t * TIME_STEP ** 2 / 2)

        time.append(t)
        t += TIME_STEP
        velocity.append(v_t)

    # print t, s_t, s_total, v_t
    if v_t > 0:
        v_impact = v_t
    elif s_t < s_total:
        v_impact = 0

    # plt.figure()
    # plt.plot(time, velocity)
    # plt.grid()
    # plt.show()
        
    # return [v_impact, s_t, s_total, v_t, u]
    return v_impact
    
    
if __name__ == "__main__":
    print calculate_impact_velocity(0.8725, 50.0) * 18 / 5, 'kph'
    print calculate_impact_velocity(0.38, 10.0) * 18 / 5, 'kph'
    print calculate_impact_velocity(0.3513, 10.0) * 18 / 5, 'kph'
    print calculate_impact_velocity(0.65, 10.0) * 18 / 5, 'kph'
