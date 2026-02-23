import pygame as p, random, time, math

# Функция pr нужна для нахождения пути к файлам
def pr(n):
    return __file__.replace('FireKill.py', n)

p.init()
screen = p.display.set_mode((1550, 800))
p.display.set_caption('FireKill')
icon = p.image.load(pr(r'images\icon.png')).convert_alpha()
p.display.set_icon(icon)

p.mixer.init()

# Загрузка звуков
game_over_sound = p.mixer.Sound(pr(r'sounds\mus_gm.mp3'))
game_over_sound_played = False

music_bg_path = pr(r'sounds\game_music.mp3')  
p.mixer.music.load(music_bg_path)
p.mixer.music.play(-1)
music_playing = True

# Загрузка изображений
player1_sk1 = p.image.load(pr(r'images\player1_sk1.png')).convert_alpha()
player1_sk1 = p.transform.scale(player1_sk1, (100, 180))

player2_sk1 = p.image.load(pr(r'images\player2_sk1.png')).convert_alpha()
player2_sk1 = p.transform.scale(player2_sk1, (130, 180))

player1_sk2 = p.image.load(pr(r'images\player1_sk2.png')).convert_alpha()
player1_sk2 = p.transform.scale(player1_sk2, (110, 200))

player2_sk2 = p.image.load(pr(r'images\player2_sk2.png')).convert_alpha()
player2_sk2 = p.transform.scale(player2_sk2, (110, 200))

enemy_img = p.image.load(pr(r'images\enemy.png')).convert_alpha()
enemy_img = p.transform.scale(enemy_img, (200, 220))

fast_enemy_img = p.image.load(pr(r'images\enemy.png')).convert_alpha()
fast_enemy_img = p.transform.scale(fast_enemy_img, (150, 150))
fast_enemy_img.fill((255, 255, 0, 255), special_flags=p.BLEND_RGBA_MULT)

tank_enemy_img = p.image.load(pr(r'images\enemy.png')).convert_alpha()
tank_enemy_img = p.transform.scale(tank_enemy_img, (250, 250))
tank_enemy_img.fill((255, 0, 0, 255), special_flags=p.BLEND_RGBA_MULT)

boss_img = p.image.load(pr(r'images\enemy.png')).convert_alpha()
boss_img = p.transform.scale(boss_img, (300, 300))
boss_img.fill((128, 0, 128, 255), special_flags=p.BLEND_RGBA_MULT)

h1 = p.image.load(pr(r'images\heart_1.png')).convert_alpha()
h1 = p.transform.scale(h1, (150, 100))

h2 = p.image.load(pr(r'images\heart_2.png')).convert_alpha()
h2 = p.transform.scale(h2, (150, 100))

h3 = p.image.load(pr(r'images\heart_3.png')).convert_alpha()
h3 = p.transform.scale(h3, (150, 100))

coin_img = p.image.load(pr(r'images\coin.png')).convert_alpha()
coin_img = p.transform.scale(coin_img, (100, 60))

shop_icon = p.image.load(pr(r'images\shop.png')).convert_alpha()
shop_icon = p.transform.scale(shop_icon, (150, 100))

shop_bg = p.image.load(pr(r'images\back_ground.jpg')).convert_alpha()
shop_bg = p.transform.scale(shop_bg, (1550, 800))

bg = p.image.load(pr(r'images\back_ground.jpg')).convert_alpha()
bg = p.transform.scale(bg, (1550, 800))

go = p.image.load(pr(r'images\game_over.png')).convert_alpha()
go = p.transform.scale(go, (1550, 800))

fireball1 = p.image.load(pr(r'images\fireball1.png')).convert_alpha()
fireball1 = p.transform.scale(fireball1, (100, 100))

fireball2 = p.image.load(pr(r'images\fireball2.png')).convert_alpha()
fireball2 = p.transform.scale(fireball2, (100, 100))

# Шрифты
font = p.font.SysFont('Arial', 30)
big_font = p.font.SysFont('Arial', 50)
small_font = p.font.SysFont('Arial', 24)

clock = p.time.Clock()

COIN_MIN_X = 0
COIN_MAX_X = 1000
COIN_MIN_Y = 10
COIN_MAX_Y = 550

# Статистика для достижений
game_stats = {
    "enemies_killed": 0,
    "fireballs_shot": 0,
    "coins_collected_total": 0,
    "powerups_collected": 0,
    "damage_taken": 0,
    "max_combo": 0,
    "bosses_killed": 0,
    "tanks_killed": 0,
    "fast_enemies_killed": 0,
    "time_survived": 0,
    "near_misses": 0,
    "perfect_levels": 0,
    "rapid_kills": 0,
    "no_miss_shots": 0,
    "close_calls": 0,
    "shop_purchases": 0,
    "skin_changes": 0,
    "control_switches": 0
}

# Классы
class Fireball:
    def __init__(self, x, y, skin_set):
        self.x = x
        self.y = y
        self.speed = 15
        self.active = True
        self.width = 100
        self.height = 100
        self.skin_set = skin_set
    
    def update(self):
        self.x += self.speed
        if self.x > 1550:
            self.active = False
    
    def draw(self):
        if self.skin_set == 1:
            screen.blit(fireball1, (self.x, self.y))
        else:
            screen.blit(fireball2, (self.x, self.y))
    
    def get_rect(self):
        return p.Rect(self.x, self.y, self.width, self.height)

class Coin:
    def __init__(self, x, y):
        self.x = max(COIN_MIN_X, min(x, COIN_MAX_X))
        self.y = max(COIN_MIN_Y, min(y, COIN_MAX_Y))
        self.speed = 3
        self.active = True
        self.width = 50
        self.height = 50
        self.value = 5
        self.magnet_attracted = False  # Флаг для магнита
        self.magnet_speed = 8  # Скорость притяжения
    
    def update(self):
        # Если монета притягивается магнитом
        if self.magnet_attracted:
            # Вычисляем направление к игроку
            dx = (x + 50) - (self.x + 25)
            dy = (y + 90) - (self.y + 25)
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Нормализуем вектор и умножаем на скорость
                dx = dx / distance * self.magnet_speed
                dy = dy / distance * self.magnet_speed
                
                self.x += dx
                self.y += dy
                
                # Если монета очень близко к игроку, собираем её
                if distance < 30:
                    self.active = False
                    return True
        else:
            # Обычное движение монеты
            self.y += self.speed
            if self.y > 800:
                self.active = False
        return False
    
    def draw(self):
        screen.blit(coin_img, (self.x, self.y))
    
    def get_rect(self):
        return p.Rect(self.x, self.y, self.width, self.height)
    
    def activate_magnet(self):
        self.magnet_attracted = True
        self.magnet_speed = 12  # Увеличиваем скорость притяжения

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.active = True
        self.width = 200
        self.height = 220
        self.has_dropped_coin = False
        self.value = 10
        self.type = "normal"
    
    def update(self):
        self.x -= self.speed
        if self.x < -200:
            self.active = False
    
    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))
    
    def get_rect(self):
        return p.Rect(self.x, self.y, self.width, self.height)
    
    def hit(self):
        self.active = False
        game_stats["enemies_killed"] += 1
        return True
    
    def drop_coin(self, coins):
        if not self.has_dropped_coin:
            if (COIN_MIN_X <= self.x + 75 <= COIN_MAX_X and
                COIN_MIN_Y <= self.y + 100 <= COIN_MAX_Y):
                coins.append(Coin(self.x + 75, self.y + 100))
            else:
                coin_x = max(COIN_MIN_X, min(self.x + 75, COIN_MAX_X))
                coin_y = max(COIN_MIN_Y, min(self.y + 100, COIN_MAX_Y))
                coins.append(Coin(coin_x, coin_y))
            self.has_dropped_coin = True

