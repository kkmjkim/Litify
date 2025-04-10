<template>
  <div class="chat-input">
    <div class="chat-input-child"></div>
    <div class="chat-input-container" id="chatThread"> 
      <BubbleList 
        :bubbles="bubbles"
        :facts="facts"
        :promptProgress="promptProgress"
        :complaint="complaint"
      />
    </div>
    <footer class="bottom-chat-bar">
      <div class="bottom-chat-bar-child"></div>
      <div class="rectangle-group">
        <div class="rectangle-div"></div>
        <input 
          :disabled="closed"
          contenteditable="true" 
          style="outline:none" 
          class="type-your-message"
          @keyup.enter="sendMessage"
          v-model="message"
          placeholder="Type your message here.."
        >
      </input>
      </div>
      <div class="send-button">
        <!-- <v-btn icon="mdi-send" size="small" variant="flat"></v-btn> -->
        <v-btn class="send-message" variant="flat" @click="sendMessage">Send message</v-btn>
        <!-- <div class="send-message">Send message</div> -->
      </div>
    </footer>
    
  </div>
</template>
<script>
  import { defineComponent, ref } from "vue";
  import BubbleList from "./BubbleList.vue";

  export default defineComponent({
    name: "ChatContainer",
    components: { BubbleList },
    props: [ "bubbles", "promptProgress", "facts", "complaint", "closed"],
    data() {
      return {
        message: "",
        placeholder: "Type your message here..",
        typing: false,
        session: undefined,
      };
    },
    methods: {
      sendMessage() {
        this.$emit("sendMessage", this.message)
        this.message = ""
      },
    },
    watch: {
      bubbles: {
        handler() {
          const main = this.$el.querySelector("#chatThread")
          setTimeout(() => {
            main.scrollTo({
              top: main.scrollHeight,
              behavior: 'smooth'
            })  
          }, 100);
          
        },
        deep: true
      }
    }
  });
