from PIL import Image

# Abrir a imagem original
img = Image.open("images/hero_walk_3.png")

# Criar a versão espelhada
img_flipped = img.transpose(Image.FLIP_LEFT_RIGHT)

# Salvar como hero_left.png
img_flipped.save("images/hero_walk_3_left.png")