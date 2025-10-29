import requests
from datetime import datetime

class NbuRate:
    def __init__(self, j:dict):
        self.r030 = j["r030"]
        self.name = j["txt"]
        self.rate = j["rate"]
        self.abbr = j["cc"]
    
    def __str__(self) -> str:
        return f"{self.name} ({self.abbr}): {self.rate}"
    

class RatesData:
    def __init__(self):
        self.exchange_date = None
        self.rates = []

    def get_sorted_rates(self) -> list:
        return sorted(self.rates, key=lambda rate: rate.abbr)
    
    def display_all_rates(self):
        if not self.rates:
            print("Немає даних про курси валют.")
            return
        
        print(f"Курси валют НБУ на {self.exchange_date}")
        for rate in self.get_sorted_rates():
            print(rate)
        

    


class NbuRatesData(RatesData):
    BASE_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

    def __init__(self, date: str = None):
        super().__init__()
        self._load_rates(date)

    def _load_rates(self, date: str = None):
        url = self.BASE_URL
        params = {'json': ''}
        
        if date:
            params['date'] = date
        
        try:
            request = requests.get(url, params=params)
            request.raise_for_status()
            response = request.json()
            
            if not response:
                raise ValueError("НБУ не повернув дані для вказаної дати")
            
            self.exchange_date = response[0]["exchangedate"]
            self.rates = [NbuRate(r) for r in response]
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Помилка підключення до API НБУ: {e}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"Помилка обробки даних від НБУ: {e}")
        
    def validate_date(date_str: str) -> tuple[bool, str, str]:
        input_formats = ['%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y']
        
        parsed_date = None
        for fmt in input_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        
        if parsed_date is None:
            return False, "", "Неправильний формат дати. Використовуйте: DD.MM.YYYY"
        
        current_date = datetime.now()
        if parsed_date >= current_date:
            return False, "", "Дата має бути з минулого (не сьогодні і не в майбутньому)"
        
        min_date = datetime(1996, 1, 1)
        if parsed_date < min_date:
            return False, "", "Дата не може бути раніше 01.01.1996"
        
        formatted_date = parsed_date.strftime('%Y%m%d')
        
        return True, formatted_date, ""



def main():

    date_input = input("\nВведіть дату у форматі DD.MM.YYYY (або Enter для поточної): ").strip()
    is_valid, formatted_date, error_msg = NbuRatesData.validate_date(date_input)
    if not is_valid:
        raise ValueError(error_msg)
    rates_data = NbuRatesData(formatted_date)

    name = input("Введіть назву валюти або її частину (наприклад, долар, євро): ")

    results = [rate for rate in rates_data.rates
               if name in rate.name]
    
    if results:
        print(f"Знайдено {len(results)} валют(у):")
        for rate in results:
            print(rate)
    else:
        print(f"Валюта з назвою '{name}' не знайдена.")

    
    # abbr = input("Введіть скорочену назву валюти (наприклад, USD, EUR): ").upper()

    # results = [rate for rate in rates_data.rates
    #            if abbr in rate.abbr]
    # if results:
    #     print(f"Знайдено {len(results)} валют(у):")
    #     for rate in results:
    #         print(rate)
    # else:
    #     print(f"Валюта з '{abbr}' не знайдена.")

    # print(next((rate for rate in rates_data.rates if rate.abbr == abbr), f"Валюта '{abbr}' не знайдена."))
    # for rate in rates_data.rates:
    #     if rate.abbr == abbr:
    #         print(rate)
    #         break
    # else:
    #     print(f"Валюта '{abbr}' не знайдена.")


if __name__ == "__main__":
    main()