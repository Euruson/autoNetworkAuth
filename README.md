# autoNetworkAuth

`autoNetworkAuth` is used for automated network authentication in China university, under the environment of which clients have to login to connect to the Internet via web browser.

Now, `autoNetworkAuth` implements the following functions in UESTC:
1. Use `selenium` to automatically login to the school network.
2. Use `ping` to monitor the network status, and call `1` to get reconnected if got offline by the network server.
3. Create a linux's `systemd` service to work automatically.

One should add its own account information in the `config.json` file.

To register the `systemd` service, the following should be cared:
1. This project should be placed at `/usr/local` and owned by `root`.
2. Make a softlink for `autoNetworkAuth.service` by `sudo ln -s  ./autoNetworkAuth.service /etc/systemd/system/autoNetworkAuth.service`.
3. Run `sudo systemctl daemon-reload`.
4. To start this service manually, use `sudo systemctl start autoNetworkAuth`.
5. To start this service automatically at every time the server boots, use `sudo systemctl enable autoNetworkAuth`.
