import random
import pgzrun

# Configurações do jogo
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer com Inimigos"
FPS = 60

# Constantes de física
GRAVITY = 0.5
JUMP_POWER = -15
MAX_FALL_SPEED = 15
MOVE_SPEED = 5

class Hero:
    def __init__(self):
        self.images_right = ["hero_walk_0", "hero_walk_1", "hero_walk_2", "hero_walk_3"]
        self.images_left = ["hero_walk_0_left", "hero_walk_1_left", "hero_walk_2_left", "hero_walk_3_left"]
        self.idle_right = "hero_walk_0"
        self.idle_left = "hero_walk_0_left"
        self.hit_image = "hero_walk_0"
        
        self.actor = Actor(self.idle_right, (100, HEIGHT - 100))
        self.vy = 0
        self.vx = 0
        self.on_ground = False
        self.direction = "right"
        self.animation_frame = 0
        self.animation_timer = 0
        self.health = 3
        self.invincibility_frames = 0
        self.opacity = 255
        
    def update(self, platforms):
        # Aplicar gravidade
        self.vy += GRAVITY
        self.vy = min(self.vy, MAX_FALL_SPEED)
        
        # Movimento horizontal
        self.vx = 0
        if keyboard.left:
            self.vx = -MOVE_SPEED
            self.direction = "left"
        elif keyboard.right:
            self.vx = MOVE_SPEED
            self.direction = "right"
        
        # Atualizar posição X
        self.actor.x += self.vx
        
        # Verificar colisões laterais
        for platform in platforms:
            if self.actor.colliderect(platform) and self.vx != 0:
                if self.vx > 0:  # Movendo para direita
                    self.actor.right = platform.left
                elif self.vx < 0:  # Movendo para esquerda
                    self.actor.left = platform.right
        
        # Atualizar posição Y
        self.actor.y += self.vy
        
        # Verificar colisões verticais
        self.on_ground = False
        for platform in platforms:
            if self.actor.colliderect(platform):
                if self.vy > 0:  # Caindo
                    self.actor.bottom = platform.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:  # Subindo
                    self.actor.top = platform.bottom
                    self.vy = 0
        
        # Manter personagem na tela
        self.actor.x = max(self.actor.width/2, min(WIDTH - self.actor.width/2, self.actor.x))
        self.actor.y = max(self.actor.height/2, min(HEIGHT - self.actor.height/2, self.actor.y))
        
        # Atualizar invencibilidade
        if self.invincibility_frames > 0:
            self.invincibility_frames -= 1
            self.opacity = 100 if self.invincibility_frames % 10 < 5 else 255
        else:
            self.opacity = 255
    
    def update_animation(self):
        self.animation_timer += 1
        
        if self.on_ground:
            if self.vx != 0:  # Andando
                if self.animation_timer % 5 == 0:
                    self.animation_frame = (self.animation_frame + 1) % len(self.images_right)
                if self.direction == "right":
                    self.actor.image = self.images_right[self.animation_frame]
                else:
                    self.actor.image = self.images_left[self.animation_frame]
            else:  # Parado
                if self.direction == "right":
                    self.actor.image = self.idle_right
                else:
                    self.actor.image = self.idle_left
        else:  # No ar
            if self.direction == "right":
                self.actor.image = self.images_right[1]  # Frame fixo no ar
            else:
                self.actor.image = self.images_left[1]
    
    def jump(self):
        if self.on_ground:
            self.vy = JUMP_POWER
            self.on_ground = False
            # sounds.jump.play()
    
    def take_damage(self):
        if self.invincibility_frames <= 0:
            self.health -= 1
            self.invincibility_frames = 60  # 1 segundo de invencibilidade
            sounds.hit.play()
            return True
        return False
    
    def draw(self):
        self.actor.opacity = self.opacity
        self.actor.draw()

