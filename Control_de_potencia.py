import requests
import tinytuya
import time
import itertools
from secrets import *
device_list = [
    {"entity_id": "switch.switch_entretenimiento", "power":18, "status": None, "beingControlled": False},
    {"entity_id": "switch.cocina_switch_2", "power":20, "status": None, "beingControlled": False},
    {"entity_id": "switch.habitacion_2", "power":20, "status": None, "beingControlled": False},
    {"entity_id": "switch.dormitorio", "power":27, "status": None, "beingControlled": False},
    {"entity_id": "switch.switch_oficina", "power":43, "status": None, "beingControlled": False},
    {"entity_id": "switch.cocina_switch_1", "power":53, "status": None, "beingControlled": False},
    {"entity_id": "switch.habitacion_1", "power":75, "status": None, "beingControlled": False},
    {"entity_id": "switch.sala", "power":35, "status": None, "beingControlled": False},
    {"entity_id": "switch.comedor", "power":31, "status": None, "beingControlled": False},
    {"entity_id": "light.pasillo1", "power":10, "status": None, "beingControlled": False},
    {"entity_id": "light.pasillo9", "power":10, "status": None, "beingControlled": False},
    {"entity_id": "switch.hall", "power":12, "status": None, "beingControlled": False},
    {"entity_id": "switch.lavado", "power":30, "status": None, "beingControlled": False},
    {"entity_id": "light.lampara", "power":10, "status": None, "beingControlled": False}
]
#variables de requests

time.sleep(5)
def ask_for_device(entity_id):
    """Consulta el estado de un interruptor en Home Assistant y devuelve True si está encendido, False si está apagado. o None si no lo encuentra"""
    url = f"{BASE_URL}/states/{entity_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        state = response.json().get("state")
        if state == "on":
            return True
        elif state == "off":
            return False
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
def toggle_light(entity_id, action):
    """Enciende o apaga una luz en Home Assistant."""
    url = f"{BASE_URL}/services/light/{action}"
    data = {"entity_id": entity_id}
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print(f"La luz {entity_id} ha En estado {action}.")
    else:
        print(f"Error {response.status_code}: {response.text}")
        
def toggle_switch(entity_id, action):
    """Enciende o apaga un interruptor en Home Assistant."""
    url = f"{BASE_URL}/services/switch/{action}"
    myobj= '{"entity_id": "'+entity_id+'"}'
    response = requests.post(url, headers=HEADERS, data=myobj)
    if response.status_code == 200:
        print(f"El interruptor {entity_id} en estado {action}.")
    else:
        print(f"Error {response.status_code}: {response.text}")

def update_status(device_list):
    """
    Actualiza el campo "status" en la lista de diccionarios de dispositivos de acuerdo con el estado real de cada dispositivo.
    
    Args:
        device_list (list): Una lista de diccionarios que contiene información sobre dispositivos con claves "entity_id" y "power".
    
    Returns:
        list: La lista de diccionarios actualizada con el campo "status".
    """
    for device in device_list:
        entity_id = device["entity_id"]
        status = ask_for_device(entity_id)
        device["status"] = status if status is not None else None
    
    return device_list



# variables de tinytuya



d = tinytuya.OutletDevice(
    dev_id=DEV_ID,
    address=TUYAIP,    # Or set to 'Auto' to auto-discover IP address
    local_key=LOCALKEY,# 
    version=3.4)



