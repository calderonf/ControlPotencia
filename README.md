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


### 1. Crear un archivo de servicio para systemd

Primero, necesitas crear un archivo de definición de servicio para `systemd`. Vamos a llamarlo `control_de_potencia.service`. Puedes crearlo en el directorio `/etc/systemd/system/`.

```bash
sudo nano /etc/systemd/system/control_de_potencia.service
```

Agrega el siguiente contenido al archivo:

```ini
[Unit]
Description=Control de Potencia para Home Assistant
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/$(user)/ControlPotencia/Control_de_potencia.py
Restart=always
User=$(user)
Group=nombre_del_grupo
WorkingDirectory=/home/$(user)/ControlPotencia/

[Install]
WantedBy=multi-user.target
```

- Asegúrate de reemplazar `/ruta/completa/a/` con la ruta completa al directorio donde se encuentra tu script.
- Cambia `nombre_de_usuario` y `nombre_del_grupo` al usuario y grupo bajo los cuales quieres ejecutar el script. Por lo general, podrías usar tu propio nombre de usuario y grupo.

### 2. Dar permisos al archivo de servicio

```bash
sudo chmod 644 /etc/systemd/system/control_de_potencia.service
```

### 3. Recargar el daemon de systemd

Cada vez que agregues o modifiques un archivo de servicio, debes decirle a `systemd` que lo recargue:

```bash
sudo systemctl daemon-reload
```

### 4. Habilitar el servicio

Para que tu servicio se inicie automáticamente al arrancar el sistema:

```bash
sudo systemctl enable control_de_potencia.service
```

### 5. Iniciar el servicio

Ahora puedes iniciar tu servicio manualmente:

```bash
sudo systemctl start control_de_potencia.service
```

### 6. Verificar el estado del servicio

Para asegurarte de que tu servicio está ejecutándose correctamente:

```bash
sudo systemctl status control_de_potencia.service
```

### 7. (Opcional) Ver los logs

Si quieres ver los mensajes de log de tu servicio (especialmente útil si algo no funciona correctamente):

```bash
journalctl -u control_de_potencia.service
```

Y eso es todo. Con estos pasos, tu script `Control_de_potencia.py` debería estar configurado como un servicio que se inicia automáticamente al arrancar tu sistema y que puedes gestionar fácilmente con `systemctl`.