</script>
<style scoped>
  .chat-input-child {
    align-self: stretch;
    height: 629px;
    position: relative;
    background-color: var(--color-gray-100);
    display: none;
  }
  .empty-status {
    position: relative;
    line-height: 16px;
    font-weight: 300;
  }
  .message-content-child {
    align-self: stretch;
    height: 1px;
    position: relative;
    border-top: 1px solid var(--color-whitesmoke-200);
    box-sizing: border-box;
    z-index: 1;
  }
  .message-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-68xl) 0px 0px;
    box-sizing: border-box;
    min-width: 196px;
  }
  .today {
    position: relative;
    font-weight: 500;
    display: inline-block;
    min-width: 33px;
    color: var(--black-45);
    z-index: 1;
  }
  .message-time {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-61xl) 0px 0px;
  }
  .thank-you-for {
    align-self: stretch;
    position: relative;
  }
  .message-status {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-end;
    text-align: left;
    font-size: var(--font-size-xs);
    color: var(--black-45);
    font-family: var(--font-sf-pro-display);
  }
  .msg-from-me {
    border-radius: var(--br-base) var(--br-base) 0px var(--br-base);
    background-color: var(--color-whitesmoke-100);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-xs) var(--padding-mid) var(--padding-7xs)
      var(--padding-lg);
    gap: var(--gap-9xs);
    z-index: 1;
  }
  .message-sent {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    padding: 0px 0px var(--padding-12xs);
    box-sizing: border-box;
    gap: var(--gap-13xl);
    min-width: 196px;
    text-align: right;
    font-size: var(--font-size-sm);
    color: var(--black-85);
    font-family: var(--font-sf-pro-text);
  }
  .message-content-parent {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    gap: var(--gap-5xl);
  }
  .message-replied-child {
    height: 24px;
    width: 24px;
    position: relative;
    object-fit: cover;
    z-index: 1;
  }
  .hello-have-you {
    position: relative;
  }
  .empty-receiver-message {
    position: relative;
    font-size: var(--font-size-xs);
    line-height: 16px;
    font-weight: 300;
    font-family: var(--font-sf-pro-display);
    color: var(--black-45);
  }
  .message {
    border-radius: 0px var(--br-base) var(--br-base) var(--br-base);
    background-color: var(--color-whitesmoke-100);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-xs) var(--padding-base) var(--padding-7xs)
      var(--padding-lg);
    box-sizing: border-box;
    gap: var(--gap-9xs);
    max-width: calc(100% - 50px);
    z-index: 1;
  }
  .message-replied {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px var(--padding-xl) 0px 0px;
    box-sizing: border-box;
    gap: var(--gap-4xs);
    max-width: 100%;
    font-size: var(--font-size-sm);
    color: var(--black-85);
    font-family: var(--font-sf-pro-text);
  }
  .message-input {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: var(--gap-xl);
    max-width: 100%;
  }
  .chat-input-container {
    overflow-y: auto;
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-end;
    padding: 20px var(--padding-lg) 20px var(--padding-2xl);
    box-sizing: border-box;
    max-width: 100%;
  }
  .bottom-chat-bar-child {
    height: 48px;
    width: 720px;
    position: relative;
    box-shadow: 0px -1px 0px #eee;
    background-color: var(--color-white);
    display: none;
    max-width: 100%;
  }
  .rectangle-div {
    height: 36px;
    width: 607px;
    position: relative;
    border-radius: var(--br-xs);
    background-color: var(--color-gray-100);
    display: none;
    max-width: 100%;
  }
  .type-your-message {
    width: 100%;
    position: relative;
    display: inline-block;
    flex-shrink: 0;
    z-index: 1;
    color: black;
  }
  .rectangle-group {
    flex: 1;
    border-radius: var(--br-xs);
    background-color: var(--color-gray-100);
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-4xs) var(--padding-smi) var(--padding-3xs);
    box-sizing: border-box;
    min-width: 166px;
    max-width: 100%;
    z-index: 1;
    margin-left: 5px;
    margin-top: 10px;
  }
  .send-message {
    position: relative;
    font-weight: 500;
    display: inline-block;
    min-width: 91px;
    z-index: 1;
    color: var(--green-2);
  }
  .send-button {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-3xs-5) 0px 0px;
    color: var(--green-2);
  }
  .bottom-chat-bar {
    align-self: stretch;
    box-shadow: 0px -1px 0px #eee;
    background-color: var(--color-white);
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-10xs) var(--padding-10xs) var(--padding-4xs);
    box-sizing: border-box;
    gap: var(--gap-2xs);
    max-width: 100%;
    z-index: 2;
    text-align: left;
    font-size: var(--font-size-sm);
    color: var(--black-45);
    font-family: var(--font-sf-pro-display);
  }
  .chat-input {
    flex-grow: 1;
    overflow-y: auto;
    align-self: stretch;
    background-color: var(--color-gray-100);
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-end;
    /* padding: var(--padding-298xl) 0px 0px; */
    box-sizing: border-box;
    max-width: 100%;
    text-align: left;
    font-size: var(--font-size-xs);
    color: var(--black-1);
    font-family: var(--font-sf-pro-display);
  }
  .placeholder {
    color: var(--black-45);
  }

  @media screen and (max-width: 975px) {
    /* .chat-input {
      gap: var(--gap-28xl);
    } */
  }
  @media screen and (max-width: 725px) {
    .message-content-parent {
      flex-wrap: wrap;
    }

    .bottom-chat-bar {
      flex-wrap: wrap;
    }

    /* .chat-input {
      padding-top: var(--padding-187xl);
      box-sizing: border-box;
    } */
  }
  @media screen and (max-width: 450px) {
    .message-sent {
      gap: var(--gap-base);
    }

    /* .chat-input {
      gap: var(--gap-5xl);
    } */
  }
  
</style>
