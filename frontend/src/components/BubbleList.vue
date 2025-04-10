<template>
  <div class="message-input">
    <div v-for="b in bubbles" class="message-sent">
      <div class="message-sent-child" v-if="b.type=='user'">
        <div class="msg-from-me">
          <div v-html="b.text" class="thank-you-for"></div>
          <div class="message-status">
            <div class="empty-status">{{ b.timestamp }}</div>
          </div>
        </div>
      </div>
      <div class="message-replied" v-else>
        <img class="message-replied-img" alt="" src="/litify_bot_icon.png" />
        <div class="message">
          <div v-html="b.text" class="hello-have-you"></div>
          <div class="empty-receiver-message">{{ b.timestamp }}</div>
        </div>
      </div>
    </div>
    <!-- progress bubble -->
    <div class="message-sent" v-show="promptProgress">
      <div class="message-replied">
        <img class="message-replied-img" alt="" src="/litify_bot_icon.png" />
        <div class="message" style="padding-bottom: 10px;">
          <div :data-text="searchText" class="search-text"> {{ searchText }}</div>
          <div class="empty-receiver-message"></div>
        </div>
      </div>
    </div>
    <v-container v-if="complaint">
      <v-row no-gutters>
        <v-col ></v-col>
        <v-col class="col closed-chat"> 대화를 기반으로 작성한 고소장 초안입니다. </v-col>
        <v-col class="col"></v-col>
      </v-row>
      <Complaint
        :facts="facts"
        :complaint="complaint"
      />
  </v-container>
  </div>
</template>
<script>
  import { defineComponent } from "vue";
  import Complaint from "./Complaint.vue";

  export default defineComponent({
    name: "BubbleList",
    components: { Complaint },
    props: [ "bubbles", "promptProgress", "closed", "facts", "complaint" ],
    data() {
      return {
        searchText: '질문을 바탕으로 답변을 생성중입니다.',
      }
    }
  });
  
</script>
<style scoped>
  .closed-chat {
    display: flex;
    align-items: center;
    text-align: center;
    color: #999;
  }
  .closed-chat::before,
  .closed-chat::after {
    width: 200px;
    content: "";
    flex: 1;
    border-bottom: 1px solid #aaa;
    margin: 0 16px;
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
    line-height: 20px;
    text-align: left;
    /* word-break: break-all; */
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
    max-width: calc(100% - 100px);
  }
  .message-sent-child {
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
  .message-sent {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    gap: var(--gap-5xl);
  }
  .message-replied-img {
    height: 24px;
    width: 24px;
    position: relative;
    object-fit: cover;
    z-index: 1;
  }
  .hello-have-you {
    line-height: 20px;
    position: relative;
    align-self: stretch;
    /* word-break: break-all; */
  }
  .empty-status {
    position: relative;
    line-height: 16px;
    font-weight: 300;
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
    max-width: calc(100%);
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
  @media screen and (max-width: 725px) {
    .message-sent {
      flex-wrap: wrap;
    }
  }
  @media screen and (max-width: 450px) {
    .message-sent-child {
      gap: var(--gap-base);
    }
  }

.search-text {
  color: black; /* 회색 기본 색상 */
  position: relative;
  overflow: hidden;
  white-space: nowrap;
}
.search-text::before {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    color: #bbb;
    white-space: nowrap;
    overflow: hidden;
    animation: shine 2s linear infinite;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}
.hello-have-you li {
  padding-left: 5px;
}
@keyframes shine {
  0% {
      clip-path: inset(0 100% 0 0);
  }
  50% {
      clip-path: inset(0 0 0 0);
  }
  100% {
      clip-path: inset(0 0 0 100%);
  }
}
</style>