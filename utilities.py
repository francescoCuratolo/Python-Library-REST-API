
class Utilities:

    @classmethod
    def safe_int(self, stringa):
        try:
            intero = int(stringa)
            return intero
        except:
            return -1
