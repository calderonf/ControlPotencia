# Control de Potencia para Home Assistant

Este repositorio contiene un script para Home Assistant que permite controlar la potencia en tu hogar utilizando un medidor de potencia bidireccional de Tuya.

### Características

- Consulta el estado de interruptores y luces en Home Assistant.
- Enciende o apaga dispositivos en Home Assistant para mantener un cierto nivel de potencia.
- Utiliza un medidor de potencia bidireccional de Tuya para obtener lecturas de potencia.
- Optimiza la potencia consumida encendiendo o apagando dispositivos según la necesidad.

### ¿Cómo funciona?

El script se conecta a Home Assistant y al medidor de potencia bidireccional de Tuya para obtener lecturas de potencia en tiempo real. Si detecta una desviación en la potencia deseada, selecciona qué dispositivos encender o apagar para acercarse lo más posible al objetivo.

### Uso

1. Configura las credenciales y detalles del medidor de potencia bidireccional de Tuya en el archivo `secrets.py`.
2. Asegúrate de tener una lista de dispositivos con su potencia nominal, entidad y estado en `device_list`. se debe ver com una lista de diccionarios así:
device_list = [{"entity_id": "switch.switch_name", "power":18, "status": None, "beingControlled": False},...]
3. Ejecuta el script y monitorea la potencia en tiempo real. El script tomará decisiones sobre qué dispositivos encender o apagar para mantener la potencia deseada.

### Notas

- Es posible que necesite realizar ajustes según su configuración particular de Home Assistant y Tuya.
- Asegúrese de tener una conexión estable a Home Assistant y al medidor de potencia para obtener resultados óptimos.
- Este script es una solución básica para controlar la potencia. Puede necesitar mejoras y optimizaciones según sus necesidades.

### Contribuciones

Las contribuciones son bienvenidas. Si encuentras errores o tienes sugerencias, no dudes en abrir un issue o enviar un pull request.

### Licencia

Este proyecto está bajo la adjunta

---

**Nota:** El archivo `README.md` proporcionado es una plantilla básica. Puede personalizarlo aún más según sus necesidades y preferencias.
