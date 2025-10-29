import sys
import traceback

try:
    import agents, crew_setup, predictor
    crew = crew_setup.create_crew()
    model = predictor.load_model()
    print('CREW_OK', hasattr(crew, 'run'))
    print('MODEL_OK', hasattr(model, 'predict'))
    # quick call to ensure predict works on sample DataFrame
    import pandas as pd
    sample = pd.DataFrame([{
        'Distance_KM': 10.0,
        'Fuel_Consumption_L': 5.0,
        'Toll_Charges_INR': 50.0,
        'Weather_Impact': 'None',
        'Fuel_per_KM': 0.5,
        'Total_Cost_INR': 500.0
    }])
    preds = model.predict(sample)
    try:
        length = len(preds)
    except Exception:
        length = None
    print('PRED_OK', length)
except Exception:
    traceback.print_exc()
    sys.exit(2)
