# trello-helper

Helper for time managament with trello.
1. Add routine tasks for every day; 
2. assign date to columns representing days of the week;
3. get tasks with the date from `INBOX` list and put them in the corresponding date.

The scheme:
![scheme](https://github.com/MashaSamoylova/trello-helper/blob/master/scheme.png)


## Setting
1. Get from https://trello.com/app-key/ `token` and `key` and put them to `config.py`.
2. Set `board_url` in `config.py`. Describe your routine tasks in `config.py`.
3. Change path to script in `trello-helper.service`.


## Build and run
```
sudo pip install -r requirements.txt
sudo cp trello-helper.service /etc/systemd/system/
sudo cp trello-helper.timer /etc/systemd/system/
systemctl daemon-reload
systemctl start trello-helper.timer
```
Timer list
```
systemctl list-timers --all
```
