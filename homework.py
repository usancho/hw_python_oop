from dataclasses import asdict, dataclass
from typing import Type


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
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_hour: float = duration
        self.weight_kg: float = weight

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

    CALORIE_SPEED_MULT: float = 18
    CALORIE_SPEED_DIFF: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки Running."""
        return ((self.CALORIE_SPEED_MULT * self.get_mean_speed()
                - self.CALORIE_SPEED_DIFF) * self.weight_kg
                / self.M_IN_KM * self.duration_hour * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIE_WEIGHT_MULT: float = 0.035
    CALORIE_SPEED_HEIGHT_MULT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки
        SportsWalking.
        """
        return ((self.CALORIE_WEIGHT_MULT * self.weight_kg
                + ((self.get_mean_speed())**2 // self.height_cm)
                * self.CALORIE_SPEED_HEIGHT_MULT * self.weight_kg)
                * self.duration_hour * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIE_SPEED_SUM: float = 1.1
    CALORIE_SPEED_WEIGHT_MULT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для тренировки Swimming."""
        return (self.length_pool_m * self.count_pool / self.M_IN_KM
                / self.duration_hour)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки Swimming."""
        return ((self.get_mean_speed() + self.CALORIE_SPEED_SUM)
                * self.CALORIE_SPEED_WEIGHT_MULT * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_activity: dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking}
    if workout_type not in type_of_activity:
        raise ValueError(f'''
Неизвестный тип тренировки: ['{workout_type}'].
Допустимые значения: {list(type_of_activity)}.
                          ''')
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
