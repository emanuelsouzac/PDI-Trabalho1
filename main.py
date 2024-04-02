import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tkinter import ttk

# Criação da janela
root = tk.Tk()
root.geometry("1000x600")
root.title("Processamento de Imagens")
root.config(bg="white")

file_path = ""

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
        # the color wheel consists of 6 sectors. Figure out which sector
        # you're in.
        sectorPos = h / 60.0
        sectorNumber = int(sectorPos)
        # get the fractional part of the sector
        fractionalSector = sectorPos - sectorNumber

        # calculate values for the three axes of the color.
        p = b * (1.0 - s)
        q = b * (1.0 - (s * fractionalSector))
        t = b * (1.0 - (s * (1 - fractionalSector)))

        # assign the fractional colors to r, g, and b based on the sector
        # the angle is in.
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

##### FUNÇÕES DOS BOTÕES #####

# Função de adicionar imagem
def import_image():
    global file_path
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    # Ajustando tamanho da imagem para caber na exibição
    if image.width>image.height:
        # Largura maior que altura
        width = 750
        height = int(image.height*(750/image.width))
        image = image.resize((width,height), Image.LANCZOS)
    elif image.height>image.width:
        # Altura maior que largura
        height = 600
        width = int(image.width*(600/image.height))
        image = image.resize((width,height), Image.LANCZOS)
    else:
        # Dimensões iguais
        height = 600
        width = 600
        image = image.resize((width,height), Image.LANCZOS)
    # Ajustando canvas para o novo tamanho da imagem
    canvas.config(width=image.width, height=image.height)
    # Convertendo imagem para ser apresentada no canvas
    image = ImageTk.PhotoImage(image)
    # Exibindo imagem
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

# Função de exportar imagem
#def export_image():

# Função de brilho multiplicativo
def brightness():
    image = Image.open(file_path)
    # Ajustando tamanho da imagem para caber na exibição
    if image.width>image.height:
        # Largura maior que altura
        width = 750
        height = int(image.height*(750/image.width))
        image = image.resize((width,height), Image.LANCZOS)
    elif image.height>image.width:
        # Altura maior que largura
        height = 600
        width = int(image.width*(600/image.height))
        image = image.resize((width,height), Image.LANCZOS)
    else:
        # Dimensões iguais
        height = 600
        width = 600
        image = image.resize((width,height), Image.LANCZOS)
    # Ajustando canvas para o novo tamanho da imagem
    canvas.config(width=image.width, height=image.height)

    width = image.size[0]
    height = image.size[1]
    matrix_pixels = image.load() 

    for i in range(width):
        for j in range(height):
            pixel = matrix_pixels[i,j]
            
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            hue, sat, bright = RGBtoHSB(red, green, blue)
            bright = bright * 0.2 # Após converter para HSB, aplicar fator na variável de brilho, posteriormente convertendo para RGB e exibindo o resultado
            red, green, blue = HSBtoRGB(hue, sat, bright)

            new_pixel = (red, green, blue)
            matrix_pixels[i,j] = new_pixel

    # Convertendo imagem para ser apresentada no canvas
    image = ImageTk.PhotoImage(image)
    # Exibindo imagem
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

# Função de saturação multiplicativa
def saturation():
    image = Image.open(file_path)
    # Ajustando tamanho da imagem para caber na exibição
    if image.width>image.height:
        # Largura maior que altura
        width = 750
        height = int(image.height*(750/image.width))
        image = image.resize((width,height), Image.LANCZOS)
    elif image.height>image.width:
        # Altura maior que largura
        height = 600
        width = int(image.width*(600/image.height))
        image = image.resize((width,height), Image.LANCZOS)
    else:
        # Dimensões iguais
        height = 600
        width = 600
        image = image.resize((width,height), Image.LANCZOS)
    # Ajustando canvas para o novo tamanho da imagem
    canvas.config(width=image.width, height=image.height)

    width = image.size[0]
    height = image.size[1]
    matrix_pixels = image.load() 

    for i in range(width):
        for j in range(height):
            pixel = matrix_pixels[i,j]
            
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            hue, sat, bright = RGBtoHSB(red, green, blue)
            sat = sat * 1.5 # Após converter para HSB, aplicar fator na variável de saturação, posteriormente convertendo para RGB e exibindo o resultado
            red, green, blue = HSBtoRGB(hue, sat, bright)

            new_pixel = (red, green, blue)
            matrix_pixels[i,j] = new_pixel

    # Convertendo imagem para ser apresentada no canvas
    image = ImageTk.PhotoImage(image)
    # Exibindo imagem
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

