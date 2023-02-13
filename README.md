# streamiko

#### summary
A simple example of a netmiko command runner using htmx & websockets

- Simple container deployment
- Leverages websockets for near realtime comms to equipment
- Leverages netmiko ssh autodetect for dynamic driver discovery

#### installing
```
git clone https://github.com/tbotnz/streamiko.git
cd streamiko
sudo docker-compose up --build
```

you can then access streamiko via ```http://localhost:9005```

#### demo
![streamiko demo](/streamiko.gif)


#### important note
project is experimental, we assume you know what you are doing.

