import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import copy
import os

# Criação da janela
root = tk.Tk()
root.geometry("1280x720")
root.title("Processamento de Imagens")
root.config(bg="white")

# Variáveis globais
file_path = ""
original_image, edition_image = None, None

##### FUNÇÕES DE CONVERSÃO #####

# Conversor RGB para HSB
def RGBtoHSB(red, green, blue):
    # normalize red, green and blue values
    r = red / 255.0
    g = green / 255.0
    b = blue / 255.0

    # conversion start
    max_val = max(r, g, b)
    min_val = min(r, g, b)

    if max_val == min_val:
        h = 0
    elif max_val == r and g >= b:
        h = 60 * (g - b) / (max_val - min_val)
    elif max_val == r and g < b:
        h = 60 * (g - b) / (max_val - min_val) + 360
    elif max_val == g:
        h = 60 * (b - r) / (max_val - min_val) + 120
    elif max_val == b:
        h = 60 * (r - g) / (max_val - min_val) + 240

    s = 0 if max_val == 0 else 1.0 - min_val / max_val

    return h, s, max_val

# Conversor HSB para RGB
def HSBtoRGB(h, s, b):
    if s == 0:
        r = g = b = b
    else:
        # A roda de cores consiste em 6 setores.       
        sectorPos = h / 60.0
        sectorNumber = int(sectorPos)

        # Obtendo a parte fracionária do setor
        fractionalSector = sectorPos - sectorNumber

        # Calculando os valores para os três eixos da cor.
        p = b * (1.0 - s)
        q = b * (1.0 - (s * fractionalSector))
        t = b * (1.0 - (s * (1 - fractionalSector)))

        # Atribuindo as cores fracionárias a r, g e b com base no setor
        
        if sectorNumber == 0:
            r = b
            g = t
            b = p
        elif sectorNumber == 1:
            r = q
            g = b
            b = p
        elif sectorNumber == 2:
            r = p
            g = b
            b = t
        elif sectorNumber == 3:
            r = p
            g = q
            b = b
        elif sectorNumber == 4:
            r = t
            g = p
            b = b
        elif sectorNumber == 5:
            r = b
            g = p
            b = q

    return int(r * 255.0), int(g * 255.0), int(b * 255.0)

##### FUNÇÃO PARA EXIBIR IMAGEM #####

def display():
    global edition_image

    # Fazendo cópia da imagem editada para exibição
    display_image = copy.copy(edition_image)

    # Ajustando tamanho da imagem para caber na exibição
    if display_image.width > display_image.height:
        # Largura maior que altura
        width = 900
        height = int(display_image.height * (900 / display_image.width))
        display_image = display_image.resize((width, height), Image.LANCZOS)
    elif display_image.height > display_image.width:
        # Altura maior que largura
        height = 720
        width = int(display_image.width * (720 / display_image.height))
        display_image = display_image.resize((width, height), Image.LANCZOS)
    else:
        # Dimensões iguais
        height = 720
        width = 720
        display_image = display_image.resize((width, height), Image.LANCZOS)

    # Ajustando canvas para o novo tamanho da imagem
    canvas.config(width=display_image.width, height=display_image.height)

    # Convertendo imagem para ser apresentada no canvas
    display_image = ImageTk.PhotoImage(display_image)

    # Exibindo imagem
    canvas.image = display_image
    canvas.create_image(0, 0, image=display_image, anchor="nw")

##### FUNÇÕES DOS BOTÕES #####

# Função de importar imagem
def import_image():
    global file_path, original_image, edition_image

    file_path = filedialog.askopenfilename()
    original_image = Image.open(file_path)
    edition_image = copy.copy(original_image)

    display()

# Função de exportar imagem
def export_image():
    global edition_image
    if edition_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"),
                                                             ("All files", ".")])
        if save_path:
            edition_image.save(save_path)
            messagebox.showinfo("Exportar Imagem", "Imagem exportada com sucesso.")
    else:
        messagebox.showerror("Erro", "Nenhuma imagem foi importada.")

# Função que gera um pop-up para usuário inserir fator
# que será usado no aumento do brilho, saturação e matiz
def get_user_input(label_text, callback):
    def apply_user_input():
        # Pega o valor da entrada
        user_input = user_input_entry.get()
        # Chama a função em questão (brilho, saturação ou matiz), passando o valor
        callback(user_input)
        # Fecha o pop-up
        user_input_window.destroy()

    # Definições da janela
    user_input_window = tk.Toplevel(root)
    user_input_window.title("Entrada do Usuário")
    user_input_window.geometry("200x100")
    user_input_window.resizable(False, False)

    user_input_label = tk.Label(user_input_window, text=label_text)
    user_input_label.pack(pady=5)

    user_input_entry = tk.Entry(user_input_window)
    user_input_entry.pack(pady=5)

    ok_button = tk.Button(user_input_window, text="OK", command=apply_user_input)
    ok_button.pack(pady=5)

