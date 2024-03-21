import cv2
import numpy as np

def procesar_imagen(imagen):
    ancho_deseado = 640
    alto_deseado = 480

    if imagen.shape[1] != ancho_deseado or imagen.shape[0] != alto_deseado:
        imagen = cv2.resize(imagen, (ancho_deseado, alto_deseado))

    gray_image = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    imagen_procesada = cv2.bilateralFilter(gray_image, 11, 75, 75)

    return imagen_procesada

def calcular_volumen_borde(imagen, altura_estimada):
    bordes = cv2.Canny(imagen, 100, 200)
    cv2.imshow("Bordes", bordes) 
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contornos) == 0:
        print("No se encontraron contornos en la imagen.")
        return 0
    
    contorno_botella = max(contornos, key=cv2.contourArea)

    area_bordes = cv2.contourArea(contorno_botella)
    diametro_promedio = np.sqrt(4 * area_bordes / np.pi)
    radio = diametro_promedio / 2
    volumen_botella = np.pi * radio * radio * altura_estimada

    return volumen_botella

def calcular_tiempo_llenado(volumen_total, velocidad_salida):
    volumen_necesario = 0.9 * volumen_total
    tiempo_llenado = (volumen_necesario / velocidad_salida) * 60
    return tiempo_llenado

cam = cv2.VideoCapture(0)

capturar_frame = True
frame = None

while True:
    if capturar_frame:
        ret, frame = cam.read()

        if not ret:
            print("Error al leer el fotograma.")
            break

        imagen_procesada = procesar_imagen(frame)
        altura_estimada = 10

        volumen = calcular_volumen_borde(imagen_procesada, altura_estimada)

        cv2.imshow("Imagen original", frame)
        cv2.imshow("Imagen procesada", imagen_procesada)

        print("Volumen de la botella:", volumen, "cm3")
        velocidad_salida = 1000
        tiempo_llenado = calcular_tiempo_llenado(volumen, velocidad_salida)
        print("Tiempo de llenado: {} segundos".format(tiempo_llenado))

        capturar_frame = False

    key = cv2.waitKey(1)
    if key == ord(' '):
        capturar_frame = True
    elif key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()