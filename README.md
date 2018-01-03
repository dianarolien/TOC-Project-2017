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
 進入聊天室, 隨便輸入一行字: Bot 會回覆使用方法(主選單)<br/>
 * 選取 novel , 再選取 biqukan, 輸入想要下載的小說網址貼上去之後開始進行下載. Bot 會把下載好的小說打包成.zip檔傳送給使用者<br/>
 * 選取 write , 可以選擇 writing or reading<br/>
 * 選取 web , 可以查詢小說相關網站
 * 選取 home , 回到主選單 (任何一個state都可以使用)<br/>
 * 選取 back , 回到上一個state (任何一個state都可以使用)<br/>
 * writing: 輸入的文字將會編輯成小說, 串接在原本的文章後<br/>
 * reading: 可以查看已有的故事內容<br/>
   
## Finite State Machine
![fsm](./machine_state.png)

### Extra
* 傳送 .gif 檔及.zip 檔
* 使用網路爬蟲閱覽文字並儲存成.txt檔
* 使用zipfile打包文字檔案
* 使用firebase-admin 讓使用者共編文字
