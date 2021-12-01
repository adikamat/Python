import os, sys
import bz2
import base64
import traceback
import fractions
import struct
import string
import io
import StringIO
from abc import ABCMeta, abstractmethod


class ImpactSpeedCalc:
    __metaclass__ = ABCMeta

    # Brake Model Parameters
    #            ^
    # DECEL_MAX  |        ______________________
    #            |       /|
    #            |      / |
    #            |     /  |
    #         0  |____/___|_______________________
    #                TD   TR
    #    TD = DEAD_TIME
    #    TR = RAMP_TIME

    DEAD_TIME = 0.1  # seconds
    RAMP_TIME = 0.3  # seconds
    DECEL = 10.0  # m/s^2

    @abstractmethod
    def calc_impact_speed(self, TTC, initial_velocity, target_velocity):
        """

        :param TTC: Time to collision in seconds
        :param initial_velocity: Initial velocity of Ego in kph
        :param target_velocity: Velocity of target in kph
        :return: Impact velocity in kph (float)
        """
        pass


class LinearMotionIterativeCalc(ImpactSpeedCalc):

    def calc_impact_speed(self, TTC, initial_velocity, target_velocity):

        TIME_STEP = 0.001  # seconds

        # Convert to m/s
        test_speed_m_s = initial_velocity * 5 / 18
        tgt_speed_m_s = target_velocity * 5 / 18

        s_dead = test_speed_m_s * self.DEAD_TIME
        s_total = test_speed_m_s * TTC

        t = self.DEAD_TIME
        s_t = s_dead
        v_t = test_speed_m_s
        velocity = []
        time = []
        while s_t < s_total and v_t > 0:
            if t > self.RAMP_TIME + self.DEAD_TIME:
                # Constant Deceleration Phase
                u = v_t
                v_t -= self.DECEL * TIME_STEP
                s_t += (u * TIME_STEP) - (self.DECEL * TIME_STEP ** 2 / 2)
            else:
                # Ramp Phase
                decel_t = self.DECEL / self.RAMP_TIME * (t - self.DEAD_TIME)
                u = v_t
                v_t -= decel_t * TIME_STEP
                s_t += (u * TIME_STEP) - (decel_t * TIME_STEP ** 2 / 2)

            time.append(t)
            s_total = s_total + (tgt_speed_m_s * TIME_STEP)
            t += TIME_STEP
            velocity.append(v_t)

        # print t, s_t, s_total, v_t
        if v_t > 0:
            v_impact = v_t * 18 / 5  # kph
        elif s_t < s_total:
            v_impact = 0

        # plt.figure()
        # plt.plot(time, velocity)
        # plt.grid()
        # plt.show()

        # return [v_impact, s_t, s_total, v_t, u]
        return v_impact


class LinearMotionFormulaeCalc(ImpactSpeedCalc):

    def calc_impact_speed(self, TTC, initial_velocity, target_velocity):
        v_impact = 0
        raise NotImplementedError("Function not Implemented")


class TurningMotionCalc(ImpactSpeedCalc):

    def calc_impact_speed(self, TTC, initial_velocity, target_velocity):
        v_impact = 0
        raise NotImplementedError("Function not Implemented")


class BrakingMotionCalc(ImpactSpeedCalc):

    def calc_impact_speed(self, TTC, initial_velocity, target_velocity):
        v_impact = 0
        raise NotImplementedError("Function not Implemented")
