from unittest import TestCase
import pandas as pd

from .test_trading_calendar import ExchangeCalendarTestBase
from zipline.utils.calendars.exchange_calendar_cme import CMEExchangeCalendar


class CMECalendarTestCase(ExchangeCalendarTestBase, TestCase):
    answer_key_filename = "cme"
    calendar_class = CMEExchangeCalendar
    GAPS_BETWEEN_SESSIONS = False
    MAX_SESSION_HOURS = 24

    def test_2016_holidays(self):
        # good friday: 2016-03-25
        # christmas (observed)_: 2016-12-26
        # new years (observed): 2016-01-02
        for date in ["2016-03-25", "2016-12-26", "2016-01-02"]:
            self.assertFalse(
                self.calendar.is_session(pd.Timestamp(date, tz='UTC'))
            )

    #    March 2016
    # Su Mo Tu We Th Fr Sa
    #        1  2  3  4  5
    #  6  7  8  9 10 11 12
    # 13 14 15 16 17 18 19
    # 20 21 22 23 24 25 26
    # 27 28 29 30 31

    def test_days_of_week(self):
        a_week = [
            "2016-03-06", # Sun
            "2016-03-07", # Mon
            "2016-03-09", # Tue
            "2016-03-10", # Wed
            "2016-03-11", # Thu
            "2016-03-12", # Fri
        ]
        for date in a_week:
            self.assertTrue(
                self.calendar.is_session(pd.Timestamp(date, tz='UTC'))
            )

    def test_2016_early_closes(self):
        # mlk day: 2016-01-18
        # presidents: 2016-02-15
        # mem day: 2016-05-30
        # july 4: 2016-07-04
        # labor day: 2016-09-05
        # thankgiving: 2016-11-24
        for date in ["2016-01-18", "2016-02-15", "2016-05-30", "2016-07-04",
                     "2016-09-05", "2016-11-24"]:
            dt = pd.Timestamp(date, tz='UTC')
            self.assertTrue(dt in self.calendar.early_closes)

            market_close = self.calendar.schedule.loc[dt].market_close
            self.assertEqual(
                12,
                market_close.tz_localize('UTC').tz_convert(
                    self.calendar.tz
                ).hour
            )
