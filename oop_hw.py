from math import gcd
from typing import Union


class Fraction:
    def __init__(self, numerator: int, denominator: int):
        if not isinstance(numerator, int):
            raise TypeError("Чисельник має бути цілим числом")
        
        if not isinstance(denominator, int):
            raise TypeError("Знаменник має бути цілим числом")
        
        if denominator == 0:
            raise ValueError("Знаменник не може бути нулем")
        
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        
        self._numerator = numerator
        self._denominator = denominator
    
    def simplify(self) -> 'Fraction':
        divisor = gcd(abs(self._numerator), abs(self._denominator))
        return Fraction(self._numerator // divisor, self._denominator // divisor)
    
    def __str__(self) -> str:
        if self._denominator == 1:
            return str(self._numerator)
        return f"{self._numerator}/{self._denominator}"
    
    def __repr__(self) -> str:
        return f"Fraction({self._numerator}, {self._denominator})"
    
    def to_float(self) -> float:
        return self._numerator / self._denominator
    
    def _validate_operand(self, other: Union['Fraction', int]) -> 'Fraction':
        if isinstance(other, Fraction):
            return other
        elif isinstance(other, int):
            return Fraction(other, 1)
        else:
            raise TypeError(f"Операція не підтримується для цього типу")
    
    def __add__(self, other: Union['Fraction', int]) -> 'Fraction':
        other = self._validate_operand(other)
        num = self._numerator * other._denominator + other._numerator * self._denominator
        den = self._denominator * other._denominator
        return Fraction(num, den).simplify()
    
    def __radd__(self, other: Union['Fraction', int]) -> 'Fraction':
        return self.__add__(other)
    
    def __sub__(self, other: Union['Fraction', int]) -> 'Fraction':
        other = self._validate_operand(other)
        num = self._numerator * other._denominator - other._numerator * self._denominator
        den = self._denominator * other._denominator
        return Fraction(num, den).simplify()
    
    def __rsub__(self, other: Union['Fraction', int]) -> 'Fraction':
        other = self._validate_operand(other)
        return other.__sub__(self)
    
    def __mul__(self, other: Union['Fraction', int]) -> 'Fraction':
        other = self._validate_operand(other)
        num = self._numerator * other._numerator
        den = self._denominator * other._denominator
        return Fraction(num, den).simplify()
    
    def __rmul__(self, other: Union['Fraction', int]) -> 'Fraction':
        return self.__mul__(other)
    
    def __truediv__(self, other: Union['Fraction', int]) -> 'Fraction':
        other = self._validate_operand(other)
        if other._numerator == 0:
            raise ValueError("Ділення на нуль неможливе")
        num = self._numerator * other._denominator
        den = self._denominator * other._numerator
        return Fraction(num, den).simplify()
    
    def __rtruediv__(self, other: Union['Fraction', int]) -> 'Fraction':
        other = self._validate_operand(other)
        return other.__truediv__(self)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (Fraction, int)):
            return False
        other = self._validate_operand(other)
        s = self.simplify()
        o = other.simplify()
        return s._numerator == o._numerator and s._denominator == o._denominator

if __name__ == "__main__":
    
    print("1. Створення дробів:")
    f1 = Fraction(4, 6)
    print(f"f1.simplify() = {f1.simplify()}")
    
    f2 = Fraction(3, 4)
    print(f"f2 = {f2}\n")
    
    print("2. Математичні операції:")
    print(f"{f1} + {f2} = {f1 + f2}")
    print(f"{f1} - {f2} = {f1 - f2}")
    print(f"{f1} * {f2} = {f1 * f2}")
    print(f"{f1} / {f2} = {f1 / f2}\n")
    
    print("3. Операції з цілими числами:")
    print(f"{f1} + 2 = {f1 + 2}")
    print(f"3 * {f2} = {3 * f2}\n")
    
    print("4. Перетворення у float:")
    print(f"{f1}.to_float() = {f1.to_float()}")
    print(f"{f2}.to_float() = {f2.to_float()}\n")

    print("5. Порівняння дробів:")
    print(f"{f1} == {Fraction(2, 3)}: {f1.simplify() == Fraction(2, 3)}")