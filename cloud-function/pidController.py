class PID_Controller:

    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.previous_error = 0
        self.integral = 0

    def feedback(self, process_value, dt):
        error = self.setpoint - process_value
        proportional_out = self.Kp * error
        self.integral += error * dt
        integral_out = self.Ki * self.integral

        if dt > 0:
            derivative = (error - self.previous_error) / dt
            derivative_out = self.Kd * derivative
        else:
            derivative_out = 0

        feedback = (
        proportional_out +
        integral_out +
        derivative_out
        )

        self.previous_error = error
        return feedback