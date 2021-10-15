# GitPRNotificationToSlack
## 0. Installation Steps
1. clone
```sh
$ git clone https://github.com/tkkawa/notification-to-slack.git
```

2. environment setup

The names of the docker image and container are specified by constants described in docker/env.sh.
These constants can be edited to suit your project.
```sh
$ cd notification-to-slack
$ cp docker/.env.sh docker/env.sh
$ sh docker/build.sh
$ sh docker/run.sh
$ sh docker/exec.sh
```
## 1. Register Pull Request
You can register Pull Request using cronjob

## 2. Register username

## 3. Notify Pull Request title to Slack