class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.width = 150
        self.height = 150
        self.value = 15
        self.type = "fast"
    
    def draw(self):
        screen.blit(fast_enemy_img, (self.x, self.y))
    
    def hit(self):
        self.active = False
        game_stats["fast_enemies_killed"] += 1
        return True

class TankEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 2
        self.width = 250
        self.height = 250
        self.health = 2
        self.max_health = 2
        self.value = 20
        self.type = "tank"
    
    def draw(self):
        screen.blit(tank_enemy_img, (self.x, self.y))
        health_width = 100 * (self.health / self.max_health)
        p.draw.rect(screen, (255, 0, 0), (self.x + 75, self.y - 15, 100, 8))
        p.draw.rect(screen, (0, 255, 0), (self.x + 75, self.y - 15, health_width, 8))
    
    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.active = False
            game_stats["tanks_killed"] += 1
            return True
        return False

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.active = True
        self.width = 300
        self.height = 300
        self.health = 5
        self.max_health = 5
        self.has_dropped_coin = False
        self.value = 100
        self.type = "boss"
    
    def update(self):
        self.x -= self.speed
        if self.x < -300:
            self.active = False
    
    def draw(self):
        screen.blit(boss_img, (self.x, self.y))
        health_width = 200 * (self.health / self.max_health)
        p.draw.rect(screen, (255, 0, 0), (self.x + 50, self.y - 20, 200, 10))
        p.draw.rect(screen, (0, 255, 0), (self.x + 50, self.y - 20, health_width, 10))
    
    def get_rect(self):
        return p.Rect(self.x, self.y, self.width, self.height)
    
    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.active = False
            game_stats["bosses_killed"] += 1
            return True
        return False
    
    def drop_coin(self, coins):
        if not self.has_dropped_coin:
            for i in range(3):
                coin_x = max(COIN_MIN_X, min(self.x + 75 + i*40, COIN_MAX_X))
                coin_y = max(COIN_MIN_Y, min(self.y + 100, COIN_MAX_Y))
                coins.append(Coin(coin_x, coin_y))
            self.has_dropped_coin = True

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.speed = 4
        self.active = True
        self.width = 60
        self.height = 60
        self.type = type
        self.duration = 360
    
    def update(self):
        self.y += self.speed
        if self.y > 800:
            self.active = False
    
    def draw(self):
        # Сопоставление русских названий с цветами
        color_map = {
            "Ускоренная перезарядка": (255, 0, 0),
            "Щит": (0, 0, 255),
            "Доп. очки": (0, 255, 0),
            "Магнит": (255, 165, 0)  # ОРАНЖЕВЫЙ ДЛЯ МАГНИТА
        }
        color = color_map.get(self.type, (255, 255, 255))  # Белый по умолчанию
        
        # Рисуем круг бонуса
        p.draw.circle(screen, color, (self.x + 30, self.y + 30), 30)
        
        # Сокращения и настройки текста для разных типов бонусов
        type_settings = {
            "Ускоренная перезарядка": {"text": "УП", "color": (255, 255, 255), "offset_x": 15, "offset_y": 15},
            "Щит": {"text": "ЩТ", "color": (255, 255, 255), "offset_x": 13, "offset_y": 18},
            "Доп. очки": {"text": "X2", "color": (0, 0, 0), "offset_x": 18, "offset_y": 18},
            "Магнит": {"text": "МГ", "color": (255, 255, 255), "offset_x": 15, "offset_y": 18}  # МАГНИТ
        }
        
        settings = type_settings.get(self.type, {"text": self.type[:2], "color": (255, 255, 255), "offset_x": 20, "offset_y": 25})
        
        type_text = small_font.render(settings["text"], True, settings["color"])
        screen.blit(type_text, (self.x + settings["offset_x"], self.y + settings["offset_y"]))
    
    def get_rect(self):
        return p.Rect(self.x, self.y, self.width, self.height)
    
class Achievement:
    def __init__(self, name, description, condition, reward):
        self.name = name
        self.description = description
        self.condition = condition
        self.reward = reward
        self.achieved = False
        self.show_timer = 0