# Função de matiz aditiva
def hue():
    image = Image.open(file_path)
    # Ajustando tamanho da imagem para caber na exibição
    if image.width>image.height:
        # Largura maior que altura
        width = 750
        height = int(image.height*(750/image.width))
        image = image.resize((width,height), Image.LANCZOS)
    elif image.height>image.width:
        # Altura maior que largura
        height = 600
        width = int(image.width*(600/image.height))
        image = image.resize((width,height), Image.LANCZOS)
    else:
        # Dimensões iguais
        height = 600
        width = 600
        image = image.resize((width,height), Image.LANCZOS)
    # Ajustando canvas para o novo tamanho da imagem
    canvas.config(width=image.width, height=image.height)

    width = image.size[0]
    height = image.size[1]
    matrix_pixels = image.load() 

    for i in range(width):
        for j in range(height):
            pixel = matrix_pixels[i,j]
            
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            hue, sat, bright = RGBtoHSB(red, green, blue)
            hue = (hue + 120) % 360 # Após converter para HSB, aplicar fator na variável de matiz, posteriormente convertendo para RGB e exibindo o resultado
            red, green, blue = HSBtoRGB(hue, sat, bright)

            new_pixel = (red, green, blue)
            matrix_pixels[i,j] = new_pixel

    # Convertendo imagem para ser apresentada no canvas
    image = ImageTk.PhotoImage(image)
    # Exibindo imagem
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

# Função de atribuição de saturação
#def saturation_assignment():
    
# Botão máscara de filtro
#def filter_mask():

# Frame da esquerda onde ficarão os botões
left_frame = tk.Frame(root, width=200, height=600, bg="grey")
left_frame.pack(side="left",fill="y")

# Onde a imagem será exibida
canvas = tk.Canvas(root, width=750, height=600)
canvas.pack()

##### BOTÕES #####

# Botão brilho HSB multiplicativo
brightness_button = tk.Button(left_frame, text="Brilho HSB Multiplicativo", command=brightness, bg="white")
brightness_button.pack(padx=5,pady=5)

# Botão saturação HSB multiplicativa
saturation_button = tk.Button(left_frame, text="Saturação HSB Multiplicativa", command=saturation, bg="white")
saturation_button.pack(padx=5,pady=5)

# Botão matiz HSB aditiva
hue_button = tk.Button(left_frame, text="Matiz HSB Aditiva", command=hue, bg="white")
hue_button.pack(padx=5,pady=5)

# Botão atribuição de saturação de outra imagem
saturationAssignment_button = tk.Button(left_frame, text="Atribuição de Saturação", bg="white")
saturationAssignment_button.pack(padx=5,pady=5)

# Botão máscara de filtro
filterMask_button = tk.Button(left_frame, text="Máscara de Filtro", bg="white")
filterMask_button.pack(padx=5,pady=5)

# Botão exportar imagem
exportImage_button = tk.Button(left_frame, text="Exportar Imagem", bg="white")
exportImage_button.pack(side="bottom", padx=5,pady=5)

# Botão importar imagem
importImage_button = tk.Button(left_frame, text="Importar Imagem", command=import_image, bg="white")
importImage_button.pack(side="bottom", padx=5,pady=5)

root.mainloop()