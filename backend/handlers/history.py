#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from datetime import datetime

from main import BasicHandler


class History(BasicHandler):
    def get(self, *args, **kwargs):
        # self.write({"resp": 1})
        # return
        try:
            city = int(self.get_argument('cityID', default='4720'))
            date_ts = self.get_argument("date", default=int(datetime.now().timestamp()).__str__())
            date = datetime.fromtimestamp(int(date_ts.split('.')[0]))
            raw_years = self.get_argument('years', default='')
            years = raw_years.split(',')

            if not years[0]:
                years = []
            else:
                years = list(map(int, years))

        except ValueError as ve:
            self.set_status(400)
            return
        else:
            self._get_weather(city, date, years)
        finally:
            return

    def _get_weather(self, city: int, date: datetime, years: list):
        weather_history = self.db_handler.get_history(city, date, years)
        self.write({"res": weather_history})
        return