# Função de brilho multiplicativo
def brightness():
    def apply_brightness_factor(brightness_factor):
        global edition_image

        # Variável que permitirá acesso e manipulação em cada pixel da imagem
        matrix_pixels = edition_image.load()

        for i in range(edition_image.width):
            for j in range(edition_image.height):
                # Pegando cada banda de cor do pixel (i,j)
                pixel = matrix_pixels[i, j]
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                # Após converter para HSB
                hue, sat, bright = RGBtoHSB(red, green, blue)
                # Aplicação do fator na variável de brilho
                bright = bright * float(brightness_factor)
                # Conversão para HSB
                red, green, blue = HSBtoRGB(hue, sat, bright)

                # Aplicação da mudança no pixel (i,j)
                matrix_pixels[i, j] = (red, green, blue)

        display()

    # Abre um pop-up para capturar fator do usuário
    get_user_input("Insira o fator de brilho:", apply_brightness_factor)

# Função de saturação multiplicativa
def saturation():
    def apply_saturation_factor(saturation_factor):
        global edition_image

        matrix_pixels = edition_image.load()

        for i in range(edition_image.width):
            for j in range(edition_image.height):
                pixel = matrix_pixels[i, j]
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                hue, sat, bright = RGBtoHSB(red, green, blue)
                sat = sat * float(saturation_factor)
                red, green, blue = HSBtoRGB(hue, sat, bright)

                matrix_pixels[i, j] = (red, green, blue)

        display()

    # Abre um pop-up para capturar fator do usuário
    get_user_input("Insira o fator de saturação:", apply_saturation_factor)

# Função de matiz aditiva
def hue():
    def apply_hue_factor(hue_factor):
        global edition_image

        matrix_pixels = edition_image.load()

        for i in range(edition_image.width):
            for j in range(edition_image.height):
                pixel = matrix_pixels[i, j]
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                hue, sat, bright = RGBtoHSB(red, green, blue)
                hue = (hue + float(hue_factor)) % 360 
                red, green, blue = HSBtoRGB(hue, sat, bright)

                matrix_pixels[i, j] = (red, green, blue)

        display()

    # Abre um pop-up para capturar fator do usuário
    get_user_input("Insira o fator de matiz:", apply_hue_factor)

# Função de atribuição de saturação
def saturation_assignment():
    global edition_image

    # Abrindo a segunda imagem
    file_path_2 = filedialog.askopenfilename()
    image_2 = Image.open(file_path_2)

    # Verificando se as duas imagens possuem mesmas dimensões
    if edition_image.width == image_2.width and edition_image.height == image_2.height:

        matrix_pixels_1 = edition_image.load()
        matrix_pixels_2 = image_2.load()

        for i in range(edition_image.width):
            for j in range(edition_image.height):
                pixel_1 = matrix_pixels_1[i, j]
                red_1 = pixel_1[0]
                green_1 = pixel_1[1]
                blue_1 = pixel_1[2]
                hue_1, sat_1, bright_1 = RGBtoHSB(red_1, green_1, blue_1)

                pixel_2 = matrix_pixels_2[i, j]
                red_2 = pixel_2[0]
                green_2 = pixel_2[1]
                blue_2 = pixel_2[2]
                hue_2, sat_2, bright_2 = RGBtoHSB(red_2, green_2, blue_2)

                # Conversão a imagem editada de volta para RGB,
                # porém atribuindo a saturação da segunda imagem
                red_1, green_1, blue_1 = HSBtoRGB(hue_1, sat_2, bright_1)

                matrix_pixels_1[i, j] = (red_1, green_1, blue_1)

        display()
    else:
        messagebox.showerror("Erro", "As duas imagens não possuem as mesmas dimensões.")

