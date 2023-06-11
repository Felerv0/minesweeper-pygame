from useful import load_images_from_folder
from mouse_input import MouseInput

getInput = MouseInput()

game_map_size = (game_map_width, game_map_height) = (16, 16)
game_mine_count = 40
game_params = (game_map_size, game_mine_count)

display_scale = 2


screen_size = (screen_width, screen_height) = display_scale * (20 + game_map_width * 16), display_scale * (52 + game_map_height * 16 + 10)
CORNER_SIZE = (10 * display_scale, 10 * display_scale)
CELL_SIZE = (16 * display_scale, 16 * display_scale)
NUMBER_SIZE = (13 * display_scale, 23 * display_scale)
BORDER_VERTICAL_SIZE = (10 * display_scale, 16 * display_scale)
BORDER_HORIZONTAL_SIZE = (16 * display_scale, 10 * display_scale)
BUTTON_SIZE = (26 * display_scale, 26 * display_scale)

FPS = 30

sprites = load_images_from_folder('assets/sprites', display_scale)