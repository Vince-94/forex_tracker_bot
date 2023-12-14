from datetime import datetime
from dateutil import tz

import requests
from bs4 import BeautifulSoup


class ForexTracker():
    def __init__(self, forex: str, thresholds: list, target_margin: float, safe_margin: float):
        """_summary_

        Args:
            forex (str): _description_
            thresholds (list): _description_
            target_margin (float): _description_
            safe_margin (float): _description_

        Raises:
            TypeError: _description_
        """
        if not isinstance(forex, str):
            raise TypeError("forex must be a str")

        self._forex = forex
        self._url = f"https://www.google.com/finance/quote/{forex}"

        # Thresholds properties
        self._thresholds = thresholds
        self._state = 0
        self._old_state = 0
        self._notification = False

        # Exchange properties
        self._sell = False
        self._buy = False
        self._start_point = None
        self._target_point = None
        self._target_margin = target_margin
        self._target_margin_increase = 0.1
        self._safe_margin = safe_margin

        self._datetime_match = "%b %d, %I:%M:%S %p %Z · Disclaimer"
        self._datetime_format = "%H:%M:%S %d/%m"

        self._forex_info()

    def _forex_info(self):
        response = requests.get(self._url)

        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract page title
        self._title = soup.title.text

        # Extract forex name
        name = soup.find('div', {'role': 'heading', 'aria-level': '1', 'class': 'zzDege'})
        if name.text is None:
            raise AttributeError("Forex name does not exist!")
        self._currencies_name = name.text

    def _update_forex_data(self):
        response = requests.get(self._url)

        if response.status_code != 200:
            print("Failed to retrieve the page. Status code:", response.status_code)
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract forex rate
        rate = soup.find('div', class_='YMlKec fxKbKc')
        if rate.text is None:
            raise AttributeError("Forex rate is None")
        self._currencies_rate = float(rate.text)

        # Extract forex time
        time_info = soup.find('div', class_='ygUjEc', jsname='Vebqub')
        if time_info.text is None:
            raise AttributeError("Forex rate is None")
        datetime_utc = datetime.strptime(time_info.text, self._datetime_match).replace(tzinfo=tz.tzutc())
        datetime_zt = datetime_utc.astimezone(tz.tzlocal())
        self._datetime_utc_f = datetime_utc.strftime(self._datetime_format)
        self._datetime_zt_f = datetime_zt.strftime(self._datetime_format)

    def _check_thresholds(self):
        if self._currencies_rate < self._thresholds[0]:
            self._state = -1
            self._notification = f"Lower threshold passed: {self._thresholds[0]}"
        elif self._currencies_rate > self._thresholds[1]:
            self._state = 1
            self._notification = f"Upper threshold passed: {self._thresholds[1]}"
        else:
            self._state = 0
            self._notification = f"Whitin threshold: [{self._thresholds[0]}, {self._thresholds[1]}]"

        if self._old_state != self._state:
            self._old_state = self._state
            return self._notification

        return

    def _check_setpoint_margin(self):
        if self._start_point is None:
            return

        margin = self._currencies_rate - self._start_point
        message = None

        if self._sell is True:
            self._target_point = self._start_point - self._target_margin
            if -margin > self._target_margin:
                message = f"Buy point (MXN->EUR). Current margin: {-margin}"
                self._target_margin += self._target_margin_increase
            elif -margin < self._safe_margin:
                message = f"Warning, out of safety: {margin}"

        if self._buy is True:
            self._target_point = self._start_point + self._target_margin
            if margin > self._target_margin:
                message = f"Sell point (EUR->MXN). Current margin: {margin}"
                self._target_margin += self._target_margin_increase
            elif margin < self._safe_margin:
                message = f"Warning, out of safety: {margin}"

        return message

    def track(self):
        self._update_forex_data()
        threshold_msg = self._check_thresholds()
        setpoint_info = self._check_setpoint_margin()

        if threshold_msg or setpoint_info is not None:
            message = f"[{self._datetime_zt_f}] Automatic notification"
            if threshold_msg is not None:
                message += f"\n{threshold_msg}"
            if setpoint_info is not None:
                message += f"\n{setpoint_info}"
            return message

    def show_info(self) -> str:
        info = f"Forex status {self._currencies_name} ({self._datetime_zt_f})" \
               f"\n- exchange: {self._currencies_rate}"
        if self._thresholds is not None:
            info += f"\n- thresholds: {self._thresholds[0]} ~ {self._thresholds[1]}"
        else:
            info += f"\n- thresholds: None"

        if self._start_point is not None:
            if self._sell is True:
                info += f"\n- action: sell EUR->MXN"
            if self._buy is True:
                info += f"\n- action: buy EUR<-MXN"
            info += f"\n- start point: {self._start_point}"
            info += f"\n- target point: {self._target_point}"
        else:
            info += "\n- action: None"

        print(info)
        return info

    def reset(self) -> bool:
        self._buy = False
        self._sell = False
        self._start_point = None
        self._target_point = None

    # Getters
    @property
    def title(self):
        return self._title

    @property
    def name(self):
        return self._currencies_name

    @property
    def value(self):
        return self._currencies_rate

    @property
    def timestamp(self):
        return f"{self._datetime_zt_f}"

    @property
    def thresholds(self):
        return self._thresholds

    @property
    def notification(self):
        return self._notification

    @property
    def start_point(self):
        return self._start_point

    @property
    def target_point(self):
        return self._target_point

    @property
    def sell(self):
        return self._sell

    @property
    def buy(self):
        return self._buy

    @property
    def target_margin(self):
        return self._target_margin

    # Setters
    @thresholds.setter
    def thresholds(self, thresholds: list):
        self._thresholds = thresholds

    @target_margin.setter
    def target_margin(self, target_margin: float):
        self._target_margin = target_margin
        if self._sell is True:
            self._target_point = self._start_point - self._target_margin
        if self._buy is True:
            self._target_point = self._start_point + self._target_margin

    @sell.setter
    def sell(self, sell_point: float):
        self._start_point = sell_point
        self._sell = True
        self._buy = False

    @buy.setter
    def buy(self, buy_point: float):
        self._start_point = buy_point
        self._buy = True
        self._sell = False