# Botão máscara de filtro
def filter_mask():
    global edition_image

    # Abrindo txt
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt")])

    if file_path:

        file_name = os.path.basename(file_path)

        with open(file_path, 'r') as file:
            elements = file.readlines()

        # Coletando as dimensões m e n da máscara
        lines= int(elements[0].split()[0])
        columns = int(elements[1].split()[0])
    
        # Criando a matriz a partir do txt
        matrix = []
        for element in elements[2:]:
            matrix.append([float(num) for num in element.split()])

        # Criação da nova imagem que será resultado da correlação
        # Por ser correlação sem extensão, a nova imagem possui reajuste das dimensões
        width, height = (edition_image.width - columns + 1), (edition_image.height - lines + 1)
        img2 = Image.new('RGB', (width, height))
        matrix_pixels2 = img2.load()
        
        for i in range(height):
            for j in range(width):
                r, g, b = 0, 0, 0
                for m in range(lines):
                    for n in range(columns):
                        # Ajustando as coordenadas para garantir que estejam dentro dos limites da imagem
                        pixel_x = j + n
                        pixel_y = i + m
                        # Verificando se o pixel está dentro dos limites da imagem
                        if 0 <= pixel_x < edition_image.width and 0 <= pixel_y < edition_image.height:
                            # Obtendo os valores RGB do pixel da imagem original
                            pixel_r, pixel_g, pixel_b = edition_image.getpixel((pixel_x, pixel_y))
                            # Calculando os valores médios ponderados pelos valores na matriz de filtro
                            r += pixel_r * matrix[m][n]
                            g += pixel_g * matrix[m][n]
                            b += pixel_b * matrix[m][n]
                # Definindo os valores RGB no pixel correspondente na nova imagem
                matrix_pixels2[j, i] = (int(r), int(g), int(b))
        
        # A imagem de edição assume o valor na nova imagem
        edition_image = copy.copy(img2)
        
        # Expansão de histograma    
        if file_name == "horizontalsobel.txt" or file_name == "verticalsobel.txt":
            
            matrix_pixels = edition_image.load()
            r_min, g_min, b_min, r_max, g_max, b_max = 255, 255, 255, 0, 0, 0
            
            # Coletando os valores mínimos e máximos de cada banda de cor
            for i in range(width):
                for j in range(height):
                    pixel_r, pixel_g, pixel_b = edition_image.getpixel((i, j))
                    if pixel_r > r_max: r_max = pixel_r
                    if pixel_r < r_min: r_min = pixel_r
                    if pixel_g > g_max: g_max = pixel_g
                    if pixel_g < g_min: g_min = pixel_g
                    if pixel_b > b_max: b_max = pixel_b
                    if pixel_b < b_min: b_min = pixel_b

            # Realizando a expansão de histograma em cada banda de cor
            for i in range(width):
                for j in range(height):
                    pixel_r, pixel_g, pixel_b = edition_image.getpixel((i, j))
                    novo_pixel_r = ((pixel_r - r_min)/(r_max - r_min))*255
                    novo_pixel_g = ((pixel_g - g_min)/(g_max - g_min))*255
                    novo_pixel_b = ((pixel_b - b_min)/(b_max - b_min))*255
                    matrix_pixels[i, j] = (int(novo_pixel_r), int(novo_pixel_g), int(novo_pixel_b))

        display()

# Botão reset
def reset_image():
    global original_image, edition_image
    edition_image = copy.copy(original_image)

    display()

# Frame da esquerda onde ficarão os botões
left_frame = tk.Frame(root, width=200, height=720, bg="grey")
left_frame.pack(side="left", fill="y")

# Onde a imagem será exibida
canvas = tk.Canvas(root, width=1080, height=720, bg="white")
canvas.pack()

##### BOTÕES #####

# Botão brilho HSB multiplicativo
brightness_button = tk.Button(left_frame, text="Brilho HSB Multiplicativo", command=brightness, bg="white")
brightness_button.pack(padx=5, pady=5, fill="x")

# Botão saturação HSB multiplicativa
saturation_button = tk.Button(left_frame, text="Saturação HSB Multiplicativa", command=saturation, bg="white")
saturation_button.pack(padx=5, pady=5, fill="x")

# Botão matiz HSB aditiva
hue_button = tk.Button(left_frame, text="Matiz HSB Aditiva", command=hue, bg="white")
hue_button.pack(padx=5, pady=5, fill="x")

# Botão atribuição de saturação de outra imagem
saturationAssignment_button = tk.Button(left_frame, text="Atribuição de Saturação", command=saturation_assignment,
                                         bg="white")
saturationAssignment_button.pack(padx=5, pady=5, fill="x")

# Botão máscara de filtro
filterMask_button = tk.Button(left_frame, text="Máscara de Filtro", command=filter_mask, bg="white")
filterMask_button.pack(padx=5, pady=5, fill="x")

# Botão reset
reset_button = tk.Button(left_frame, text="Reset", command=reset_image, bg="white")
reset_button.pack(padx=5, pady=5, fill="x")

# Botão exportar imagem
exportImage_button = tk.Button(left_frame, text="Exportar Imagem", command=export_image, bg="white")
exportImage_button.pack(side="bottom", padx=5, pady=5, fill="x")

# Botão importar imagem
importImage_button = tk.Button(left_frame, text="Importar Imagem", command=import_image, bg="white")
importImage_button.pack(side="bottom", padx=5, pady=5, fill="x")

root.mainloop()