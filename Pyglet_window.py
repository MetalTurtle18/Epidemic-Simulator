import time

import pyglet

import Functions


def centerImage(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


class Chart:
    def __init__(self, entity_map, infection_rate, recovery_rate, recovery_rate_increase, fatality_rate,
                 fatality_rate_decrease):

        self.entity_map = entity_map
        self.infection_rate = infection_rate
        self.recovery_rate = recovery_rate
        self.recovery_rate_increase = recovery_rate_increase
        self.fatality_rate = fatality_rate
        self.fatality_rate_decrease = fatality_rate_decrease

        self.cycleCount = 0

        self.window = pyglet.window.Window(width=810, height=810)

        pyglet.resource.path = ["assets"]
        pyglet.resource.reindex()

        self.background_image = pyglet.resource.image("window_background.png")
        self.simulation_background_image = pyglet.resource.image("simulation_background.png")
        self.entity_healthy_image = pyglet.resource.image("entity_healthy.png")
        self.entity_infected_image = pyglet.resource.image("entity_infected.png")
        self.entity_recovered_image = pyglet.resource.image("entity_recovered.png")
        self.entity_dead_image = pyglet.resource.image("entity_dead.png")
        self.top_text = pyglet.text.Label("Epidemic Simulation: Running", font_name="Lucida Grande", font_size=24,
                                          x=self.window.width // 2,
                                          y=775, anchor_x="center", anchor_y="center")

        self.window_background = pyglet.sprite.Sprite(self.background_image, x=0, y=0)
        self.window_background.scale = 0.75
        self.simulation_background = pyglet.sprite.Sprite(self.simulation_background_image, x=35, y=308)
        self.simulation_background.scale = 0.4

        centerImage(self.background_image)
        centerImage(self.simulation_background_image)

        self.entity_batch = pyglet.graphics.Batch()
        self.entity_sprites = []

        centerImage(self.entity_healthy_image)
        centerImage(self.entity_infected_image)
        centerImage(self.entity_recovered_image)
        centerImage(self.entity_dead_image)

    def on_draw(self):
        self.window.clear()
        self.window_background.draw()
        self.simulation_background.draw()
        self.top_text.draw()
        self.entity_batch.draw()

    # noinspection PyUnusedLocal
    def updateSprites(self, dt):
        self.cycleCount += 1
        if self.cycleCount == 1:
            array = self.entity_map
        else:
            array = Functions.tickWorld(self.entity_map, self.infection_rate, self.recovery_rate, self.fatality_rate)
        self.entity_sprites.clear()
        for row in range(len(array)):
            for column in range(len(array)):
                if array[row][column] == "H":
                    self.entity_sprites.append(
                        pyglet.sprite.Sprite(self.entity_healthy_image, (column + 1) * 40, (row + 1) * 40,
                                             batch=self.entity_batch))
                elif array[row][column] == "I":
                    self.entity_sprites.append(
                        pyglet.sprite.Sprite(self.entity_infected_image, (column + 1) * 40, (row + 1) * 40,
                                             batch=self.entity_batch))
                elif array[row][column] == "R":
                    self.entity_sprites.append(
                        pyglet.sprite.Sprite(self.entity_recovered_image, (column + 1) * 40, (row + 1) * 40,
                                             batch=self.entity_batch))
                elif array[row][column] == "D":
                    self.entity_sprites.append(
                        pyglet.sprite.Sprite(self.entity_dead_image, (column + 1) * 40, (row + 1) * 40,
                                             batch=self.entity_batch))

        self.window.clear()
        self.window_background.draw()
        self.simulation_background.draw()
        self.top_text.draw()
        self.entity_batch.draw()

        if self.recovery_rate < 100:
            self.recovery_rate += self.recovery_rate_increase
        if self.fatality_rate > 0:
            self.fatality_rate -= self.fatality_rate_decrease
        if (self.fatality_rate <= 0 and self.recovery_rate <= 0) or (not Functions.contains(array, "I")):
            self.window.clear()
            self.top_text = pyglet.text.Label("Epidemic Simulation: Finished", font_name="Lucida Grande", font_size=24,
                                              x=self.window.width // 2,
                                              y=775, anchor_x="center", anchor_y="center")
            self.window_background.draw()
            self.simulation_background.draw()
            self.top_text.draw()
            self.entity_batch.draw()
            time.sleep(5)
            self.window.close()

    def start(self):
        pyglet.clock.schedule_interval(self.updateSprites, 3)
        pyglet.app.run()
