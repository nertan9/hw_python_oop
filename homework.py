from typing import Dict, List, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:0.3f} ч.; "
                f"Дистанция: {self.distance:0.3f} км; "
                f"Ср. скорость: {self.speed:0.3f} км/ч; "
                f"Потрачено ккал: {self.calories:0.3f}.")


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MINS_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALLORIE_COUNT_COEFFICIENT_1 = 18
    CALLORIE_COUNT_COEFFICIENT_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.CALLORIE_COUNT_COEFFICIENT_1
                * self.get_mean_speed()
                - self.CALLORIE_COUNT_COEFFICIENT_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MINS_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALLORIE_COUNT_COEFFICIENT_1 = 0.035
    CALLORIE_COUNT_COEFFICIENT_2 = 2
    CALLORIE_COUNT_COEFFICIENT_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALLORIE_COUNT_COEFFICIENT_1
                * self.weight
                + (self.get_mean_speed()
                    ** self.CALLORIE_COUNT_COEFFICIENT_2
                    // self.height)
                * self.CALLORIE_COUNT_COEFFICIENT_3
                * self.weight)
                * self.duration
                * self.MINS_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALLORIE_COUNT_COEFFICIENT_1 = 1.1
    CALLORIE_COUNT_COEFFICIENT_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.CALLORIE_COUNT_COEFFICIENT_1)
                * self.CALLORIE_COUNT_COEFFICIENT_2
                * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    sport_codenames: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in sport_codenames:
        return sport_codenames[workout_type](*data)
    raise ValueError(f"Тренировка с именем {workout_type} не найдена.")


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
