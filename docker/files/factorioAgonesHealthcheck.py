import factorio_rcon, os, socket, time, requests


class factorioAgonesHealthcheck:
    def __init__(self) -> None:
        self.ready = False
        self.healthcheckServer()

    def healthcheckServer(self):
        try:
            self.__createRconConnection__()
            while True:
                self.checkVersion()
                time.sleep(30)
        except Exception as errorMessage:
            print(f"Exception encountered: {errorMessage}")
            print("Retrying in 5 seconds")
            time.sleep(5)
            self.healthcheckServer()

    def __createRconConnection__(self):
        factorioRconPassword = self.__fetchRconPassword__().strip()

        factorioHostname = socket.gethostname()
        factorioRconIPAddress = socket.gethostbyname(factorioHostname)
        factorioRconPort = int(os.getenv("RCON_PORT"))
        self.factorioRconClient = factorio_rcon.RCONClient(
            factorioRconIPAddress, factorioRconPort, factorioRconPassword
        )

    def checkVersion(self):
        envFactorioVersion = os.getenv("VERSION")
        rconFactorioVersion = self.factorioRconClient.send_command("/version")

        if rconFactorioVersion == rconFactorioVersion:
            if self.ready == False:
                self.__notifyAgonesReady__()
            self.__notifyAgonesHealthy__()

    def __fetchRconPassword__(self):
        factorioConfigPath = os.getenv("CONFIG")
        return open(f"{factorioConfigPath}/rconpw", "r").read()

    def __notifyAgonesReady__(self):
        agonesSdkHttpPort = os.getenv("AGONES_SDK_HTTP_PORT")
        url = f"http://localhost:{agonesSdkHttpPort}/ready"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data={}, headers=headers)
        if response.text == "{}":
            self.ready = True
            print("Server now ready, Agones has been notified.")

    def __notifyAgonesHealthy__(self):
        agonesSdkHttpPort = os.getenv("AGONES_SDK_HTTP_PORT")
        url = f"http://localhost:{agonesSdkHttpPort}/health"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data={}, headers=headers)
        if response.text == "":
            print("Server is healthy, Agones notified")


if __name__ == "__main__":
    factorioAgonesMonitorInitialise = factorioAgonesHealthcheck()
