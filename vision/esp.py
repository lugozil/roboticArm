import network

# Configurar las credenciales de WiFi
ssid = 'nombre_de_red'
password = 'contraseña_de_red'

# Conectar a la red WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)

# Esperar a que se establezca la conexión
while not sta_if.isconnected():
    print('Conectando a la red WiFi...')
print('Conectado a la red WiFi')