class Button:
    def __init__(self, x, y, width, height, text, price, action):
        self.rect = p.Rect(x, y, width, height)
        self.text = text
        self.price = price
        self.action = action
        self.color = (100, 100, 200)
        self.hover_color = (150, 150, 250)
        self.is_hovered = False
        self.border_radius = 15

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        p.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        p.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=self.border_radius)
        if self.price:
            text_surface = font.render(f"{self.text} - {self.price} монет", True, (255, 255, 255))
        else:
            text_surface = font.render(f"{self.text}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def check_click(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class ControlButton:
    def __init__(self, x, y, width, height, text):
        self.rect = p.Rect(x, y, width, height)
        self.text = text
        self.color = (100, 100, 200)
        self.hover_color = (150, 150, 250)
        self.is_hovered = False
        self.selected = False
    
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        if self.selected:
            color = (0, 200, 0)
        p.draw.rect(screen, color, self.rect, border_radius=10)
        p.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def check_click(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class ScrollableArea:
    def __init__(self, x, y, width, height, content_height):
        self.rect = p.Rect(x, y, width, height)
        self.content_height = content_height
        self.scroll_y = 0
        self.scrollbar_width = 20
        self.is_dragging = False
        self.drag_offset = 0
    
    def get_scroll_ratio(self):
        return self.scroll_y / (self.content_height - self.rect.height)
    
    def set_scroll_from_ratio(self, ratio):
        self.scroll_y = max(0, min(ratio * (self.content_height - self.rect.height), self.content_height - self.rect.height))
    
    def handle_event(self, event, mouse_pos):
        if event.type == p.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_y = max(0, self.scroll_y - 30)
                return True
            elif event.button == 5:  # Scroll down
                self.scroll_y = max(0, min(self.scroll_y + 30, self.content_height - self.rect.height))
                return True
            elif event.button == 1:  # Left click
                scrollbar_rect = p.Rect(
                    self.rect.right - self.scrollbar_width,
                    self.rect.top + (self.rect.height - 50) * self.get_scroll_ratio(),
                    self.scrollbar_width,
                    50
                )
                if scrollbar_rect.collidepoint(mouse_pos):
                    self.is_dragging = True
                    self.drag_offset = mouse_pos[1] - scrollbar_rect.top
                    return True
        
        elif event.type == p.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
                return True
        
        elif event.type == p.MOUSEMOTION:
            if self.is_dragging:
                new_y = mouse_pos[1] - self.drag_offset
                scroll_ratio = (new_y - self.rect.top) / (self.rect.height - 50)
                self.set_scroll_from_ratio(max(0, min(scroll_ratio, 1)))
                return True
        
        return False
    
    def draw_scrollbar(self):
        if self.content_height > self.rect.height:
            scrollbar_height = max(50, self.rect.height * (self.rect.height / self.content_height))
            scrollbar_y = self.rect.top + (self.rect.height - scrollbar_height) * self.get_scroll_ratio()
            
            scrollbar_rect = p.Rect(
                self.rect.right - self.scrollbar_width,
                scrollbar_y,
                self.scrollbar_width,
                scrollbar_height
            )
            p.draw.rect(screen, (150, 150, 150), scrollbar_rect)
            p.draw.rect(screen, (0, 0, 0), scrollbar_rect, 1)

# Игровые переменные
running = True
game_over = False
shop_open = False
show_instructions = True
x = 0
y = 230
fireballs = []
enemies = []
coins = []
powerups = []
speed = 15
fire_cooldown_max = 60
fire_cooldown = 0
can_fire = True
current_skin = player1_sk1
shooting_animation_time = 0
score = 0
final_time = 0 
coins_collected = 0
enemy_spawn_timer = 0
powerup_timer = 0
lives = 3
invulnerability_timer = 0
extra_lives = 0
current_skin_set = 1
skin2_unlocked = False
begin_time = round(time.time())
final_time = 0
coin_multiplier = 1
coin_multiplier_unlocked = False
mouse_control = False
music_key_pressed = False

# Система комбо
combo = 0
combo_timer = 0
combo_multiplier = 1

# Система боссов и уровней
boss_spawn_timer = 0
boss_active = False
boss = None
level = 1

# Активные бонусы
active_powerups = {}

# Достижения (32 достижения)
achievements = [
    # Базовые достижения
    Achievement("Первый шаг", "Наберите 100 очков", lambda: score >= 100, 10),
    Achievement("Коллекционер", "Соберите 50 монет", lambda: coins_collected >= 50, 25),
    Achievement("Снайпер", "Уничтожьте 20 врагов", lambda: game_stats["enemies_killed"] >= 20, 30),
    Achievement("Неуязвимый", "Проживите 60 секунд без повреждений", 
                lambda: game_stats["time_survived"] >= 60 and game_stats["damage_taken"] == 0, 50),
    Achievement("Босс-победитель", "Победите босса", lambda: game_stats["bosses_killed"] >= 1, 100),
    Achievement("Мастер комбо", "Соберите комбо x5", lambda: combo_multiplier >= 5, 75),
    Achievement("Богач", "Соберите 200 монет", lambda: coins_collected >= 200, 100),
    Achievement("Скорострел", "Сделайте 50 выстрелов", lambda: game_stats["fireballs_shot"] >= 50, 40),
    Achievement("Выживший", "Проживите 3 минуты", lambda: game_stats["time_survived"] >= 180, 80),
    Achievement("Охотник за скинами", "Купите новый скин", lambda: skin2_unlocked, 60),
    Achievement("Улучшенный", "Купите 3 улучшения", lambda: speed_level + fire_rate_level >= 3, 70),
    Achievement("Легенда", "Наберите 1000 очков", lambda: score >= 1000, 150),
    Achievement("Танкобойца", "Уничтожьте 10 танков", lambda: game_stats["tanks_killed"] >= 10, 80),
    Achievement("Спринтер", "Уничтожьте 25 быстрых врагов", lambda: game_stats["fast_enemies_killed"] >= 25, 90),
    Achievement("Ниндзя", "Проживите 30 секунд не получив урон", 
                lambda: game_stats["time_survived"] >= 30 and game_stats["damage_taken"] == 0, 120),
    Achievement("Бонус-мания", "Соберите 15 бонусов", lambda: game_stats["powerups_collected"] >= 15, 100),
    Achievement("Комбо-король", "Достигните комбо x10", lambda: game_stats["max_combo"] >= 10, 200),
    Achievement("Молниеносный", "Уничтожьте 5 врагов за 10 секунд", 
                lambda: game_stats["rapid_kills"] >= 5, 150),
    Achievement("Снайпер-ас", "Попадите 10 раз подряд без промаха", 
                lambda: game_stats["no_miss_shots"] >= 10, 130),
    Achievement("Уворачиватель", "Избегайте 20 близких столкновений", 
                lambda: game_stats["near_misses"] >= 20, 110),
    Achievement("Магазинный маньяк", "Совершите 10 покупок в магазине", 
                lambda: game_stats["shop_purchases"] >= 10, 180),
    Achievement("Мультимиллионер", "Соберите 1000 монет за всю игру", 
                lambda: game_stats["coins_collected_total"] >= 1000, 250),
    Achievement("Неудержимый", "Достигните 10 уровня", lambda: level >= 10, 300),
    Achievement("Босс-охотник", "Уничтожьте 5 боссов", lambda: game_stats["bosses_killed"] >= 5, 400),
    Achievement("Идеальный уровень", "Пройдите уровень без получения урона", 
                lambda: game_stats["perfect_levels"] >= 1, 160),
    Achievement("Хамелеон", "Смените скин 5 раз", lambda: game_stats["skin_changes"] >= 5, 90),
    Achievement("Универсал", "Используйте оба режима управления", 
                lambda: game_stats["control_switches"] >= 2, 120),
    Achievement("Феникс", "Восстановите все жизни после их потери", 
                lambda: lives == 3 and game_stats["damage_taken"] > 0, 140),
    Achievement("Экономист", "Накопите 500 монет не тратя их", 
                lambda: coins_collected >= 500 and game_stats["shop_purchases"] == 0, 220),
    Achievement("Непробиваемый", "Активируйте щит 5 раз", 
                lambda: sum(1 for p_type in active_powerups if p_type == "Щит") >= 5, 100),
    Achievement("Мастер огня", "Сделайте 1000 выстрелов", lambda: game_stats["fireballs_shot"] >= 1000, 350),
    Achievement("Бессмертный", "Проживите 10 минут", lambda: game_stats["time_survived"] >= 600, 500)
]

# Информация о врагах
enemy_info = [
    {
        "name": "Обычный враг",
        "image": enemy_img,
        "speed": "Средняя",
        "health": "1 удар",
        "reward": "10 очков",
        "description": "Базовый противник"
    },
    {
        "name": "Быстрый враг",
        "image": p.transform.scale(fast_enemy_img, (200, 220)),
        "speed": "Высокая",
        "health": "1 удар", 
        "reward": "15 очков",
        "description": "Быстро движется, сложно попасть"
    },
    {
        "name": "Танк",
        "image": p.transform.scale(tank_enemy_img, (200, 220)),
        "speed": "Низкая",
        "health": "2 удара",
        "reward": "20 очков",
        "description": "Медленный, но прочный"
    },
    {
        "name": "Босс",
        "image": p.transform.scale(boss_img, (200, 220)),
        "speed": "Средняя",
        "health": "5 ударов",
        "reward": "100 очков + 3 монеты",
        "description": "Опасный босс, появляется редко"
    }
]

# Ограничения по уровням для улучшений
speed_level = 0
max_speed_level = 3
fire_rate_level = 0
max_fire_rate_level = 4

# Списки скинов
sk1 = [player1_sk1, player2_sk1]
sk2 = [player1_sk2, player2_sk2]
skins = sk1

# Создаем кнопки магазина
shop_buttons = [
    Button(470, 200, 600, 60, "Увеличить скор. стрельбы", 50, "faster_fire"),
    Button(470, 300, 600, 60, "Дополнительная жизнь", 100, "extra_life"),
    Button(470, 400, 600, 60, "Увеличить скорость игрока", 75, "faster_move"),
    Button(470, 500, 600, 60, "Купить скин для игрока", 200, "buy_skin2"),
    Button(470, 600, 600, 60, "x2 монеты навсегда", 300, "coin_multiplier"),
    Button(470, 700, 600, 60, "Закрыть магазин", 0, "close_shop")
]

# Новые кнопки для вкладок
tab_buttons = [
    Button(260, 130, 300, 60, "УЛУЧШЕНИЯ", 0, "tab_upgrades"),
    Button(610, 130, 300, 60, "ДОСТИЖЕНИЯ", 0, "tab_achievements"),
    Button(960, 130, 300, 60, "ИНФО О ВРАГАХ", 0, "tab_enemies")
]

control_buttons = [
    ControlButton(300, 430, 320, 60, "Клавиатура (стрелки)"),
    ControlButton(900, 430, 250, 60, "Мышь")
]

# Переменные магазина
not_enough_coins_message = ""
not_enough_coins_timer = 0
current_shop_tab = 0  # 0-улучшения, 1-достижения, 2-враги

# Области для скролла
achievements_scroll = ScrollableArea(200, 250, 1150, 450, len(achievements) * 80)
enemies_scroll = ScrollableArea(200, 250, 1150, 450, len(enemy_info) * 150)

# Переменные для отслеживания времени
last_shot_time = 0
last_enemy_kill_time = 0
consecutive_hits = 0
last_damage_time = begin_time
last_achievement_check_time = begin_time

# ФУНКЦИЯ ДЛЯ РАСЧЕТА СЛОЖНОСТИ В ЗАВИСИМОСТИ ОТ УРОВНЯ
def get_level_difficulty():
    """Возвращает параметры сложности в зависимости от уровня"""
    base_spawn_rate = 120  # Базовый таймер спавна
    min_spawn_rate = 40   # Минимальный таймер спавна
    
    # Уменьшаем таймер спавна с каждым уровнем (враги появляются чаще)
    spawn_timer = max(min_spawn_rate, base_spawn_rate - level * 8)
    
    # Увеличиваем шанс появления сложных врагов
    if level <= 3:
        enemy_weights = [0.6, 0.3, 0.1, 0.0]  # обычные, быстрые, танки, боссы
    elif level <= 6:
        enemy_weights = [0.4, 0.4, 0.2, 0.0]
    elif level <= 9:
        enemy_weights = [0.3, 0.4, 0.3, 0.0]
    elif level <= 12:
        enemy_weights = [0.2, 0.4, 0.3, 0.1]
    else:
        enemy_weights = [0.1, 0.3, 0.4, 0.2]
    
    # Увеличиваем скорость врагов с уровнем
    speed_multiplier = 1.0 + (level - 1) * 0.1
    
    return spawn_timer, enemy_weights, speed_multiplier

#! Главный цикл игры
while running:
    mouse_clicked = False
    mouse_pos = p.mouse.get_pos()
    
    # Обновление статистики времени (только когда игра активна, не в магазине)
    current_time = round(time.time())
    if not shop_open and not game_over and not show_instructions:
        game_stats["time_survived"] = current_time - begin_time
    game_stats["max_combo"] = max(game_stats["max_combo"], combo_multiplier)
    
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        if event.type == p.MOUSEBUTTONDOWN:
            mouse_clicked = True
            
        if game_over and event.type == p.KEYDOWN:
            if event.key == p.K_r:
                # Сброс игры
                game_over = False
                game_over_sound_played = False  # Сброс флага звука проигрыша
                x, y = 0, 200
                fireballs, enemies, coins, powerups = [], [], [], []
                speed, fire_cooldown_max = 15, 60
                fire_cooldown, can_fire = 0, True
                current_skin = player1_sk1
                shooting_animation_time, score, coins_collected = 0, 0, 0
                enemy_spawn_timer, powerup_timer = 0, 0
                lives, invulnerability_timer, extra_lives = 3, 0, 0
                current_skin_set, skins = 1, sk1
                begin_time, final_time = round(time.time()), 0
                speed_level, fire_rate_level = 0, 0
                music_key_pressed = False
                combo, combo_timer, combo_multiplier = 0, 0, 1
                boss_spawn_timer, boss_active, boss, level = 0, False, None, 1
                active_powerups = {}
                
                # Сброс статистики
                for stat in game_stats:
                    game_stats[stat] = 0
                
                for achievement in achievements:
                    achievement.achieved = False
                    achievement.show_timer = 0
                
                # ВОССТАНАВЛИВАЕМ МУЗЫКУ ПРИ ПЕРЕЗАПУСКЕ
                p.mixer.music.play(-1)
                music_playing = True

        keys = p.key.get_pressed()
        if keys[p.K_m] and not music_key_pressed:
            music_key_pressed = True
            if music_playing:
                p.mixer.music.pause()
                music_playing = False
            else:
                p.mixer.music.unpause()
                music_playing = True
        elif not keys[p.K_m]:
            music_key_pressed = False

        # Обработка скролла в магазине
        if shop_open:
            if current_shop_tab == 1:  # Достижения
                achievements_scroll.handle_event(event, mouse_pos)
            elif current_shop_tab == 2:  # Враги
                enemies_scroll.handle_event(event, mouse_pos)

    if show_instructions:
        # Экран инструкции
        screen.blit(bg, (0, 0))
        title_text = big_font.render("FireKill - Инструкция", True, (255, 0, 0))
        screen.blit(title_text, (500, 50))
        
        instructions = [
            "Цель: уничтожать врагов, собирать монеты, выживать.",
            "Жизни: 3 штуки, при потере — короткая неуязвимость.",
            "Магазин (иконка вверху справа): улучшения, скины, множитель монет. итд",
            "Враги: обычные, быстрые, танки, босс (у каждого своя прочность и награда).",
            "Бонусы: дают временные эффекты (ускорение, щит, ×2 очков, магнит).", "",
            "Выберите способ управления:"
        ]
        
        for i, line in enumerate(instructions):
            instr_text = small_font.render(line, True, (255, 255, 255))
            screen.blit(instr_text, (300, 150 + i * 30))
        
        key_text = small_font.render("Клавиатура: Стрелки/WASD - движение, Пробел - стрельба", True, (255, 255, 255))
        screen.blit(key_text, (800, 320))
        mouse_text = small_font.render("Мышь: Движение - курсор, ЛКМ - стрельба", True, (255, 255, 255))
        screen.blit(mouse_text, (800, 350))
        
        for button in control_buttons:
            button.check_hover(mouse_pos)
            button.draw()
            if mouse_clicked and button.check_click(mouse_pos, True):
                if button.text == "Клавиатура (стрелки)":
                    mouse_control = False
                    control_buttons[0].selected = True
                    control_buttons[1].selected = False
                    game_stats["control_switches"] += 1
                else:
                    mouse_control = True
                    control_buttons[0].selected = False
                    control_buttons[1].selected = True
                    game_stats["control_switches"] += 1
        
        # Кнопка "НАЧАТЬ ИГРУ" с увеличенным скруглением
        start_button = p.Rect(520, 570, 460, 80)
        p.draw.rect(screen, (0, 150, 0), start_button, border_radius=25)  # Увеличено скругление
        p.draw.rect(screen, (0, 0, 0), start_button, 3, border_radius=25)
        start_text = big_font.render("НАЧАТЬ ИГРУ", True, (255, 255, 255))
        screen.blit(start_text, (585, 583))
        text_or = big_font.render('ИЛИ', True, 'white')
        screen.blit(text_or, (700, 430))

        if mouse_clicked and start_button.collidepoint(mouse_pos):
            show_instructions = False
            
    elif shop_open:
        # Отрисовка магазина
        screen.blit(shop_bg, (0, 0))
        
        title_text = big_font.render("МАГАЗИН", True, (255, 215, 0))
        screen.blit(title_text, (650, 10))
        
        coins_text = big_font.render(f"Монеты: {coins_collected}", True, (255, 215, 0))
        screen.blit(coins_text, (650, 70))
        
        # Отрисовка кнопок вкладок
        for button in tab_buttons:
            # Подсветка активной вкладки
            if (button.action == "tab_upgrades" and current_shop_tab == 0) or \
               (button.action == "tab_achievements" and current_shop_tab == 1) or \
               (button.action == "tab_enemies" and current_shop_tab == 2):
                button.color = (150, 150, 250)
            else:
                button.color = (100, 100, 200)
                
            button.check_hover(mouse_pos)
            button.draw()
            
            if mouse_clicked and button.check_click(mouse_pos, True):
                if button.action == "tab_upgrades":
                    current_shop_tab = 0
                elif button.action == "tab_achievements":
                    current_shop_tab = 1
                elif button.action == "tab_enemies":
                    current_shop_tab = 2
        
        if current_shop_tab == 0:  # Улучшения
            if skin2_unlocked:
                unlocked_text = font.render("2 скин разблокирован!", True, (0, 255, 0))
                screen.blit(unlocked_text, (600, 210))
            
            # Отрисовка кнопок улучшений
            for button in shop_buttons:
                if button.action == "buy_skin2" and skin2_unlocked:
                    button.text = "Переключить скин"
                    button.price = 0
                elif button.action == "buy_skin2" and not skin2_unlocked:
                    button.text = "Купить скин для игрока"
                    button.price = 200
                    
                if button.action == "coin_multiplier" and coin_multiplier_unlocked:
                    button.text = "x2 монеты активирован"
                    button.price = 0
                elif button.action == "coin_multiplier" and not coin_multiplier_unlocked:
                    button.text = "x2 монеты навсегда"
                    button.price = 300
                    
                if button.action == "faster_move":
                    if speed_level >= max_speed_level:
                        button.text = "Скорость макс. уровень"
                        button.price = 0
                    else:
                        button.text = f"Увеличить скорость (ур. {speed_level + 1}/{max_speed_level})"
                        button.price = 75 + speed_level * 25
                        
                if button.action == "faster_fire":
                    if fire_rate_level >= max_fire_rate_level:
                        button.text = "Скорострельность макс. уровень"
                        button.price = 0
                    else:
                        button.text = f"Увел. перезарядку (ур. {fire_rate_level + 1}/{max_fire_rate_level})"
                        button.price = 50 + fire_rate_level * 20
                    
                button.check_hover(mouse_pos)
                button.draw()
                
                if mouse_clicked and button.check_click(mouse_pos, True):
                    if button.action == "close_shop":
                        shop_open = False
                    elif button.action == "extra_life":
                        if coins_collected >= button.price:
                            coins_collected -= button.price
                            lives += 1
                            extra_lives += 1
                            game_stats["shop_purchases"] += 1
                        else:
                            not_enough_coins_message = "Недостаточно монет!"
                            not_enough_coins_timer = 120
                    elif button.action == "faster_fire":
                        if fire_rate_level < max_fire_rate_level:
                            if coins_collected >= button.price:
                                coins_collected -= button.price
                                fire_cooldown_max = max(10, fire_cooldown_max - 12)
                                fire_rate_level += 1
                                game_stats["shop_purchases"] += 1
                            else:
                                not_enough_coins_message = "Недостаточно монет!"
                                not_enough_coins_timer = 120
                        else:
                            not_enough_coins_message = "Максимальный уровень достигнут!"
                            not_enough_coins_timer = 120
                    elif button.action == "faster_move":
                        if speed_level < max_speed_level:
                            if coins_collected >= button.price:
                                coins_collected -= button.price
                                speed = min(30, speed + 5)
                                speed_level += 1
                                game_stats["shop_purchases"] += 1
                            else:
                                not_enough_coins_message = "Недостаточно монет!"
                                not_enough_coins_timer = 120
                        else:
                            not_enough_coins_message = "Максимальный уровень достигнут!"
                            not_enough_coins_timer = 120
                    elif button.action == "buy_skin2":
                        if not skin2_unlocked:
                            if coins_collected >= 200:
                                coins_collected -= 200
                                skin2_unlocked = True
                                game_stats["shop_purchases"] += 1
                            else:
                                not_enough_coins_message = "Недостаточно монет!"
                                not_enough_coins_timer = 120
                        else:
                            if current_skin_set == 1:
                                current_skin_set = 2
                                skins = sk2
                                current_skin = sk2[0]
                            else:
                                current_skin_set = 1
                                skins = sk1
                                current_skin = sk1[0]
                            game_stats["skin_changes"] += 1
                    elif button.action == "coin_multiplier":
                        if not coin_multiplier_unlocked:
                            if coins_collected >= 300:
                                coins_collected -= 300
                                coin_multiplier = 2
                                coin_multiplier_unlocked = True
                                game_stats["shop_purchases"] += 1
                            else:
                                not_enough_coins_message = "Недостаточно монет!"
                                not_enough_coins_timer = 120
        
        elif current_shop_tab == 1:  # Достижения
            # Отрисовка кнопки закрытия магазина
            buttoncl = Button(470, 710, 600, 60, "Закрыть магазин", 0, "close_shop")
            buttoncl.draw()
            if mouse_clicked and buttoncl.check_click(mouse_pos, True):
                shop_open = False

            # Область для скролла достижений
            scroll_area = p.Rect(200, 250, 1150, 450, border_radius = 15)
            p.draw.rect(screen, (50, 50, 80), scroll_area)
            p.draw.rect(screen, (255, 215, 0), scroll_area, 2)
            
            # Сохраняем область отрисовки
            clip_rect = screen.get_clip()
            screen.set_clip(scroll_area)
            
            achievement_y = 250 - achievements_scroll.scroll_y
            for achievement in achievements:
                if achievement_y + 80 > 250 and achievement_y < 700:  # Только видимые достижения
                    achievement_bg = p.Rect(210, achievement_y, 1130, 70, border_radius = 15)
                    if achievement.achieved:
                        p.draw.rect(screen, (50, 150, 50), achievement_bg)
                        status_text = "ВЫПОЛНЕНО"
                        status_color = (0, 255, 0)
                    else:
                        p.draw.rect(screen, (80, 80, 80), achievement_bg)
                        status_text = "В ПРОЦЕССЕ"
                        status_color = (200, 200, 200)
                    
                    p.draw.rect(screen, (0, 0, 0), achievement_bg, 2)
                    
                    name_text = font.render(achievement.name, True, (255, 255, 255))
                    desc_text = small_font.render(achievement.description, True, (200, 200, 200))
                    status_surface = small_font.render(status_text, True, status_color)
                    reward_text = small_font.render(f"Награда: +{achievement.reward} монет", True, (255, 215, 0))
                    
                    screen.blit(name_text, (220, achievement_y + 10))
                    screen.blit(desc_text, (220, achievement_y + 40))
                    screen.blit(status_surface, (810, achievement_y + 10))
                    screen.blit(reward_text, (1100, achievement_y + 25))
                    
                    # ОТОБРАЖЕНИЕ ПРОГРЕССА ДЛЯ НЕВЫПОЛНЕННЫХ ДОСТИЖЕНИЙ
                    if not achievement.achieved:
                        # Получаем текущее значение прогресса
                        progress_value = 0
                        if achievement.name == "Первый шаг":
                            progress_value = min(score, 100)
                        elif achievement.name == "Коллекционер":
                            progress_value = min(coins_collected, 50)
                        elif achievement.name == "Снайпер":
                            progress_value = min(game_stats["enemies_killed"], 20)
                        elif achievement.name == "Неуязвимый":
                            progress_value = min(game_stats["time_survived"], 60)
                        elif achievement.name == "Босс-победитель":
                            progress_value = min(game_stats["bosses_killed"], 1)
                        elif achievement.name == "Мастер комбо":
                            progress_value = min(game_stats["max_combo"], 5)
                        elif achievement.name == "Богач":
                            progress_value = min(coins_collected, 200)
                        elif achievement.name == "Скорострел":
                            progress_value = min(game_stats["fireballs_shot"], 50)
                        elif achievement.name == "Выживший":
                            progress_value = min(game_stats["time_survived"], 180)
                        elif achievement.name == "Охотник за скинами":
                            progress_value = 1 if skin2_unlocked else 0
                        elif achievement.name == "Улучшенный":
                            progress_value = min(speed_level + fire_rate_level, 3)
                        elif achievement.name == "Легенда":
                            progress_value = min(score, 1000)
                        elif achievement.name == "Танкобойца":
                            progress_value = min(game_stats["tanks_killed"], 10)
                        elif achievement.name == "Спринтер":
                            progress_value = min(game_stats["fast_enemies_killed"], 25)
                        elif achievement.name == "Ниндзя":
                            progress_value = min(game_stats["time_survived"], 30)
                        elif achievement.name == "Бонус-мания":
                            progress_value = min(game_stats["powerups_collected"], 15)
                        elif achievement.name == "Комбо-король":
                            progress_value = min(game_stats["max_combo"], 10)
                        elif achievement.name == "Молниеносный":
                            progress_value = min(game_stats["rapid_kills"], 5)
                        elif achievement.name == "Снайпер-ас":
                            progress_value = min(game_stats["no_miss_shots"], 10)
                        elif achievement.name == "Уворачиватель":
                            progress_value = min(game_stats["near_misses"], 20)
                        elif achievement.name == "Магазинный маньяк":
                            progress_value = min(game_stats["shop_purchases"], 10)
                        elif achievement.name == "Мультимиллионер":
                            progress_value = min(game_stats["coins_collected_total"], 1000)
                        elif achievement.name == "Неудержимый":
                            progress_value = min(level, 10)
                        elif achievement.name == "Босс-охотник":
                            progress_value = min(game_stats["bosses_killed"], 5)
                        elif achievement.name == "Идеальный уровень":
                            progress_value = min(game_stats["perfect_levels"], 1)
                        elif achievement.name == "Хамелеон":
                            progress_value = min(game_stats["skin_changes"], 5)
                        elif achievement.name == "Универсал":
                            progress_value = min(game_stats["control_switches"], 2)
                        elif achievement.name == "Феникс":
                            progress_value = 1 if (lives == 3 and game_stats["damage_taken"] > 0) else 0
                        elif achievement.name == "Экономист":
                            progress_value = min(coins_collected, 500)
                        elif achievement.name == "Непробиваемый":
                            progress_value = min(sum(1 for p_type in active_powerups if p_type == "Щит"), 5)
                        elif achievement.name == "Мастер огня":
                            progress_value = min(game_stats["fireballs_shot"], 1000)
                        elif achievement.name == "Бессмертный":
                            progress_value = min(game_stats["time_survived"], 600)
                        
                        # Получаем целевое значение из условия
                        target_value = 0
                        if "100 очков" in achievement.description:
                            target_value = 100
                        elif "50 монет" in achievement.description:
                            target_value = 50
                        elif "20 врагов" in achievement.description:
                            target_value = 20
                        elif "60 секунд" in achievement.description:
                            target_value = 60
                        elif "Победите босса" in achievement.description:
                            target_value = 1
                        elif "комбо x5" in achievement.description:
                            target_value = 5
                        elif "200 монет" in achievement.description:
                            target_value = 200
                        elif "50 выстрелов" in achievement.description:
                            target_value = 50
                        elif "3 минуты" in achievement.description:
                            target_value = 180
                        elif "новый скин" in achievement.description:
                            target_value = 1
                        elif "3 улучшения" in achievement.description:
                            target_value = 3
                        elif "1000 очков" in achievement.description:
                            target_value = 1000
                        elif "10 танков" in achievement.description:
                            target_value = 10
                        elif "25 быстрых врагов" in achievement.description:
                            target_value = 25
                        elif "30 секунд" in achievement.description:
                            target_value = 30
                        elif "15 бонусов" in achievement.description:
                            target_value = 15
                        elif "комбо x10" in achievement.description:
                            target_value = 10
                        elif "5 врагов за 10 секунд" in achievement.description:
                            target_value = 5
                        elif "10 раз подряд" in achievement.description:
                            target_value = 10
                        elif "20 близких столкновений" in achievement.description:
                            target_value = 20
                        elif "10 покупок" in achievement.description:
                            target_value = 10
                        elif "1000 монет" in achievement.description:
                            target_value = 1000
                        elif "10 уровня" in achievement.description:
                            target_value = 10
                        elif "5 боссов" in achievement.description:
                            target_value = 5
                        elif "уровень без получения урона" in achievement.description:
                            target_value = 1
                        elif "5 раз" in achievement.description:
                            target_value = 5
                        elif "оба режима управления" in achievement.description:
                            target_value = 2
                        elif "все жизни после их потери" in achievement.description:
                            target_value = 1
                        elif "500 монет не тратя их" in achievement.description:
                            target_value = 500
                        elif "2 секунд после его появления" in achievement.description:
                            target_value = 3
                        elif "5 раз" in achievement.description and "щит" in achievement.description.lower():
                            target_value = 5
                        elif "1000 выстрелов" in achievement.description:
                            target_value = 1000
                        elif "10 минут" in achievement.description:
                            target_value = 600
                        
                        # Отображаем прогресс
                        if target_value > 0:
                            progress_percent = min(100, int((progress_value / target_value) * 100))
                            progress_text = small_font.render(f"Прогресс: {progress_value}/{target_value} ({progress_percent}%)", True, (150, 150, 150))
                            screen.blit(progress_text, ((810, achievement_y + 35)))
                
                achievement_y += 80
            
            # Восстанавливаем область отрисовки
            screen.set_clip(clip_rect)
            
            # Отрисовка скроллбара
            achievements_scroll.draw_scrollbar()
        
        else:  # Враги
            
            # Отрисовка кнопки закрытия магазина
            buttoncl = Button(470, 710, 600, 60, "Закрыть магазин", 0, "close_shop")
            buttoncl.draw()
            if mouse_clicked and buttoncl.check_click(mouse_pos, True):
                shop_open = False

             # Область для скролла врагов
            scroll_area = p.Rect(200, 250, 1150, 450, border_radius = 15)
            p.draw.rect(screen, (50, 50, 80), scroll_area)
            p.draw.rect(screen, (255, 215, 0), scroll_area, 2)
            
            # Сохраняем область отрисовки
            clip_rect = screen.get_clip()
            screen.set_clip(scroll_area)
            
            enemy_y = 250 - enemies_scroll.scroll_y
            for enemy_data in enemy_info:
                if enemy_y + 140 > 250 and enemy_y < 700:  # Только видимые враги
                    enemy_bg = p.Rect(210, enemy_y, 1130, 130, border_radius = 15)
                    p.draw.rect(screen, (60, 60, 100), enemy_bg)
                    p.draw.rect(screen, (255, 215, 0), enemy_bg, 2)
                    
                    # Изображение врага
                    screen.blit(enemy_data["image"], (220, enemy_y - 30))
                    
                    # Информация о враге
                    name_text = font.render(enemy_data["name"], True, (255, 255, 255))
                    desc_text = small_font.render(enemy_data["description"], True, (200, 200, 200))
                    speed_text = small_font.render(f"Скорость: {enemy_data['speed']}", True, (100, 255, 100))
                    health_text = small_font.render(f"Здоровье: {enemy_data['health']}", True, (255, 100, 100))
                    reward_text = small_font.render(f"Награда: {enemy_data['reward']}", True, (255, 215, 0))
                    
                    screen.blit(name_text, (450, enemy_y + 15))
                    screen.blit(desc_text, (450, enemy_y + 45))
                    screen.blit(speed_text, (450, enemy_y + 75))
                    screen.blit(health_text, (690, enemy_y + 75))
                    screen.blit(reward_text, (920, enemy_y + 75))
                
                enemy_y += 140
            
            # Восстанавливаем область отрисовки
            screen.set_clip(clip_rect)
            
            # Отрисовка скроллбара
            enemies_scroll.draw_scrollbar()
        
        # Отображение сообщения о недостатке монет
        if not_enough_coins_timer > 0:
            error_text = font.render(not_enough_coins_message, True, (255, 0, 0))
            screen.blit(error_text, (620, 660))
            not_enough_coins_timer -= 1
            
    elif not game_over:
        # Игровой процесс
        screen.blit(bg, (0, 0))
        
        keys = p.key.get_pressed()
        
        # Проверка достижений (только раз в секунду для оптимизации)
        if current_time - last_achievement_check_time >= 1.0:
            for achievement in achievements:
                if not achievement.achieved and achievement.condition():
                    achievement.achieved = True
                    achievement.show_timer = 180
                    coins_collected += achievement.reward
            last_achievement_check_time = current_time

        # Движение игрока
        if mouse_control:
            x = max(0, min(mouse_pos[0] - 50, 1000))
            y = max(10, min(mouse_pos[1] - 90, 550))
            if mouse_clicked and can_fire:
                fireballs.append(Fireball(x + 120, y + 50, current_skin_set))
                can_fire = False
                fire_cooldown = fire_cooldown_max
                shooting_animation_time = 15
                current_skin = skins[1]
                game_stats["fireballs_shot"] += 1
        else:
            if (keys[p.K_RIGHT] and x < 1000) or (keys[p.K_d] and x < 1000):
                x += speed
            if (keys[p.K_LEFT] and x > 0) or (keys[p.K_a] and x > 0): 
                x -= speed
            if (keys[p.K_DOWN] and y < 550) or (keys[p.K_s] and y < 550):
                y += speed
            if (keys[p.K_UP] and not y < 10) or (keys[p.K_w] and not y < 10): 
                y -= speed

            if keys[p.K_SPACE] and can_fire:
                fireballs.append(Fireball(x + 120, y + 50, current_skin_set))
                can_fire = False
                fire_cooldown = fire_cooldown_max
                shooting_animation_time = 15
                current_skin = skins[1]
                game_stats["fireballs_shot"] += 1
        
        if shooting_animation_time > 0:
            shooting_animation_time -= 1
            if shooting_animation_time == 0:
                current_skin = skins[0]

        if not can_fire:
            fire_cooldown -= 1
            if fire_cooldown <= 0:
                can_fire = True
                fire_cooldown = 0

        if invulnerability_timer > 0:
            invulnerability_timer -= 1

        # Спавн врагов с учетом уровня сложности
        enemy_spawn_timer += 1
        spawn_timer, enemy_weights, speed_multiplier = get_level_difficulty()
        
        if enemy_spawn_timer >= spawn_timer:
            # Выбираем тип врага с учетом весов
            enemy_type = random.choices(["normal", "fast", "tank", "boss"], weights=enemy_weights)[0]
            enemy_y = random.randint(50, 550)
            
            if enemy_type == "normal":
                enemy = Enemy(1550, enemy_y)
                enemy.speed = int(enemy.speed * speed_multiplier)
                enemies.append(enemy)
            elif enemy_type == "fast":
                enemy = FastEnemy(1550, enemy_y)
                enemy.speed = int(enemy.speed * speed_multiplier)
                enemies.append(enemy)
            elif enemy_type == "tank":
                enemy = TankEnemy(1550, enemy_y)
                enemy.speed = max(1, int(enemy.speed * speed_multiplier))
                enemies.append(enemy)
            
            enemy_spawn_timer = 0

        # Спавн босса (отдельно от обычных врагов)
        if not boss_active:
            boss_spawn_timer += 1
            # Босс появляется реже на низких уровнях, чаще на высоких
            boss_spawn_threshold = max(600, 1800 - level * 100)
            if boss_spawn_timer >= boss_spawn_threshold:
                boss = Boss(1550, random.randint(50, 450))
                boss.speed = int(boss.speed * speed_multiplier)
                boss_active = True
                boss_spawn_timer = 0

        # Спавн бонусов (ДОБАВЛЕН МАГНИТ)
        powerup_timer += 1
        if powerup_timer >= 600:
            powerup_types = ["Ускоренная перезарядка", "Щит", "Доп. очки", "Магнит"]
            powerups.append(PowerUp(random.randint(50, 950), -60, random.choice(powerup_types)))
            powerup_timer = 0

        # Отрисовка иконки магазина
        shop_rect = p.Rect(1370, 5, 150, 100)
        screen.blit(shop_icon, (1400, 0))
        if mouse_clicked and shop_rect.collidepoint(mouse_pos):
            shop_open = True

        # Рисуем игрока
        if invulnerability_timer == 0 or invulnerability_timer % 10 < 5:
            screen.blit(current_skin, (x, y))

        # Обновляем файрболы
        for fb in fireballs[:]:
            fb.update()
            for enemy in enemies[:]:
                if fb.active and enemy.active:
                    if fb.get_rect().colliderect(enemy.get_rect()):
                        if enemy.hit():
                            score += enemy.value * combo_multiplier
                            enemy.drop_coin(coins)
                            combo += 1
                            combo_timer = 180
                            combo_multiplier = min(99, 1 + combo // 3)
                            
                            # Статистика для быстрых убийств
                            current_time = round(time.time())
                            if current_time - last_enemy_kill_time < 10:
                                game_stats["rapid_kills"] += 1
                            last_enemy_kill_time = current_time
                            
                        fb.active = False
                        break
            if boss_active and boss and fb.active:
                if fb.get_rect().colliderect(boss.get_rect()):
                    if boss.hit():
                        score += boss.value * combo_multiplier
                        boss.drop_coin(coins)
                        boss_active = False
                        level += 1
                        combo += 3
                        combo_timer = 180
                        combo_multiplier = min(5, 1 + combo // 5)
                    fb.active = False
            if fb.active:
                fb.draw()
            else:
                fireballs.remove(fb)

        # Обновляем врагов
        player_rect = p.Rect(x, y, 100, 180)
        for enemy in enemies[:]:
            enemy.update()
            if enemy.active and invulnerability_timer == 0:
                if enemy.get_rect().colliderect(player_rect):
                    lives -= 1
                    invulnerability_timer = 120
                    enemy.active = False
                    combo = 0
                    combo_multiplier = 1
                    game_stats["damage_taken"] += 1
                    last_damage_time = round(time.time())
                    if lives <= 0:
                        game_over = True
                        final_time = round(time.time())
                        # ПРОИГРЫШ ЗВУКА ПРОИГРЫША И ВЫКЛЮЧЕНИЕ МУЗЫКИ
                        if not game_over_sound_played:
                            game_over_sound.play()
                            game_over_sound_played = True
                            p.mixer.music.stop()  # ВЫКЛЮЧАЕМ ОСНОВНУЮ МУЗЫКУ
                # Проверка близких столкновений
                elif enemy.get_rect().inflate(20, 20).colliderect(player_rect):
                    game_stats["near_misses"] += 1
            if enemy.active:
                enemy.draw()
            else:
                enemies.remove(enemy)

        # Обновляем босса
        if boss_active and boss:
            boss.update()
            if boss.active:
                boss.draw()
                if invulnerability_timer == 0 and boss.get_rect().colliderect(player_rect):
                    lives -= 2
                    invulnerability_timer = 120
                    combo = 0
                    combo_multiplier = 1
                    game_stats["damage_taken"] += 2
                    last_damage_time = round(time.time())
                    if lives <= 0:
                        game_over = True
                        final_time = round(time.time())
                        # ПРОИГРЫШ ЗВУКА ПРОИГРЫША И ВЫКЛЮЧЕНИЕ МУЗЫКИ
                        if not game_over_sound_played:
                            game_over_sound.play()
                            game_over_sound_played = True
                            p.mixer.music.stop()  # ВЫКЛЮЧАЕМ ОСНОВНУЮ МУЗЫКУ
            else:
                boss_active = False

        # Обновляем бонусы
        for powerup in powerups[:]:
            powerup.update()
            if powerup.active and powerup.get_rect().colliderect(player_rect):
                active_powerups[powerup.type] = powerup.duration
                game_stats["powerups_collected"] += 1
                if powerup.type == "Ускоренная перезарядка":
                    fire_cooldown_max = max(5, fire_cooldown_max // 2)
                elif powerup.type == "Щит":
                    invulnerability_timer = max(invulnerability_timer, powerup.duration)
                elif powerup.type == "Магнит":
                    # АКТИВАЦИЯ МАГНИТА - ПРИТЯГИВАЕМ ВСЕ МОНЕТЫ (включая уже существующие)
                    for coin in coins:
                        coin.activate_magnet()
                powerup.active = False
            if powerup.active:
                powerup.draw()
            else:
                powerups.remove(powerup)

        # Обновляем активные бонусы
        for powerup_type in list(active_powerups.keys()):
            active_powerups[powerup_type] -= 1
            if active_powerups[powerup_type] <= 0:
                if powerup_type == "Ускоренная перезарядка":
                    # Восстанавливаем скорость стрельбы с учетом всех улучшений
                    # Базовый cooldown = 60, каждый уровень уменьшает на 12
                    fire_cooldown_max = 60 - (fire_rate_level * 12)
                    # Обеспечиваем минимальное значение
                    fire_cooldown_max = max(10, fire_cooldown_max)
                del active_powerups[powerup_type]

        # Обновляем комбо
        if combo_timer > 0:
            combo_timer -= 1
            if combo_timer == 0:
                combo = 0
                combo_multiplier = 1

        # Обновляем монеты (С АНИМАЦИЕЙ МАГНИТА И ПРОВЕРКОЙ СТОЛКНОВЕНИЯ)
        for coin in coins[:]:
            collected = coin.update()
            if collected:
                coins_collected += coin.value * coin_multiplier
                game_stats["coins_collected_total"] += coin.value * coin_multiplier
                score += coin.value * 2 * coin_multiplier
                coins.remove(coin)
            elif coin.active:
                # ПРОВЕРКА СТОЛКНОВЕНИЯ С ИГРОКОМ ДЛЯ ОБЫЧНЫХ МОНЕТ
                if not coin.magnet_attracted and coin.get_rect().colliderect(player_rect):
                    coins_collected += coin.value * coin_multiplier
                    game_stats["coins_collected_total"] += coin.value * coin_multiplier
                    score += coin.value * 2 * coin_multiplier
                    coin.active = False
                    coins.remove(coin)
                else:
                    coin.draw()
            else:
                coins.remove(coin)

        # Проверка достижения "Идеальный уровень"
        if round(time.time()) - last_damage_time >= 60 and game_stats["damage_taken"] == 0:
            game_stats["perfect_levels"] += 1
            last_damage_time = round(time.time())

        # Интерфейс
        if not can_fire:
            cooldown_text = font.render(f'Перезарядка: {fire_cooldown/60:.1f} сек', True, (255, 0, 0))
            screen.blit(cooldown_text, (10, 10))
        else:
            ready_text = font.render('Готов к стрельбе!', True, (0, 255, 0))
            screen.blit(ready_text, (10, 10))

        score_text = font.render(f'Счет: {score}', True, (255, 255, 255))
        screen.blit(score_text, (320, 10))

        coins_text = font.render(f'Монеты: {coins_collected}', True, (255, 215, 0))
        screen.blit(coins_text, (520, 10))

        # Отображение комбо
        if combo > 1:
            combo_text = font.render(f"COMBO x{combo_multiplier}! ({combo} убийств)", True, (255, 215, 0))
            screen.blit(combo_text, (650, 50))
        
         # Отображение текущего режима управления
        control_mode = "Мышь" if mouse_control else "Клавиатура"
        control_text = font.render(f'Управ.: {control_mode}', True, (200, 200, 100))
        screen.blit(control_text, (1080, 10))

        # Отображение уровня
        level_text = font.render(f'Уровень: {level}', True, (255, 255, 255))
        screen.blit(level_text, (320, 50))

        # Отображение статуса музыки
        music_status = "ВКЛ" if music_playing else "ВЫКЛ"
        music_text = font.render(f'Музыка: {music_status} (M)', True, (200, 200, 200))
        screen.blit(music_text, (770, 10))
        
        if lives >= 3:
            screen.blit(h3, (10, 20))
        elif lives == 2:
            screen.blit(h2, (10, 20))
        elif lives == 1:
            screen.blit(h1, (10, 20))

        if lives > 3:
            extra_text = font.render(f'+{lives - 3}', True, (0, 255, 0))
            screen.blit(extra_text, (140, 50))

        # Отображение активных бонусов
        bonus_y = 120
        for powerup_type, time_left in active_powerups.items():
            bonus_text = font.render(f"{powerup_type}: {time_left//60}", True, (255, 255, 0))
            screen.blit(bonus_text, (10, bonus_y))
            bonus_y += 30

        # Отображение уведомлений о достижениях (слева внизу столбиком вправо)
        active_achievements = [a for a in achievements if a.show_timer > 0]
        for i, achievement in enumerate(active_achievements):
            # Тексты достижения
            achievement_text = font.render(f"Достижение: {achievement.name}", True, (255, 215, 0))
            reward_text = font.render(f"Награда: +{achievement.reward} монет", True, (255, 255, 255))
            
            # Определяем размеры текста
            text_width1 = achievement_text.get_width()
            text_width2 = reward_text.get_width()
            max_text_width = max(text_width1, text_width2)
            
            # Создаем прямоугольник под текст (с отступами)
            rect_width = max_text_width + 30  # +30 пикселей отступы слева/справа
            rect_height = 80  # Высота прямоугольника
            rect_x = 10 + i * (rect_width + 10)  # Позиция X с отступом 10px между уведомлениями
            rect_y = 650  # Позиция Y внизу
            
            # Рисуем прямоугольник
            s = p.Surface((rect_width, rect_height), p.SRCALPHA)
            s.fill((0, 0, 0, 180))  # Полупрозрачный черный фон
            screen.blit(s, (rect_x, rect_y))
            
            # Рисуем рамку вокруг прямоугольника
            p.draw.rect(screen, (255, 215, 0), (rect_x, rect_y, rect_width, rect_height), 2)
            
            # Выводим текст (центрируем по ширине прямоугольника)
            text_x1 = rect_x + (rect_width - text_width1) // 2
            text_x2 = rect_x + (rect_width - text_width2) // 2
            
            screen.blit(achievement_text, (text_x1, rect_y + 10))
            screen.blit(reward_text, (text_x2, rect_y + 40))
            
            achievement.show_timer -= 1

    else:
        # Экран окончания игры
        if final_time == 0:
            final_time = round(time.time())
        elapsed_time = final_time - begin_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        if minutes == 0:
            main_time = f"{seconds} секунд"
        elif minutes == 1:
            if seconds == 0:
                main_time = "1 минута"
            else:
                main_time = f"1 минута и {seconds} секунд"
        else:
            if seconds == 0:
                main_time = f"{minutes} минут"
            else:
                main_time = f"{minutes} минут и {seconds} секунд"

        screen.blit(go, (0, 0))
        game_over_text = big_font.render(f'Счет: {score}', True, (255, 0, 0))
        coins_text = big_font.render(f'Монеты: {coins_collected}', True, (255, 215, 0))
        restart_text = big_font.render('Нажмите R для перезапуска', True, (255, 255, 255))
        time_text = big_font.render(f'Время игры: {main_time}', True, (255, 255, 255))
        level_text = big_font.render(f'Достигнутый уровень: {level}', True, (255, 255, 255))
        
        screen.blit(game_over_text, (900, 600))
        screen.blit(coins_text, (400, 600))
        screen.blit(restart_text, (400, 700))
        screen.blit(time_text, (450, 10))
        screen.blit(level_text, (450, 80))

    p.display.update()
    clock.tick(60)

p.quit()