class Enemy:
    def __init__(self, x, y):
        self.images = ["enemy_0", "enemy_1", "enemy_2"]
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = 1  # 1 para direita, -1 para esquerda
        self.animation_frame = 0
        self.animation_timer = 0
        self.width = 50
        self.height = 30
        
    def update(self):
        self.x += self.speed * self.direction
        
        # Inverter direção ao atingir bordas
        if self.x < 0 or self.x > WIDTH:
            self.direction *= -1
            
        # Atualizar animação
        self.animation_timer += 1
        if self.animation_timer % 10 == 0:
            self.animation_frame = (self.animation_frame + 1) % len(self.images)
    
    def draw(self):
        # Desenhar o inimigo (flip se estiver indo para esquerda)
        enemy_img = self.images[self.animation_frame]
        screen.blit(enemy_img, (self.x, self.y))
    
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.state = "menu"
        self.hero = Hero()
        self.platforms = [
            Rect((0, HEIGHT - 20), (WIDTH, 20)),
            Rect((200, 400), (150, 20)),
            Rect((400, 300), (150, 20)),
            Rect((600, 200), (150, 20))
        ]
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 300  # frames
        
        # Configurar música
        try:
            music.play("background_music")
            music.set_volume(0.5)
        except:
            print("Erro ao carregar música.")
    
    def update(self):
        if self.state == "playing":
            self.hero.update(self.platforms)
            self.hero.update_animation()
            
            # Spawn de inimigos
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= self.enemy_spawn_rate and random.random() < 0.3:
                self.spawn_enemy()
                self.enemy_spawn_timer = 0
            
            # Atualizar inimigos e verificar colisões
            for enemy in self.enemies[:]:
                enemy.update()
                
                if (self.hero.invincibility_frames <= 0 and 
                    self.hero.actor.colliderect(enemy.get_rect()) and 
                    self.hero.vy >= 0):
                    
                    if self.hero.take_damage() and self.hero.health <= 0:
                        self.game_over()
    
    def spawn_enemy(self):
        if self.platforms:
            plat = random.choice(self.platforms)
            self.enemies.append(Enemy(plat.left, plat.top - 30))
    
    def draw(self):
        screen.clear()
        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()
    
    def draw_menu(self):
        screen.fill((0, 0, 50))  
        screen.draw.text(TITLE, center=(WIDTH//2, HEIGHT//3), fontsize=50, color="white")
        screen.draw.text("Press SPACE to Start", center=(WIDTH//2, HEIGHT//2), fontsize=30, color="yellow")
        screen.draw.text("Press M to Toggle Music", center=(WIDTH//2, HEIGHT//2 + 40), fontsize=25, color="lightgray")
        screen.draw.text("Press ESC to Quit", center=(WIDTH//2, HEIGHT//2 + 80), fontsize=25, color="red")
    
    def draw_game(self):
        screen.fill((0, 0, 30))  
        
        # Desenhar plataformas
        for platform in self.platforms:
            screen.draw.filled_rect(platform, "gray")
        
        # Desenhar inimigos
        for enemy in self.enemies:
            enemy.draw()
        
        # Desenhar herói
        self.hero.draw()
        
        # Mostrar vida
        for i in range(self.hero.health):
            screen.blit("heart", (10 + i * 30, 10))
        
        # Se invencível, mostrar efeito
        if self.hero.invincibility_frames > 0:
            screen.draw.text("INVENCIBLE", (WIDTH//2 - 50, 10), color="red")
    
    def draw_game_over(self):
        screen.fill((50, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=60, color="red")
        screen.draw.text("Press R to Restart", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")
    
    def start_game(self):
        self.state = "playing"
        self.reset_game()
    
    def reset_game(self):
        self.hero = Hero()
        self.enemies.clear()
        self.enemy_spawn_timer = 0
    
    def game_over(self):
        self.state = "game_over"
        music.stop()
        sounds.game_over.play()
    
    def toggle_music(self):
        if music.is_playing("background_music"):
            music.stop()
        else:
            music.play("background_music")

# Inicialização do jogo
game = Game()

def update():
    game.update()

def draw():
    game.draw()

def on_key_down(key):
    if game.state == "menu":
        if key == keys.SPACE:
            game.start_game()
        elif key == keys.M:
            game.toggle_music()
        elif key == keys.ESCAPE:
            exit()
    elif game.state == "playing":
        if key == keys.UP:
            game.hero.jump()
    elif game.state == "game_over" and key == keys.R:
        game.start_game()

pgzrun.go()