def parse_Power_Status_old(data):
    """
    Parse the data from d.status() to check its validity and extract specific values.
    # Test the function
    data1 = {'protocol': 4, 't': 1698552953, 'data': {'dps': {'101': 480}}, 'dps': {'101': 480}}
    data2 = {'dps': {'1': 618, '2': 0, '101': 298, '102': 'FORWARD'}}
    data3 = {'dps': {'1': 618, '2': 0, '101': 297, '102': 'REVERSE'}}

    print(parse_status(data1))  # (False, None, None)
    print(parse_status(data2))  # (True, 298, 'FORWARD')
    print(parse_status(data3))  # (True, 297, 'REVERSE')
    
    Parameters:
    - data (dict): Dictionary output from d.status()
    
    Returns:
    - dep (bool): True if the data is valid, else False
    - power (int or None): Integer value from the key "101" if present and valid, else None
    - cad (str or None): String value from the key "102" if present and valid (either 'FORWARD' or 'REVERSE'), else None
    """
    # Initial values
    dep = False
    power = None
    cad = None
    
    # Check if data is a dictionary
    if not isinstance(data, dict):
        return dep, power, cad
    
    # Check if the key 'dps' exists and its structure
    if 'dps' in data and isinstance(data['dps'], dict):
        # Check for keys "101" and "102"
        if '101' in data['dps'] and '102' in data['dps']:
            # Check the data type of the values for the keys
            if isinstance(data['dps']['101'], int) and data['dps']['101'] >= 0:
                if data['dps']['102'] in ['FORWARD', 'REVERSE']:
                    dep = True
                    power = data['dps']['101']
                    cad = data['dps']['102']
    if cad is None:
        print(data)
    return dep, power, cad

def parse_Power_Status(data):
    """
    Parse the data from d.status() to check its validity and extract specific values.
    
    Parameters:
    - data (dict): Dictionary output from d.status()
    
    Returns:
    - dep (bool): True if the data is valid, else False
    - power (int or None): Integer value from the key "101" if present and valid, else None
    - cad (str or None): String value from the key "102" if present and valid (either 'FORWARD' or 'REVERSE'), else None
    - error (bool): True if there's an "Error" key in the dictionary, else False
    """
    # Initial values
    dep = False
    power = None
    cad = None
    error = False
    
    # Check if data is a dictionary
    if not isinstance(data, dict):
        return dep, power, cad, error
    
    # Check for "Error" key
    if "Error" in data:
        error = True
        return dep, power, cad, error
    
    # Check if the key 'dps' exists and its structure
    if 'dps' in data and isinstance(data['dps'], dict):
        # Check for keys "101" and "102"
        if '101' in data['dps'] and '102' in data['dps']:
            # Check the data type of the values for the keys
            if isinstance(data['dps']['101'], int) and data['dps']['101'] >= 0:
                if data['dps']['102'] in ['FORWARD', 'REVERSE']:
                    dep = True
                    power = data['dps']['101']
                    cad = data['dps']['102']
    
    return dep, power, cad, error


#Variables optimización
POWER_OPT_ERROR=2
NEGHISTERESIS=3
POSHISTERESIS=7
CICLOS_ACT=5

