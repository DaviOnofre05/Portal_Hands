import cv2
import mediapipe as mp
import numpy as np
import math

mp_maos = mp.solutions.hands
maos = mp_maos.Hands(
    max_num_hands=2,               
    min_detection_confidence=0.7,  
    min_tracking_confidence=0.7    
)

mp_desenho = mp.solutions.drawing_utils

captura = cv2.VideoCapture(0)

def efeito_termico(img):
    return cv2.applyColorMap(img, cv2.COLORMAP_JET)

def efeito_predador(img):
    return cv2.applyColorMap(img, cv2.COLORMAP_HSV)

def efeito_invertido(img):
    return cv2.bitwise_not(img)

def efeito_minecraft(img):
    altura, largura = img.shape[:2]
    pequena = cv2.resize(img, (largura // 20, altura // 20), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(pequena, (largura, altura), interpolation=cv2.INTER_NEAREST)

def efeito_matrix(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contornos = cv2.Canny(cinza, 50, 150)
    matrix = np.zeros_like(img)
    matrix[contornos == 255] = [0, 255, 0]
    return matrix

def efeito_cartoon(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cinza_suave = cv2.medianBlur(cinza, 5)
    
    bordas = cv2.adaptiveThreshold(cinza_suave, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    cor = cv2.bilateralFilter(img, 9, 300, 300)
    
    cartoon = cv2.bitwise_and(cor, cor, mask=bordas)
    return cartoon

def efeito_sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia = cv2.transform(img, kernel)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    return sepia

def efeito_glitch(img):
    glitch = img.copy()
    
    deslocamento = 15
    glitch[:, deslocamento:, 2] = img[:, :-deslocamento, 2] 
    glitch[:, :-deslocamento, 0] = img[:, deslocamento:, 0] 
    return glitch

filtros = [efeito_termico, efeito_minecraft, efeito_matrix, efeito_invertido, efeito_predador, efeito_cartoon, efeito_sepia, efeito_glitch]

index_filtro = 0

dedos_juntos = False

while True: 

    sucesso, frame = captura.read()

    if not sucesso:
        break

    frame = cv2.flip(frame, 1)
    
    altura, largura, _ = frame.shape
    

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resultados = maos.process(frame_rgb)
    
    maos_detectadas = []

    if resultados.multi_hand_landmarks:
        for marcacoes_maos in resultados.multi_hand_landmarks:
            
            polegar = marcacoes_maos.landmark[4]
            indicador = marcacoes_maos.landmark[8]
            
            p_x, p_y = int(polegar.x * largura), int(polegar.y * altura)
            i_x, i_y = int(indicador.x * largura), int(indicador.y * altura)
            
            maos_detectadas.append({
                "polegar": [p_x, p_y],
                "indicador": [i_x, i_y],
                "centro_x": (p_x + i_x) / 2 
            })
            
    if len(maos_detectadas) == 2:

        maos_detectadas = sorted(maos_detectadas, key=lambda m: m["centro_x"])
        
        mao_esquerda = maos_detectadas[0]
        mao_direita = maos_detectadas[1]
        
        ix_d, iy_d = mao_direita["indicador"]
        px_d, py_d = mao_direita["polegar"]
        distancia_direita = math.hypot(ix_d - px_d, iy_d - py_d)
        
        ix_e, iy_e = mao_esquerda["indicador"]
        px_e, py_e = mao_esquerda["polegar"]
        distancia_esquerda = math.hypot(ix_e - px_e, iy_e - py_e)
        
        if distancia_direita < 30 and distancia_esquerda < 30:
            if not dedos_juntos:
                index_filtro = (index_filtro + 1) % len(filtros)
                dedos_juntos = True
        else:
            dedos_juntos = False
        
        pontos_ordenados = [
            mao_esquerda["indicador"],
            mao_direita["indicador"],
            mao_direita["polegar"],
            mao_esquerda["polegar"]
        ]

        pontos_np = np.array(pontos_ordenados, dtype=np.int32)
        
        mascara = np.zeros((altura, largura), dtype=np.uint8)
        
        cv2.fillPoly(mascara, [pontos_np], 255)
        
        funcao_filtro = filtros[index_filtro]
        
        frame_filtrado = funcao_filtro(frame)
        
        mascara_3_canais = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
        
        frame = np.where(mascara_3_canais == 255, frame_filtrado, frame)
        
    cv2.imshow("Portal", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()