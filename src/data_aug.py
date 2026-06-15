import cv2
import numpy as np
import random
import os
import shutil  
import zipfile 

# 1. Função para rotacionar (mantém o tamanho original)
def aplicar_rotacao(img, angulo):
    h, w = img.shape[:2]          
    centro = (w // 2, h // 2)      # centro baseado no tamanho atual
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)

    return cv2.warpAffine(img, M, (w, h))   # mantém largura e altura atuais

# 2. Função para escala
def aplicar_escala(img, fator):
    h, w = img.shape[:2]
    novo_w = int(w * fator)
    novo_h = int(h * fator)

    return cv2.resize(img, (novo_w, novo_h))   # retorna imagem com novo tamanho

# 3. Função para Translação 
def aplicar_translacao(img, tx, ty):  # tx e ty representam, respectivamente, eixo x e eixo y
    h, w = img.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])

    return cv2.warpAffine(img, M, (w, h))   # tamanho atual (largura, altura)

# 4. Função para Reflexão 
def reflexao(img, checkbox):  # Verifica se o checkbox da aba 1 do gradio foi ativo

    if checkbox:
        return cv2.flip(img, 1) 
    else:
        return img

# 5. Ajuste de gamma 
def aplicar_gamma(img, gamma):
    img_norm = img / 255.0
    img_corrigida = np.power(img_norm, gamma)  # Lei de Potêncianos - valores normalizados
    return (img_corrigida * 255).astype(np.uint8)

# 6. Gera uma única imagem aumentada com parâmetros aleatórios (botão aleatório aba 1)
def aplicar_aleatorio(img):
    escolha = random.randint(0, 4) 
    
    match escolha:
        case 0:
            # Sorteia um ângulo e aplica a rotação
            angulo = random.uniform(-30, 30)
            return aplicar_rotacao(img, angulo)
        case 1:
            # Sorteia um fator e aplica a escala
            fator = random.uniform(0.8, 1.2)
            return aplicar_escala(img, fator)
        case 2:
            # Sorteia translação X e Y e aplica
            tx, ty = random.uniform(-50, 50), random.uniform(-50, 50)
            return aplicar_translacao(img, tx, ty)
        case 3:
            # Reflexão com valor boolean
            return reflexao(img, True) 
        case 4:
            # Sorteia um gamma e aplica
            g = random.uniform(0.7, 1.3)
            return aplicar_gamma(img, g)

# 7. Função para gerar dataser
def gerar_dataset(img, data_qtd, rot_min, rot_max, esc_min, esc_max, gam_min, gam_max):
    lista_galeria = []
    pasta_temp = "dataset_temp"
    nome_zip = "dataset_aumentado.zip"

    # Limpa a pasta temporária se ela já existir
    if os.path.exists(pasta_temp):
        shutil.rmtree(pasta_temp)
    os.makedirs(pasta_temp)

    # Gerar o ZIP pelo input do usuário
    with zipfile.ZipFile(nome_zip, 'w') as zipf:
        for i in range(int(data_qtd)):
            # Sorteia os valores dentro dos ranges informados pelo utilizador
            angulo = random.uniform(rot_min, rot_max)
            fator = random.uniform(esc_min, esc_max)
            valor_gamma = random.uniform(gam_min, gam_max)

            # Aplica as tuas funções de forma sequencial
            img_aug = aplicar_rotacao(img, angulo)  
            img_aug = aplicar_escala(img_aug, fator)  # A imagem resultante de uma serve de entrada para a próxima
            img_aug = aplicar_gamma(img_aug, valor_gamma)

            # Guarda na lista da galeria (Gradio usa RGB)
            lista_galeria.append(img_aug)

            # 4. Guarda no disco e adiciona ao ZIP (OpenCV usa BGR)
            nome_foto = f"aug_{i+1:03d}.png"
            caminho_foto = os.path.join(pasta_temp, nome_foto)
            
            img_bgr = cv2.cvtColor(img_aug, cv2.COLOR_RGB2BGR)
            cv2.imwrite(caminho_foto, img_bgr)
            zipf.write(caminho_foto, nome_foto)

    # Retorna a lista para a Galeria e o ficheiro para o componente File
    return lista_galeria, nome_zip