def CalculatePower(device_list,target_power, max_error=0,estado=False,beingControlled=False):
    """CalculatePower: calcula que dispositivos deben encenderse para lograr una potencia adecuada, 
        Si se usan las banderas por defecto
        estado=False,beingControlled=False
        Lo calcula sobre los dispositivos apagados que no estan siendo controlados útil cuando se quieren encender para consumir
        Se se usan con las banderas:
        estado=True,beingControlled=True
        Lo calcula sobre los dispositivos que fueron encendidos por el control y estan encendidos, útil cuando se quiere calcular que apagar.

    Args:
        device_list (list):lista de diccionarios
        target_power (int): potencia objetivo
        max_error (int, optional): _description_. Defaults to 0.
        estado (bool, optional): _description_. Defaults to False.
        beingControlled (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    if target_power <= 0:
        return [], 0, 0

    # Filtra los dispositivos con status  y power > 0
    filter_devices = [device for device in device_list if device["status"] == estado and device["power"] > 0 and device["beingControlled"] == beingControlled]

    # Si la potencia de entrada es mayor o igual a la suma de todas las potencias, retorna todos los dispositivos
    total_power_all = sum(device["power"] for device in filter_devices)
    if target_power >= total_power_all:
        return [device["entity_id"] for device in filter_devices], total_power_all, abs(target_power - total_power_all)

    # Encuentra todas las combinaciones posibles de dispositivos
    combinations = []
    for r in range(1, len(filter_devices) + 1):
        combinations.extend(itertools.combinations(filter_devices, r))

    # Inicializa variables para mantener el mejor resultado encontrado
    best_combination = None
    closest_power = float("100000")

    # Encuentra la combinación más cercana al target_power
    for combo in combinations:
        total_power = sum(device["power"] for device in combo)
        power_error = abs(target_power - total_power)
        if power_error <= max_error:
            return [device["entity_id"] for device in combo], total_power, power_error
        
        if power_error < closest_power:
            #print("Mejor encontrado: ",best_combination,"\npower_error:",power_error,"< a closest_power:",closest_power,"total_power->",total_power)
            closest_power = power_error
            best_combination = combo
            
    if best_combination:
        selected_devices = [device["entity_id"] for device in best_combination]
        total_power_selected = sum(device["power"] for device in best_combination)
        power_error = abs(target_power - total_power_selected)
        return selected_devices, total_power_selected, power_error
    else:
        return [], 0, 0

def IsbeingControlled(device_list):
    for device in device_list:
        if device["beingControlled"]:
            return True
    return False

updated_device_list = update_status(device_list)
time.sleep(1)
# Imprime la lista actualizada
for device in updated_device_list:
    print(f"Entity ID: {device['entity_id']}, Power: {device['power']}, Status: {device['status']}")
cont=0
while True:
    dep, power, cad,ParseError = parse_Power_Status(d.status())
    if ParseError:
        print("Se detecta Error en el dispositivo. Reiniciando")
        toggle_switch("switch.1001798c1b", "turn_off")
        time.sleep(1)
        toggle_switch("switch.1001798c1b", "turn_on")
        time.sleep(30)
        continue
        
    if not dep: # Si la salida del dispositivo es válida
        #    print("\rPotencia:\t {}W, En dirección:\t {}".format(power, cad), end='', flush=True)
        #else:
        print("\rno se detecta trama válida, reintentando\t\t     ", end='', flush=True)
        time.sleep(1)
        continue
        
    if cad=='REVERSE' and power>NEGHISTERESIS:#
        print("")
        print("Se toma accion de control por inyección")
        target_power = power
        max_error = POWER_OPT_ERROR  # Puedes ajustar este valor según tus necesidades
        start_time = time.time()
        updated_device_list = update_status(updated_device_list)
        selected_devices, total_power, power_error = CalculatePower(updated_device_list,target_power, max_error)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Dispositivos seleccionados para igualar la potencia:", selected_devices)
        print("Potencia total: ", total_power,"Error de potencia: ", power_error,"Tiempo de ejecución: ", elapsed_time, "segundos")
        # Actualiza el estado de los dispositivos en la lista
        # Obtener la lista de dispositivos a encender
        # Bucle para encender los dispositivos
        for entity_id in selected_devices:
            # Determinar si el dispositivo es una luz o un interruptor
            is_light = entity_id.startswith("light.")
            is_switch = entity_id.startswith("switch.")
            if is_light:
                toggle_light(entity_id, "turn_on")
            elif is_switch:
                toggle_switch(entity_id, "turn_on")
            else:
                print(f"El dispositivo {entity_id} no es una luz ni un interruptor y no se puede encender.")
            # Actualizar la bandera "beingControlled" en el diccionario correspondiente
            for device in updated_device_list:
                if device["entity_id"] == entity_id:
                    device["beingControlled"] = True
                    break  # Una vez actualizado, podemos salir del bucle
        time.sleep(1)
        updated_device_list = update_status(updated_device_list)
    if cad =='FORWARD' and power>POSHISTERESIS and IsbeingControlled(updated_device_list):
        target_power = power
        max_error = POWER_OPT_ERROR  # Puedes ajustar este valor según tus necesidades
        start_time = time.time()
        selected_devices, total_power, power_error = CalculatePower(updated_device_list, target_power, max_error, estado=True, beingControlled=True)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if len(selected_devices) == 0:
            print("Algo raro pasa no deberia entrar acá")
        else:
            print("")
            print("Se toma accion de control, se apagan dispositivos encendidos por este control")
            print("Dispositivos seleccionados para igualar la potencia:", selected_devices)
            print("Potencia total: ", total_power,"Error de potencia: ", power_error,"Tiempo de ejecución: ", elapsed_time, "segundos")
        # Actualiza el estado de los dispositivos en la lista
        # Obtener la lista de dispositivos a encender
        # Bucle para encender los dispositivos
        for entity_id in selected_devices:
            # Determinar si el dispositivo es una luz o un interruptor
            is_light = entity_id.startswith("light.")
            is_switch = entity_id.startswith("switch.")
            if is_light:
                toggle_light(entity_id, "turn_off")
            elif is_switch:
                toggle_switch(entity_id, "turn_off")
            else:
                print(f"El dispositivo {entity_id} no es una luz ni un interruptor y no se puede encender.")
            # Actualizar la bandera "beingControlled" en el diccionario correspondiente
            for device in updated_device_list:
                if device["entity_id"] == entity_id:
                    device["beingControlled"] = False
                    break  # Una vez actualizado, podemos salir del bucle
        time.sleep(1)
        updated_device_list = update_status(updated_device_list)
    time.sleep(1)
    cont=cont+1
    if cont>=CICLOS_ACT:
        updated_device_list = update_status(updated_device_list)
        cont=0
        











# Ejemplo de uso
target_power = 23
max_error = 1  # Puedes ajustar este valor según tus necesidades
start_time = time.time()
selected_devices, total_power, power_error = CalculatePower(target_power, max_error)
end_time = time.time()
elapsed_time = end_time - start_time
print("Dispositivos seleccionados para igualar la potencia:", selected_devices)
print("Potencia total:", total_power)
print("Error de potencia:", power_error)
print("Tiempo de ejecución:", elapsed_time, "segundos")

















"""
import matplotlib.pyplot as plt

