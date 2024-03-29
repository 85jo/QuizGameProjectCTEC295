class Bird():
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound
        

    def to_json(self):
        return {
            'name': self.name,
            'sound': self.sound,
        }

birds = [Bird('duck', 'quack'), Bird('Sparrow', 'chirp'), Bird('Robin', 'Squeak')]

