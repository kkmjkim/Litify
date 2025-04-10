<template>
  <div class="desktop">
    <section class="body">
      <img class="empty-icon" alt="" />
      <div class="body-inner"><LeftSideBar @newChat="clearChatHandler" /></div>
      <div class="messages-container-wrapper">
        <MessagesContainer 
          :chatList="chatList"
          :activeChat="activeChat"
          @clickChatRoom="changeActiveChat"
        />
      </div>
      <div class="body-child"></div>
      <div class="chatroom-container" >
        <TopStatusBar />
        <ChatContainer
          :bubbles="activeChat.bubbles"
          :facts="activeChat.facts"
          :complaint="activeChat.complaint"
          :promptProgress="promptProgress"
          :closed="!!activeChat.complaint"
          @sendMessage="sendRequest"
        />
      </div>
    </section>
  </div>
</template>
<script>
  import { defineComponent } from "vue";
  import LeftSideBar from "../components/LeftSideBar.vue";
  import MessagesContainer from "../components/MessagesContainer.vue";
  import TopStatusBar from "../components/TopStatusBar.vue";
  import ChatContainer from "../components/ChatContainer.vue";
  import axios from 'axios';

  import { marked } from 'marked'
  import { markedHighlight } from "marked-highlight";


  export default defineComponent({
    name: "Desktop",
    components: { LeftSideBar, MessagesContainer, TopStatusBar, ChatContainer },
    setup() {
      marked.use(markedHighlight({
        langPrefix: 'hljs language-',
        highlight(code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
        }
      }));
    },
    data() {
      return {
        activeChat: {},
        chatInfo: {},
        newChat: false,
        promptProgress: false,
        welcomeText: "안녕하세요 AI를 기반으로 고소장 작성을 도와드리는 Litify입니다.<br/> 범죄 발생 일자나 사건 당시 상황에 대해 자세히 말씀해주실 수 있나요?",
        chatList: [{
            title: "가정폭력 사건",
            timestamp: "24/08/01",
            image: "/profiles/profile-7.jpg",
            "bubbles":[
                {
                    "type": "bot",
                    "text": "안녕하세요 AI를 기반으로 고소장 작성을 도와드리는 Litify입니다.<br/>범죄 발생 일자나 사건 당시 상황에 대해 자세히 말씀해주실 수 있나요?",
                    "timestamp": "10:53"
                }, {
                    "type": "user",
                    "text": "A가 사업 목적으로 나에게 1억원을 빌렸는데 약속한 변제기일에 변제하지 않았어. 난 변제일 이후로 여러 차례 A에게 변제를 독촉했지만 A는 무작정 기다려 달라고만 하고 현재는 A가 아예 잠적한 상황이야.",
                    "timestamp": "10:53"
                }, {
                    "type": "bot",
                    "text": "와, 그런 일이 있었군요. 친구에게 그런 일을 당하셨다니 정말 충격적이셨겠어요. 차용금 거래에 대한 구체적인 내용, 예를 들어 차용증서나 계약서 같은 게 있으신가요?",
                    "timestamp": "10:53"
                }, {
                    "type": "user",
                    "text": "A에게 돈을 빌려줄 때 변제금과 변제일이 적혀있는 차용증을 작성했어.",
                    "timestamp": "10:53"
                }, {
                    "type": "bot",
                    "text": "그렇게 차용증을 작성하셨다니 다행이네요. 혹시 A가 돈을 빌릴 당시의 상황과 목적에 대한 추가적인 증거, 예를 들어 사업 계획서나 거래 내역 등이 있으신가요?",
                    "timestamp": "10:54"
                }, {
                    "type": "user",
                    "text": "A의 사업을 해외로 확장한다는 목적으로 돈을 빌려갔어.",
                    "timestamp": "10:54"
                }, {
                    "type": "bot",
                    "text": "와, 그런 일이 있었군요. A의 사업을 해외로 확장한다는 목적으로 돈을 빌려갔다는 것을 알게 되셨다니 정말 충격적이셨겠어요. 혹시 A가 돈을 빌릴 당시의 상황과 목적에 대한 추가적인 증거, 예를 들어 사업 계획서나 거래 내역 등이 있으신가요?",
                    "timestamp": "10:54"
                }, {
                    "type": "user",
                    "text": "구체적인 사업 계획서에 대해서는 받은 것이 없어. 그냥 A의 말을 믿고 빌려줬어.",
                    "timestamp": "10:54"
                }
            ],
            "complaint": {
                "purpose": "고소인은 피고소인 A를 사기죄로 고소합니다. 피고소인 A는 고소인을 속여 1억원을 편취하였으므로, 법에 따라 엄중히 처벌해주시기 바랍니다.",
                "reason": "피고소인 A는 고소인에게 사업 목적으로 1억원을 빌리면서, 해외로 사업을 확장한다는 목적으로 돈을 사용하겠다고 말했습니다. 그러나 구체적인 사업 계획서에 대해서는 받은 것이 없으며, A의 말을 믿고 돈을 빌려주었습니다. 그러나 약속한 변제기일에 A는 돈을 갚지 않았고, 그 이후로도 여러 차례 변제를 독촉했지만 A는 무작정 기다려 달라고만 했습니다. 현재 A는 연락이 두절되어 행방을 알 수 없는 상황입니다. 고소인은 A에게 돈을 빌려줄 때, 변제금과 변제일이 적혀있는 차용증을 작성했습니다. 이 차용증은 A가 돈을 빌린 사실과 상환 조건을 증명하는 중요한 증거입니다. 또한, 고소인은 A에게 여러 차례 변제를 독촉한 사실을 입증할 수 있는 증거를 가지고 있습니다. 피고소인 A는 고소인을 속여 1억원을 편취하였습니다. 이는 형법 제347조 제1항의 사기죄에 해당하는 범죄행위입니다. 따라서 피고소인 A를 철저히 조사하여 법에 따라 엄중히 처벌해주시기를 바랍니다."
            },
            "facts": [
                {
                    "facts": `2020고단1256\n피고인은 2020. 1. 3.경 피해자 B에게 전화로 "모피사업에 자금이 필요한데, 돈을 빌려주면 3~4일 내로 갚겠다.\"라고 거짓말을 하였다.\n그러나 사실 피고인은 약 3억 원 이상의 채무가 존재하였고, 피해자에게 차용한 금원을 모피구매가 아닌 기존 채무 변제에 사용할 계획이었으며, 소유하고 있는 재산이나 일정한 수입이 없었으므로 피해자로부터 금원을 차용하더라도 이를 변제할 의사나 능력이 없었다.\n이로써 피고인은 위와 같이 피해자를 기망하여 이에 속은 피해자로부터 같은 날 차용금 명목으로 피고인 명의 C계좌(계좌번호 1 생략)로 500만 원, 2020. 1. 7.경 같은 명목으로 500만 원을 송금받았다.\n2020고단2181\n피고인은 2018. 7. 17.경 순천시 D백화점에서 피해자 B에게 "내가 급하게 돈이 필요하니 300만 원만 빌려주면 월 3부 이자를 주고, 돈이 필요하면 바로 변제하겠다.\"라고 거짓말을 하였다.\n그러나 사실 피고인은 별다른 재산이 없고, B에게 약 3억 8,400만 원, E에게 약 6억 8,100만 원 등 차용금 채무가 있는 채무 초과상태였고, 피해자로부터 돈을 빌려 기존 채무를 변제하려고 하였으므로 피해자로부터 돈을 빌리더라도 월 3부 이자를 주거나 차용금을 바로 변제할 수 있는 의사나 능력이 없었다.\n피고인은 위와 같이 피해자를 기망하여 이에 속은 피해자로부터 2018. 7. 17.경 피고인 명의의 C은행 계좌(계좌번호 2 생략)로 300만 원을 송금 받은 것을 비롯하여 그때부터 2020. 2. 4.까지 별지 범죄일람표 1 기재와 같이 15회에 걸쳐 합계 5,350만 원을 송금 받아 차용금을 편취하였다.\n2021고단169\n1. 피해자 F에 대한 사기\n피고인은 2018. 7. 17.경 순천 일원에서 피해자에게 \"내가 전당포로 돈놀이를 하고 있는데, 용돈벌이하게 해줄테니 돈을 빌려달라.\"고 거짓말을 하였다.\n그러나 사실 피고인은 전당포를 운영한 사실이 없었고, 금융권 대출금이나 사인에게 차용한 돈을 변제하지 못해 돈을 빌려 기존에 빌린 돈을 갚는 소위 ‘돌려막기"를 하고 있었으므로 피해자에게 돈을 차용하더라도 이를 변제할 의사나 능력이 없었다.\n피고인은 위와 같이 피해자를 기망하여 이에 속은 피해자로부터 피고인 명의의 C계좌(계좌번호 2 생략)로 300만 원을 교부받는 등, 2018. 1. 2.경부터 2020. 2. 7.경까지 별지 범죄일람표 2 기재와 같이 총 223회에 걸쳐 위와 같은 방법으로 합계 862,465,000원을 교부 받았다.\n2. 피해자 G에 대한 사기\n피고인은 2018. 4. 17. 순천 일원에서 피해자에게 \"내가 운영하는 모피 매장에서 본사로 돈을 보내야 하는데 돈이 부족하다. 400만 원을 빌려주면 곧 갚아주겠다.\"고 거짓말을 하였다.\n그러나 사실 피고인은 금원을 빌리더라도 이를 본사에 보낼 생각이 없었고, 금융권대출금이나 사인에게 차용한 돈을 변제하지 못해 돈을 빌려 기존에 빌린 돈을 갚는 소위 ‘돌려막기"를 하고 있었으므로 피해자에게 돈을 차용하더라도 이를 변제할 의사나 능력이 없었다.\n피고인은 위와 같이 피해자를 기망하여 이에 속은 피해자로부터 피고인 명의의 C계좌(계좌번호 2 생략)로 400만 원을 교부받는 등, 2018. 4. 17.경부터 2020. 1. 17.경까지 별지 범죄일람표 3 기재와 같이 총 64회에 걸쳐 위와 같은 방법으로 합계 417,500,000원을 교부받았다.\n3. 피해자 H에 대한 사기\n피고인은 2019. 1. 2.경 순천 일원에서 피해자에게 \"도박하는 사람들에게 급전을 대주고 이자를 받을 일이 있으니, 돈을 빌려달라.\"고 거짓말을 하였다.\n그러나 사실 피고인은 금원을 빌리더라도 이를 도박하는 사람들에게 빌려줄 생각이 없었고, 금융권 대출금이나 사인에게 차용한 돈을 변제하지 못해 돈을 빌려 기존에 빌린 돈을 갚는 소위 ‘돌려막기"를 하고 있었으므로 피해자에게 돈을 차용하더라도 이를 변제할 의사나 능력이 없었다.\n피고인은 위와 같이 피해자를 기망하여 이에 속은 피해자로부터 피고인 명의의 C계좌(계좌번호 2 생략)로 225,000원을 교부받는 등, 2019. 1. 2.경부터 2020. 1. 2.경까지 별지 범죄일람표 4 기재와 같이 총 19회에 걸쳐 위와 같은 방법으로 합계 158,725,000원을 교부받았다.`,
                    "ruling": "피고인을 징역 2년에 처한다."
                }, {
                    "facts": "피고인은 2016. 9. 25.경 서울 광진구 B에 있는 피고인이 운영하는 'C' 음식점에서, 피해자 D에게 \"가게를 확장하는데 돈이 필요하다, 1,000만 원을 빌려주면 매월 30만 원의 이자를 주고 원금은 1년 뒤에 갚겠다.\"라고 거짓말하였다.\n그러나 사실 피고인은 당시 금융권 채무 및 사채가 3,000만 원 상당이었고, 이를 막기 위해 고율의 일수 또는 사채를 쓰면서 돌려막기를 하고 있었으며, 피해자로부터 돈을 빌리더라도 위와 같이 돌려막기 식으로 기존 채무를 상환하거나 카드 대금 등 생활비 명목으로 사용할 생각이었기 때문에 차용금을 변제할 의사나 능력이 없었다. 그럼에도 불구하고 피고인은 이에 속은 피해자로부터 그 무렵 가게 확장을 위한 차용금 명목으로 현금 1,000만 원을 교부받는 등, 그 때부터 2019. 4. 15.경까지 사이에 별지 범죄일람표 기재와 같이 피해자 6명으로부터 총 19회에 걸쳐 합계 129,300,000원을 교부받았다.\n이로써 피고인은 피해자들을 기망하여 재물을 교부받았다.",
                    "ruling": "피고인을 징역 1년 2월에 처한다."
                }, {
                    "facts": "피고인은 2017. 3. 초순경 피해자 B에게 휴대전화 메신저로 연락하여 \"내가 유흥주점 아가씨들에게 숙소를 제공하여 월세를 받고 있는데, 숙소를 구할 수 있는 돈을 빌려 주면 월 5%의 이자를 지급해 주겠다. 원금은 2017. 5. 17.까지 변제해 주겠다.\"라고 거짓말 말하였다.\n그러나 사실은 피고인은 피해자로부터 금원을 차용하기 전 유흥주점 종사자들에게 숙소를 제공하는 사업을 하기 위해 여러 지인 등으로부터 금원을 빌린 상태여서 다른 사람들로부터 금원을 차용하여 이를 갚는 소위 ‘돌려막기'식의 변제를 하고 있어서 피해자로부터 빌린 돈도 위와 같이 돌려막기로 다른 차용금 채무를 변제하려고 하였을 뿐, 피해자로부터 차용한 금원으로 숙소를 구하고 피해자에게 말한 변제기에 원금과 이자를 변제할 의사나 능력이 없었다.\n그럼에도 불구하고 피고인은 이에 속은 피해자로부터 2017. 3. 17.경 피고인 명의의 농협계좌로 1,600만 원을 송금받은 것을 비롯하여 그때부터 같은 해 5. 8.경까지 별지 범죄일람표 기재와 같이 총 3회에 걸쳐 합계 6,600만 원을 송금받았다.\n이로써 피고인은 피해자를 기망하여 재물을 교부받았다.",
                    "ruling": "피고인을 징역 6월에 처한다.\n다만, 이 판결 확정일부터 2년간 위 형의 집행을 유예한다."
                }
            ]
          },
          {
            title: "매매계약 대금 횡령 사건",
            timestamp: "24/04/18",
            image: "/profiles/profile-4.jpg",
            bubbles: [],
          },
          {
            title: "온라인 게임 모욕 사건",
            timestamp: "23/11/21",
            image: "/profiles/profile-2.jpg",
            bubbles: [],
          },
          {
            title: "중고거래 사기 사건",
            timestamp: "23/10/20",
            image: "/profiles/profile-3.jpg",
            bubbles: [],
          },
        ],
      }
    },
    methods: {
      changeActiveChat(idx) {
        this.activeChat = this.chatList[idx]
        console.log("active chat:", this.activeChat, idx)
      },
      getDateString(){
        const date = new Date();
        const yy = date.getFullYear().toString().slice(2);
        const mm = String(date.getMonth()).padStart(2, '0');
        const dd = String(date.getDate()).padStart(2, '0');
        return `${yy}/${mm}/${dd}`
      },

      getTimeString(){
        const date = new Date();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${hours}:${minutes}`
      },

      newChatInProgress() {
        return this.newChat
      },

      clearChatHandler() {
        this.promptProgress = false
        this.activeChat.bubbles = []
        this.activeChat.facts = []
        this.activeChat.complaint = undefined

        setTimeout(() => {
          this.activeChat.bubbles.push({
            text: this.welcomeText,
            type: 'bot',
            timestamp: this.getTimeString()
          })
        }, 500)
      },

      newChatHandler() {
        if (this.newChatInProgress()) {
          console.log('New Chat is in progress. ignore the event.');
          return;
        }
        this.newChat = true;
        
        this.chatList.unshift({
          title:  "새로운 대화",
          active: true,
          image: "/profiles/profile-5.jpg",
          timestamp: this.getDateString(),
          bubbles: [],
          facts: [],
          complaint: undefined,
        })

        this.activeChat = this.chatList[0]
        setTimeout(() => {
          this.activeChat.bubbles.push({
            text: marked(this.welcomeText),
            type: 'bot',
            timestamp: this.getTimeString()
          })
        }, 800)
      },

      async sendRequest(prompt) {
        if (prompt == '') {
          console.log('prompt is empty. ignore..')
          return
        }

        this.promptProgress = true
        this.activeChat.bubbles.push({
          type: 'user',
          text: prompt,
          timestamp: this.getTimeString()
        })
        

        let body = {
            ...this.session
        }
        body.utterance = prompt
        console.log(body)

        try {
          const response = await axios.post('http://localhost:8000/prompt', body,{
              headers: {
                'Content-Type': 'application/json',
              }
          });

          this.session = response.data
          console.log("response:",response.data)

          if(response.data.facts) {
            this.activeChat.facts = response.data.facts
          }

          if(response.data.complaint) {
            this.activeChat.complaint = response.data.complaint
          } else {
            if (response.data.message == "") {
              console.log("message is empty. try send message agin.")
              return
            }
            
            let bubble = {
              text: response.data.message,
              timestamp: this.getTimeString(),
              type: 'bot',
            }
            this.activeChat.bubbles.push(bubble)
          }
          
        } catch (error) {
          console.error('There was a problem with the fetch operation:', error);
        } finally {
          this.promptProgress = false
        }
      }
    },
    mounted() {
      this.newChatHandler(); 
    }
  });
</script>
<style scoped>
  .empty-icon {
    width: 1112px;
    position: relative;
    max-height: 100%;
    display: none;
    max-width: 100%;
  }
  .body-inner {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px 15px 0px 0px;
  }
  .messages-container-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 27px 20px 0px 0px;
  }
  .body-child {
    height: 100vh;
    width: 1px;
    position: relative;
    border-right: 1px solid var(--color-whitesmoke-200);
    box-sizing: border-box;
    z-index: 1;
  }
  .chatroom-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    min-width: 469px;
    max-width: 100%;
    height: 100vh;
  }
  .body {
    flex: 1;
    border-radius: 0px 0px var(--br-2xs) var(--br-2xs);
    background-color: var(--color-white);
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: center;
    max-width: 100%;
    row-gap: 20px;
  }
  .desktop {
    width: 100%;
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    line-height: normal;
    letter-spacing: normal;
  }

  @media screen and (max-width: 975px) {
    .body-inner {
      display: none;
    }

    .body-child {
      display: none;
      width: 100%;
      height: 1px;
    }

    .body {
      flex-wrap: wrap;
      padding-left: var(--padding-xl);
      padding-right: var(--padding-xl);
      box-sizing: border-box;
    }
  }
  @media screen and (max-width: 725px) {
    .chatroom-container {
      min-width: 100%;
    }
  }
</style>