# Define el rango de potencia solicitada de 0 a 400
potencia_solicitada = list(range(361))

# Calcula el error para cada potencia solicitada y almacénalo en una lista
errores = []
for power in potencia_solicitada:
    _, _, error = CalculatePower(power, max_error=0)
    errores.append(error)

# Crea la gráfica
plt.figure(figsize=(10, 6))
plt.plot(potencia_solicitada, errores, marker='o', linestyle='-')
plt.title('Error vs Potencia Solicitada')
plt.xlabel('Potencia Solicitada')
plt.ylabel('Error')
plt.grid(True)

# Muestra la gráfica
plt.show()
"""





"""

quiero una funcion llamada CalculatePower que me retone a solicitud el entity_id de los dispositivos que tienen asociado el Status False,
es decir los que no están encendidos ya, cuya suma en key "Power" sea lo mas cercana posible al valor de entrada de la funcion. es decir

si entro 
CalculatePower(120)
me debe retornar una lista con los entity_id de los dispositivos a ser encendidos para igualar la potencia de entrada a la función, no necesariamente debe ser la misma lo ideal es que si no es igual este lo mas cercana posible
la lista de dispositivos se ve así, puedes usar alguna libreria que consideres para hacer la optimización

device_list = [
    {"entity_id": "switch.switch_entretenimiento", "power": 18, "status": None, "beingControlled": False},
    {"entity_id": "switch.cocina_switch_2", "power": 20, "status": None, "beingControlled": False},
    {"entity_id": "switch.habitacion_2", "power": 20, "status": None, "beingControlled": False},
    {"entity_id": "switch.dormitorio", "power": 27, "status": None, "beingControlled": False},
    {"entity_id": "switch.switch_oficina", "power": 43, "status": None, "beingControlled": False},
    {"entity_id": "switch.cocina_switch_1", "power": 53, "status": None, "beingControlled": False},
    {"entity_id": "switch.habitacion_1", "power": 75, "status": None, "beingControlled": False},
    {"entity_id": "switch.sala", "power": 35, "status": None, "beingControlled": False},
    {"entity_id": "switch.comedor", "power": 31, "status": None, "beingControlled": False},
    {"entity_id": "light.pasillo1", "power": 10, "status": None, "beingControlled": False},
    {"entity_id": "light.pasillo9", "power": 10, "status": None, "beingControlled": False},
    {"entity_id": "switch.hall", "power": 12, "status": None, "beingControlled": False},
    {"entity_id": "switch.lavado", "power": 30, "status": None, "beingControlled": False},
    {"entity_id": "light.lampara", "power": 10, "status": None, "beingControlled": False}
]

"""
