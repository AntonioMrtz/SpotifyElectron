# FAQ

## ◾ Unresponsive app while using the installed client

If the app is unresponsive or cant process operations such as create user, login etc it may me possible that the server is not fully launch yet. Wait 30-45 seconds for the first request and then all the request will be done inmediatly.

Our backend is hosted on an external third party server. The server goes to sleep when a fixed amout of time happens without any request. Sending a request to a slept server will trigger a cold start that can take up to 1 minute. This process is only being made when the server is going to sleep, apart from that the usage should be fast.

See [architecture structure](../Architecture.md) for more info.
