import ctypes
import random

import PySimpleGUI as sg  # for GUI
import matplotlib.animation as animation  # for animations
import matplotlib.pyplot as plt  # for plotting
import numpy as np  # for matrix calculations
import pygame.midi  # for sounds

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def construct_pattern(pattern, m, clicked_buttons, window):  # used for constructing predefined/saved patterns
    if pattern.shape[0] <= m.shape[0] and pattern.shape[1] <= m.shape[1]:
        m[0:pattern.shape[0], 0:pattern.shape[1]] = pattern
        for i in range(pattern.shape[0]):
            for j in range(pattern.shape[1]):
                if pattern.item((i, j)) == 1:
                    but = 'btn' + str(i) + 'x' + str(j)
                    if but not in clicked_buttons:
                        clicked_buttons.append(but)
                        window.find_element(str(but)).Update(button_color=('black', 'yellow'))


def init_terrain():  # used to initialize the terrain
    global survives_array, born_array
    glider = np.matrix([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
    beacon = np.matrix([[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]])
    toad = np.matrix([[0, 0, 0, 0], [0, 1, 1, 1], [1, 1, 1, 0], [0, 0, 0, 0]])
    blinker = np.matrix([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    glider_gun = np.matrix([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    sunflower = np.matrix([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    welcome_layout = [[sg.Text('Dimensions(x): '), sg.InputText(key='xDim')],
                      [sg.Text('Dimensions(y): '), sg.InputText(key='yDim')],
                      [sg.Text('Number alive: '), sg.InputText(key='aliveNr')],
                      [sg.Button('Create own game'), sg.Button('Randomize'), sg.Button('Change rules'),
                       sg.Checkbox('With sound', default=True, key='With sound'),
                       sg.Checkbox('With alive cell number chart', default=True, key='With chart'),
                       sg.Text('Interval: '),
                       sg.Slider(range=(50, 2000), default_value=500, size=(20, 15), orientation='horizontal',
                                 key='interval')],
                      [sg.T('')], [sg.Text('Load pattern: '), sg.Input(key='fileNameToLoad'),
                                   sg.FileBrowse(key='Browse', file_types=(("NumPy array file", "*.npy"),))],
                      [sg.T('')], [sg.Text('Load rules: '), sg.Input(key='rulesToLoad'),
                                   sg.FileBrowse(key='Browse rules',
                                                 file_types=(("NumPy archived array files", "*.npz"),))]]
    welcome_window = sg.Window('Game Of Life', welcome_layout).Finalize()
    while True:
        event, values = welcome_window.read()
        global soundOn
        soundOn = values['With sound']
        global with_chart
        with_chart = values['With chart']
        global interval
        interval = int(values['interval'])
        if not values['xDim']:
            if not values['yDim']:
                dim = (20, 20)
            else:
                dim = int(values['yDim']), int(values['yDim'])
        else:
            if not values['yDim']:
                dim = int(values['xDim']), int(values['xDim'])
            else:
                dim = int(values['xDim']), int(values['yDim'])
        m = np.zeros(dim)
        if values['aliveNr']:
            nr_alive = int(values['aliveNr'])
        else:
            nr_alive = int(dim[0] * dim[1] / 2)
        if event == sg.WIN_CLOSED:
            return m
        if values['rulesToLoad']:
            data = np.load(values['rulesToLoad'])
            born_array = data['arr_0'].tolist()
            survives_array = data['arr_1'].tolist()
        if event == 'Create own game':
            welcome_window.close()
            upper_buttons = [sg.Button('Start simulation'), sg.Button('Clear simulation'), sg.Button('Glider'),
                             sg.Button('Beacon'), sg.Button('Toad'), sg.Button('Blinker'), sg.Button('Glider Gun'),
                             sg.Button('Sunflower')]
            save_elements = [sg.Text('File name: '), sg.InputText(key='fileName'),
                             sg.Button('Save')]
            column = []
            loaded_matrix = []
            if values['fileNameToLoad']:
                loaded_matrix = np.load(values['fileNameToLoad'])
                m = np.array(loaded_matrix)
                dim = m.shape
            for i in range(dim[0]):
                buttons_horizontal = []
                for j in range(dim[1]):
                    buttons_horizontal.append(
                        sg.Button(button_color='purple', key='btn' + str(i) + 'x' + str(j), size=(2, 1)))
                column.append(buttons_horizontal)
            layout = [upper_buttons, save_elements, [sg.Column(column, scrollable=True, size=screensize)]]
            window = sg.Window('Game Of Life creator', layout).Finalize()
            window.maximize()
            clicked_buttons = []
            if values['fileNameToLoad']:
                construct_pattern(loaded_matrix, m, clicked_buttons, window)
            while True:
                event, values = window.read()
                window.refresh()
                if event == sg.WIN_CLOSED or event == 'Start simulation':
                    window.close()
                    return m
                if event == 'Clear simulation':
                    for button in clicked_buttons:
                        window.find_element(str(button)).Update(button_color='purple')
                        x = button[3:button.find('x')]
                        y = button[button.find('x') + 1:]
                        x = int(x)
                        y = int(y)
                        m[x, y] = 0
                    clicked_buttons = []
                if event == 'Save':
                    np.save(values['fileName'], m)
                    sg.popup('Successfully saved file ' + values['fileName'] + '.npy', title='Saved')
                if event == 'Glider':
                    construct_pattern(glider, m, clicked_buttons, window)
                if event == 'Beacon':
                    construct_pattern(beacon, m, clicked_buttons, window)
                if event == 'Toad':
                    construct_pattern(toad, m, clicked_buttons, window)
                if event == 'Blinker':
                    construct_pattern(blinker, m, clicked_buttons, window)
                if event == 'Glider Gun':
                    construct_pattern(glider_gun, m, clicked_buttons, window)
                if event == 'Sunflower':
                    construct_pattern(sunflower, m, clicked_buttons, window)
                if event[:3] == 'btn':
                    if event not in clicked_buttons:
                        clicked_buttons.append(event)
                        window.find_element(str(event)).Update(button_color=('black', 'yellow'))
                        x = event[3:event.find('x')]
                        y = event[event.find('x') + 1:]
                        x = int(x)
                        y = int(y)
                        m[x, y] = 1
                    else:
                        clicked_buttons.remove(event)
                        window.find_element(str(event)).Update(button_color='purple')
                        x = event[3:event.find('x')]
                        y = event[event.find('x') + 1:]
                        x = int(x)
                        y = int(y)
                        m[x, y] = 0
        if event == 'Randomize':
            welcome_window.close()
            for _ in range(nr_alive):
                x = random.randint(0, m.shape[0] - 1)
                y = random.randint(0, m.shape[1] - 1)
                while m[x, y] == 1:
                    x = random.randint(0, m.shape[0] - 1)
                    y = random.randint(0, m.shape[1] - 1)
                m[x, y] = 1
            return m
        if event == 'Change rules':
            nr_list = list(range(0, 9))
            welcome_window.hide()
            change_rules_layout = [[sg.Text('Save rules: '), sg.InputText(key='fileName'),
                                    sg.Button('Save')],
                                   [sg.Button('Check all'),
                                    sg.Button('Uncheck all')],
                                   [sg.Text('Survives')]]
            survives_row = []
            for i in nr_list:
                if i in survives_array:
                    survives_row.append(sg.Checkbox(str(i), default=True, key='surv' + str(i)))
                else:
                    survives_row.append(sg.Checkbox(str(i), default=False, key='surv' + str(i)))
            change_rules_layout.append(survives_row)
            change_rules_layout.append([sg.Text('Born')])
            born_row = []
            for i in nr_list:
                if i in born_array:
                    born_row.append(sg.Checkbox(str(i), default=True, key='born' + str(i)))
                else:
                    born_row.append(sg.Checkbox(str(i), default=False, key='born' + str(i)))
            change_rules_layout.append(born_row)
            change_rules_layout.append([sg.Button('Confirm')])
            change_rules_window = sg.Window('Rules of Game of Life', change_rules_layout).Finalize()
            while True:
                event_rules, values_rules = change_rules_window.read()
                if event_rules == sg.WIN_CLOSED or event_rules == 'Confirm':
                    for value in values_rules:
                        if value[:4] == 'surv' and values_rules[value] and int(value[4]) not in survives_array:
                            survives_array.append(int(value[4]))
                        elif value[:4] == 'surv' and not values_rules[value] and int(value[4]) in survives_array:
                            survives_array.remove(int(value[4]))
                    for value in values_rules:
                        if value[:4] == 'born' and values_rules[value] and int(value[4]) not in born_array:
                            born_array.append(int(value[4]))
                        elif value[:4] == 'born' and not values_rules[value] and int(value[4]) in born_array:
                            born_array.remove(int(value[4]))
                    change_rules_window.hide()
                    welcome_window.un_hide()
                    break
                if event_rules == 'Save':
                    for value in values_rules:
                        if value[:4] == 'surv' and values_rules[value] and int(value[4]) not in survives_array:
                            survives_array.append(int(value[4]))
                        elif value[:4] == 'surv' and not values_rules[value] and int(value[4]) in survives_array:
                            survives_array.remove(int(value[4]))
                    for value in values_rules:
                        if value[:4] == 'born' and values_rules[value] and int(value[4]) not in born_array:
                            born_array.append(int(value[4]))
                        elif value[:4] == 'born' and not values_rules[value] and int(value[4]) in born_array:
                            born_array.remove(int(value[4]))
                    np.savez(values_rules['fileName'], born_array, survives_array)
                    sg.popup('Successfully saved file ' + values_rules['fileName'] + '.npz', title='Saved')
                    change_rules_window.refresh()
                if event_rules == 'Check all':
                    for value in values_rules:
                        if value[:4] == 'surv' or value[:4] == 'born':
                            change_rules_window[value].update(True)
                            values_rules[value] = True
                            survives_array = nr_list
                            born_array = nr_list
                if event_rules == 'Uncheck all':
                    for value in values_rules:
                        if value[:4] == 'surv' or value[:4] == 'born':
                            change_rules_window[value].update(False)
                            values_rules[value] = False
                            survives_array = []
                            born_array = []


def get_neigh_nr(x, y, m):  # get the number of neighbors for a specific position in the m matrix
    nr = 0
    if x - 1 >= 0 and y - 1 >= 0:  # NW
        if m[x - 1, y - 1] == 1:
            nr += 1
    if x - 1 >= 0:  # N
        if m[x - 1, y] == 1:
            nr += 1
    if x - 1 >= 0 and y + 1 < m.shape[1]:  # NE
        if m[x - 1, y + 1] == 1:
            nr += 1
    if y - 1 >= 0:  # W
        if m[x, y - 1] == 1:
            nr += 1
    if y + 1 < m.shape[1]:  # E
        if m[x, y + 1] == 1:
            nr += 1
    if x + 1 < m.shape[0] and y - 1 >= 0:  # SW
        if m[x + 1, y - 1] == 1:
            nr += 1
    if x + 1 < m.shape[0]:  # S
        if m[x + 1, y] == 1:
            nr += 1
    if x + 1 < m.shape[0] and y + 1 < m.shape[1]:  # SE
        if m[x + 1, y + 1] == 1:
            nr += 1
    return nr


def transition(m, x, y, nr_neigh):  # check if the cell at (x,y) position will survive, based on the number of neighbors
    global born_array, survives_array
    if m[x, y] == 0:
        if nr_neigh in born_array:
            m[x, y] = 1
    else:
        if nr_neigh not in survives_array:
            m[x, y] = 0


def update_fig(self):  # used for updating the matplotlib figures
    if not pause:
        nr_alive = 0
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if mat[i, j] == 1:
                    nr_alive += 1
        global generation_count
        generation_count += 1
        text = f'Alive cells: {nr_alive} / {mat.size}      Generation number:{generation_count}\n'
        if with_chart:
            nr_alive_array.append(nr_alive)
            generations_array.append(generation_count)
            if len(nr_alive_array) == 5:
                nr_alive_array.pop(0)
            if len(generations_array) == 5:
                generations_array.pop(0)
            ax2.plot(generations_array, nr_alive_array)
        title.set_text(text)
        neigh = np.zeros((mat.shape[0], mat.shape[1]))
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                nr_neigh = get_neigh_nr(i, j, mat)
                neigh[i][j] = nr_neigh
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                transition(mat, i, j, neigh[i][j])
                im.set_array(mat)
        if soundOn and nr_alive != 0:
            midi()
        return im,


def midi():  # used for sound
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] == 1:
                freqToPlay = int((j + 1) * (128 / mat.shape[1]))
                if freqToPlay == 128:
                    freqToPlay = 127
                instrumentToPlay = int((i + 1) * (128 / mat.shape[0]))
                if instrumentToPlay < 0:
                    instrumentToPlay = 0
                if instrumentToPlay > 127:
                    instrumentToPlay = 127
                midi_out.set_instrument(instrumentToPlay)
                midi_out.note_on(freqToPlay, 127)


def onClick(self):  # pause on click
    global pause
    pause ^= True


survives_array = [2, 3]
born_array = [3]
pause = False
pygame.midi.init()
port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)
soundOn = False
with_chart = False
interval = 500
mat = init_terrain()
if with_chart:
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.canvas.mpl_connect('button_press_event', onClick)
    ax1 = axes[0]
    ax1.set_ylabel('instrument')
    ax1.set_xlabel('frequency')
    ax2 = axes[1]
    ax2.set_ylabel('alive cells')
    ax2.set_xlabel('generation')
    im = ax1.imshow(mat, animated=True)
else:
    fig = plt.figure()
    im = plt.imshow(mat, animated=True)
fig.tight_layout()
title = fig.text(0, 0, '')

nr_alive_array = []
generations_array = []
generation_count = 0
ani = animation.FuncAnimation(fig, update_fig, interval=interval, blit=False)
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()
