from time import time


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def start(self):
        self.start_time = time()

    def stop(self):
        self.end_time = time()

    @property
    def minutes(self):
        return int(self.end_time - self.start_time) // 60

    @property
    def seconds(self):
        return int(self.end_time - self.start_time) % 60

    @property
    def time_passed(self):
        return f"{self.minutes}:{self.seconds:02d}"

    def __str__(self):
        return self.time_passed
