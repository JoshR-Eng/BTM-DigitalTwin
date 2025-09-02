# Cloud/main.py
import functions_framework 
from recursiveLeastSquares import RLS

# RLS object persists between invocations as long as the container is warm
rls = RLS(forgetting_factor=0.995)

@functions_framework.http
def controller(request):
    """
    Receives a JSON file containing system measurements,
    returns updated internal resistance and state variables.
    """
    data = request.get_json(silent=True)
    if data is None:
        return "Invalid JSON", 400
    
    # Extract incoming variables
    T = data['temperature']           # current measured temperature
    T_prev = data['temperature_prev'] # previous measured temperature
    I = data['current']               # current draw [A]
    P_cooling = data['cooling_power'] # applied cooling power [W]
    dt = data['dt']                   # timestep [s]
    r = data['internal_resistance']   # current estimate of R
    p = data['p']                     # current covariance
    
    # Compute regression model 
    phi, y = rls.compute_regressors_power(
        new_temperature=T,
        prev_temperature=T_prev,
        cooling_power=P_cooling,
        current=I,
        dt=dt
    )
    
    # Run RLS update
    minimised_function = rls.update(
        y= y,
        phi=phi,
        r=r,
        p=p
    )

    improved_r = minimised_function['r']
    improved_p = minimised_function['p']

    # Package response back to client
    response = {
        'time_sent': data['time_sent'],  # echo back timestamp for syncing
        'temperature_prev': T,           # send back new T as next-step T_prev
        'internal_resistance': improved_r,
        'p': improved_p,
        'innovation': minimised_function['e']
    }

    return response
