# TOC Project 2017

Template Code for TOC Project 2017

A telegram bot based on a finite state machine

## Run my python3 code

 1. Open server ./ngrok http 5000<br/>
 2. python3 app.py

## my telegram-bot
* ID = @PiggyDD_bot

#### introdction
以小說為主題，與其他使用者互動的bot<br/>
主要功能:<br/>
1. 下載小說<br/>
2. 與其他使用者共同編輯一本小說<br/>
3. 查詢相關網站

#### How to use


### Run Locally
You can either setup https server or using `ngrok` as a proxy.

**`ngrok` would be used in the following instruction**

```sh
ngrok http 5000
```

After that, `ngrok` would generate a https URL.

You should set `WEBHOOK_URL` (in app.py) to `your-https-URL/hook`.


## Finite State Machine
![fsm](./img/show-fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"

