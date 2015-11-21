from galois_tables import LOG_TABLE, EXP_TABLE


class Galois256(object):

    def __init__(self):
        pass

    @staticmethod
    def exp(a, n):
        """
        Computes a**n

        :param a: A member of the field
        :param n: A plain old integer
        :return: The result of multiplying a by itself n times
        """
        if n == 0: return 1
        elif a == 0: return 0
        else:
            log_result = (LOG_TABLE[a] * n) % 255
            return EXP_TABLE[log_result]
