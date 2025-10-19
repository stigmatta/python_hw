import math

data = (2.0, 4.0, 8.0, 16.0)

strategies = (
    ("Арифметичне", lambda d: sum(d) / len(d)),
    ("Геометричне", lambda d: math.prod(d) ** (1 / len(d))),
    ("Гармонійне", lambda d: len(d) / sum(1 / x for x in d))
)

def find_max_average(data_tuple:tuple, strategy_tuple:tuple):
    results = []
    for name, func in strategy_tuple:
        result = func(data_tuple)
        results.append((name, result))
        print(f"{name} середнє = {result:.2f}")
    max_name, max_value = max(results, key=lambda x: x[1])
    print(f"\nМаксимальне середнє ({max_name}) = {max_value:.2f}")
    return max_name, max_value

if __name__ == "__main__":
    find_max_average(data, strategies)
