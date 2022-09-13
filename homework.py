from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAIN_INFO = ('Тип тренировки: {training_type}; '
                  'Длительность: {duration:.3f} ч.; '
                  'Дистанция: {distance:.3f} км; '
                  'Ср. скорость: {speed:.3f} км/ч; '
                  'Потрачено ккал: {calories:.3f}.'
                  )

    def get_message(self) -> str:
        """Получить строку с информацией о тренировке."""
        return self.TRAIN_INFO.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_hour = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_hour,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_SPEED_MULT: float = 18
    COEFF_CALORIE_SPEED_DIFF: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки Running."""
        return ((self.COEFF_CALORIE_SPEED_MULT * self.get_mean_speed()
                - self.COEFF_CALORIE_SPEED_DIFF) * self.weight_kg
                / self.M_IN_KM * self.duration_hour * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_WEIGHT_MULT: float = 0.035
    COEFF_CALORIE_SPEEDHEIGHT_MULT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_sm = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки
        SportsWalking.
        """
        return ((self.COEFF_CALORIE_WEIGHT_MULT * self.weight_kg
                + ((self.get_mean_speed())**2 // self.height_sm)
                * self.COEFF_CALORIE_SPEEDHEIGHT_MULT * self.weight_kg)
                * self.duration_hour * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_SPEED_SUM: float = 1.1
    COEFF_CALORIE_SPEEDWEIGHT_MULT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для тренировки Swimming."""
        return (self.length_pool_m * self.count_pool / self.M_IN_KM
                / self.duration_hour)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки Swimming."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_SPEED_SUM)
                * self.COEFF_CALORIE_SPEEDWEIGHT_MULT * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_activity: type[Training] = {'SWM': Swimming,
                                        'RUN': Running,
                                        'WLK': SportsWalking}
    if workout_type not in type_of_activity:  # проверка соответствия данных
        raise ValueError(f'ValueError: '
                         f'Неизвестный тип тренировки... '
                         f'Допустимые значения: '
                         f'{list(type_of_activity)}'
                         )
    return type_of_activity[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
