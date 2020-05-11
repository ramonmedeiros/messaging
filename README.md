![CI](https://github.com/ramonmedeiros/messaging/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/ramonmedeiros/messaging/branch/master/graph/badge.svg)](https://codecov.io/gh/ramonmedeiros/messaging)

# Messaging - playing with Cloud Run and Bigtable

Made with Python, Flask, BigTable and CloudRun, the service is running on Google Cloud by this address https://messaging-viz3uyzyva-lz.a.run.app.

## Features

### Send message

It's possible to send a message. You just need a string with a valid email format and a message.

```
curl -H "Content-Type: application/json" -d '{"recipient": "email@email.com", "message": "a"}' -X POST https://messaging-viz3uyzyva-lz.a.run.app/message
```

### Retrieve messages

#### Not fetched before
You can retrieve all messages that were never retrieved, by:
```
curl -X GET https://messaging-viz3uyzyva-lz.a.run.app/message
{"2020-05-11T00:07:53.303464": {"message": {"recipient": "email@email.com", "message": "a"}, "read": false},....

```

#### By Index
Specify start and end index
```
curl -X GET https://messaging-viz3uyzyva-lz.a.run.app/message?start=0&end=0
{"2020-05-11T00:07:53.303464": {"message": {"recipient": "email@email.com", "message": "a"}, "read": false}
```
