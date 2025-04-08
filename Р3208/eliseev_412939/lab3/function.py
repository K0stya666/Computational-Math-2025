class Function:
    """
    Класс для хранения функции (лямбда-выражение) и её описания.
    """

    def __init__(self, function, description):
        self.function = function
        self.description = description

    def __call__(self, x):
        """
        Позволяет вызывать экземпляр класса как функцию:
        f_obj(x) эквивалентно f_obj.function(x)
        """
        return self.function(x)