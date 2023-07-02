import pico.MicroPython.network.httpget as nw
import env
import ntptime
import ujson
import time
import utime


def GetWeather(nw):
    url = "https://api.openweathermap.org/data/2.5/onecall"

    params = [
        "lat=35.4478",
        "lon=139.6425",
        f"appid={env.WetherAppID}",
        "units=metric",
        "lang=ja",
    ]
    paramstr = "&".join(params)
    url = url + "?" + paramstr

    print("access:" + url)
    rst = nw.Access(url)

    if not rst[0]:
        return False

    ret = ujson.loads(rst[1].text)
    return ret["current"]["weather"]


def GetBitcoin(nw):
    url = "https://api.bitflyer.jp/v1/ticker?product_code=BTC_JPY"
    rst = nw.Access(url)

    if not rst[0]:
        return False

    ret = ujson.loads(rst[1].text)
    return ret["best_ask"]


# JST(日本標準時)はUTC+9時間
JP_UTC_OFFSET = 9


class TimeObj:
    def __init__(self, offset, retry):
        self.offset = offset
        self.retry = retry
        self.success = False

    def Fix(self):
        for i in range(self.retry):
            try:
                ntptime.settime()
                self.success = True
                break
            except OSError as exc:
                if exc.args[0] == 110:  # ETIMEDOUT
                    print("ETIMEDOUT. Returning False")
                    time.sleep(5)

    def GetTime(self):
        if not self.success:
            self.Fix()
        return utime.localtime(utime.mktime(utime.localtime()) + self.offset * 3600)


if __name__ == "__main__":
    n = nw.Network(env.Ssid, env.Password)
    ip = n.Connect()
    print(f"connect{ip}")

    # time
    tm = TimeObj(JP_UTC_OFFSET, 2)
    print(tm.GetTime())
    # coin
    coin = GetBitcoin(nw)
    if not coin:
        print("coin error")
    else:
        print("coin:" + coin)

    # weather
    weather = GetWeather(nw)
    if not weather:
        print("weather error")
    else:
        print("weather:" + weather)
