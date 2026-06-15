import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import gradio as gr
import data_aug as dt

# 1. Criação das abas
with gr.Blocks() as app:
    gr.Markdown("# Data Aug com Gradio")

    with gr.Tabs():
        # Aba Visualização Individual
        with gr.Tab("Visualização Individual"):
            
            # Linha para separar coluna
            with gr.Row():
                
                # Coluna 1: Imagem Original (Esquerda)
                with gr.Column():
                    gr.Markdown("### Entrada")
                    img_entrada = gr.Image(label="Imagem Original", type="numpy")

                # Coluna 2: Controles/Sliders (Centro)
                with gr.Column():
                    gr.Markdown("### Ajustes")
                    rotacao = gr.Slider(-180, 180, value=0, label="Rotação em Graus") 
                    escala = gr.Slider(0.5, 2.0, value=1.0, label="Escala") 
                    tx = gr.Slider(-100, 100, value=0, label="Translação no eixo X")
                    ty = gr.Slider(-100, 100, value=0, label="Translação no eixo Y")
                    gamma = gr.Slider(0.3, 3.0, value=1.0, label="Gamma") 
                    reflexao = gr.Checkbox(label="Aplicar Reflexão Horizontal")
                    aleatorio = gr.Button("Gerar Transformação Aleatória")

                # Coluna 3: Saída Imagem (Direita)
                with gr.Column():
                    gr.Markdown("### Resultado")
                    img_saida = gr.Image(label="Imagem Saída")

            # --------Eventos dos sliders da Aba 1----------

            # Rotação
            rotacao.change(fn=dt.aplicar_rotacao, inputs=[img_entrada, rotacao], outputs=img_saida)

            # Escala
            escala.change(fn=dt.aplicar_escala, inputs=[img_entrada, escala], outputs=img_saida)

            # Translação (ambos os eixos acionam a mesma função)
            tx.change(fn=dt.aplicar_translacao, inputs=[img_entrada, tx, ty], outputs=img_saida)
            ty.change(fn=dt.aplicar_translacao, inputs=[img_entrada, tx, ty], outputs=img_saida)

            # Gamma
            gamma.change(fn=dt.aplicar_gamma, inputs=[img_entrada, gamma], outputs=img_saida)
            
            # Reflexão
            reflexao.change(fn=dt.reflexao, inputs=[img_entrada, reflexao], outputs=img_saida)

            # Transformação aleatoria
            aleatorio.click(fn=dt.aplicar_aleatorio, inputs=img_entrada, outputs=img_saida)


        # Aba do Dataset
        with gr.Tab("Gerar Dataset"):
            with gr.Row():
                # Coluna de Entrada e Configurações
                with gr.Column():
                    gr.Markdown("### Imagem de Entrada")
                    img_data_in = gr.Image(label="Imagem Original", type="numpy")
                    
                    gr.Markdown("### Ajustes de Quantidade")
                    data_qtd = gr.Slider(1, 100, value=1, step=1, label="Qtd. de Variações")
                    
                    btn_gerar = gr.Button("Gerar Dataset", variant="primary")

                # Coluna de Intervalos (Ranges)
                with gr.Column():
                    gr.Markdown("### Configurações de Ranges Aleatórios")
                    
                    # Coluna da rotação
                    with gr.Row():
                        rot_min = gr.Number(label="Rotação Mín (°)", value=-30)
                        rot_max = gr.Number(label="Rotação Máx (°)", value=30)

                    # Coluna da escala
                    with gr.Row():
                        esc_min = gr.Number(label="Escala Mín (x)", value=0.8)
                        esc_max = gr.Number(label="Escala Máx (x)", value=1.2)

                    # Coluna do gamma
                    with gr.Row():
                        gam_min = gr.Number(label="Gamma Mín", value=0.7)
                        gam_max = gr.Number(label="Gamma Máx", value=1.3)

                # Coluna de Saída (Galeria e Download)
                with gr.Column():
                    gr.Markdown("### Variações Geradas")
                    # Galeria para mostrar as imagens geradas 
                    galeria = gr.Gallery(label="Galeria de Imagens", columns= 4)
                    
                    # Botão para download do ZIP 
                    btn_zip = gr.File(label="Download do Dataset (ZIP)")

        
            # A função no data_aug.py retorna o dataset e a galeria para download
            btn_gerar.click(
                fn=dt.gerar_dataset, 
                inputs=[img_data_in, data_qtd, rot_min, rot_max, esc_min, esc_max, gam_min, gam_max],  # Cada parametro (rotação, escala e gamma solicitado no exercício) entrando na gerar_dataset
                outputs=[galeria, btn_zip]
            )

app.launch()