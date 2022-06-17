

class Utils(object):
    def normalize(x, min, max):
        return (x - min) / (max - min) * 100;
        