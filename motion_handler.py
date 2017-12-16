
class MotionHandler:

    def __init__(self, image_manager, scale):
        self.setting_first = True
        self.image_manger = image_manager
        self.scale = scale

    def start(self):
        self.setting_first = True
        self.end_x = None
        self.end_y = None
        manager = self.image_manger
        manager.restore_original()
        manager.save_original()
        panel = manager.get_panel('image')
        panel.bind('<Motion>', lambda event: self.movement(event))
        panel.bind('<Button-1>', lambda event: self.click(event))

    def stop(self):
        panel = self.image_manger.get_panel('image')
        panel.unbind('<Motion>')
        panel.unbind('<Button-1>')

    def movement(self, event):
        self.last_x = event.y
        self.last_y = event.x
        if not self.setting_first:
            self._draw_rect()

    def click(self, event):
        self.movement(event)
        if self.setting_first:
            self.setting_first = False
            self.start_x = self.last_x
            self.start_y = self.last_y
        else:
            self.setting_first = True
            self.end_x = self.last_x
            self.end_y = self.last_y
            self.stop()

    def get_rect(self):
        real_max_width = self.image_manger.get_image('image').shape[1]
        multiplier = float(real_max_width) / self.scale
        start_x = int(min(self.start_x, self.end_x) * multiplier)
        start_y = int(min(self.start_y, self.end_y) * multiplier)
        end_x = int(max(self.start_x, self.end_x) * multiplier)
        end_y = int(max(self.start_y, self.end_y) * multiplier)
        return (start_x, start_y), (end_x, end_y)

    def _draw_rect(self):
        self.image_manger.restore_original()
        img = self.image_manger.get_image('resized')
        start_x = min(self.start_x, self.last_x)
        start_y = min(self.start_y, self.last_y)
        end_x = max(self.start_x, self.last_x)
        end_y = max(self.start_y, self.last_y)
        start_x = 0 if start_x < 0 else start_x
        start_y = 0 if start_y < 0 else start_y
        end_x = len(img)-1 if end_x >= len(img) else end_x
        end_y = len(img[0]) - 1 if end_y >= len(img[0]) else end_y
        for i in range(start_x, end_x):
            img[i, start_y] = [255, 0, 0]
            img[i, end_y] = [255, 0, 0]
        for i in range(start_y, end_y):
            img[start_x, i] = [255, 0, 0]
            img[end_x, i] = [255, 0, 0]
        self.image_manger.update_panel(img)
