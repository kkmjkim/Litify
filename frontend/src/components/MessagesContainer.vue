<template>
  <div class="messages-container">
    <a class="messages">Litify</a>
    <!-- Save time for lawyers, Make legal assistance easy for clients. -->
    <!-- Criminal Complaint Drafting System -->
    <div class="messages-container-inner">
      <div class="frame-parent1">
        <div class="shape-wrapper1">
          <img class="shape-icon3" alt="" src="/shape-3.svg" />
        </div>
        <!-- <a class="search">Search</a> -->
        <input 
          contenteditable="true" 
          style="outline:none" 
          class="type-your-message"
          placeholder="Search"
        >
      </div>
    </div>
    <div class="messages-container-child">
      <div class="active-chat-parent">
        <div 
          v-for="(chat, i) in chatList" 
          class="active-chat" 
          :class="chat == activeChat?'active':''"
          @click="clickChatRoom(i)"
        >
          <ChatRomeList 
            :message="chat"
          />
        </div> 
      </div>
    </div>
  </div>
</template>
<script>
  import { defineComponent } from "vue";
  import ChatRomeList from "./ChatRoomList.vue";

  export default defineComponent({
    name: "MessagesContainer",
    components: { ChatRomeList },
    props: ["chatList", "activeChat"],
    data() {
      return {
      }
    },
    methods: {
      clickChatRoom(chatroomId) {
        console.log(chatroomId)
        this.$emit("clickChatRoom", chatroomId)
      }
    }
  });
</script>
<style scoped>
  .messages {
    text-decoration: none;
    position: relative;
    font-size: var(--font-size-4xl);
    line-height: 16px;
    font-weight: 700;
    font-family: var(--font-sf-pro-text);
    color: inherit;
  }
  .shape-icon3 {
    width: 10px;
    height: 10px;
    position: relative;
  }
  .shape-wrapper1 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-9xs-5) 0px 0px;
  }
  .search {
    text-decoration: none;
    width: 121px;
    position: relative;
    color: inherit;
    display: inline-block;
    flex-shrink: 0;
  }
  .frame-parent1 {
    flex: 1;
    border-radius: var(--br-xs);
    background-color: var(--color-whitesmoke-200);
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: var(--padding-3xs-5) var(--padding-xs);
    gap: var(--gap-base);
  }
  .messages-container-inner {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px 0px 0px var(--padding-11xs);
    top: 0;
    z-index: 99;
    position: sticky;
    color: var(--black-45);
  }
  .group-icon {
    height: 12px;
    width: 12px;
    position: relative;
  }
  .john-doe {
    text-decoration: none;
    position: relative;
    line-height: 16px;
    font-weight: 500;
    color: inherit;
  }
  .active-chat {
    align-self: stretch;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: var(--gap-base);
    margin-bottom: 5px;
  }
  .active-chat:hover {
    background-color: var(--color-whitesmoke-100);
    border-radius: 5px;
    cursor: pointer;
  }
  .active-chat:active {
    background-color: var(--color-gray-200);
    border-radius: 5px;
    transition: background-color 0.5s ease;
    /* background: radial-gradient(circle); */
  }
  .active-chat.active {
    background-color: var(--color-whitesmoke-100);
    font-weight: 700 !important;
    border-radius: 5px;
    /* background: radial-gradient(circle); */
  }
  .active-chat.active:hover {
    background-color: var(--color-gray-200);
    border-radius: 5px;
    cursor: pointer;
  }
  .awesome {
    align-self: stretch;
    position: relative;
    line-height: 16px;
  }
  .single-icon {
    position: relative;
    line-height: 16px;
    font-weight: 500;
  }
  .single-icon-wrapper {
    width: 14px;
    height: 14px;
    border-radius: var(--br-72xl);
    background-color: var(--green-2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--padding-12xs-5) var(--padding-10xs);
    box-sizing: border-box;
    font-size: var(--font-size-3xs);
    color: var(--color-white);
  }
  .chat-item-icons {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    gap: var(--gap-9xs);
    font-size: var(--font-size-xs);
    color: var(--color-gray-300);
  }
  .are-you-interested {
    position: relative;
    line-height: 16px;
    color: var(--black-45);
  }
  .frame-parent6 {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: var(--gap-xs);
  }
  .chat-list-container3 {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: var(--gap-12xs);
  }
  .vivienne-westwood {
    position: relative;
    line-height: 16px;
    font-weight: 500;
    display: inline-block;
    min-width: 121px;
  }
  .active-chat-parent {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px 0px var(--padding-11xl);
    /* gap: var(--gap-base); */
  }
  .messages-container-child {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px 0px 0px var(--padding-11xs);
    color: var(--black-85);
  }
  .messages-container {
    align-self: stretch;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px 0px var(--padding-574xl);
    box-sizing: border-box;
    gap: var(--gap-base-5);
    text-align: left;
    font-size: var(--font-size-sm);
    color: var(--color-black);
    font-family: var(--font-sf-pro-display);
  }

  @media screen and (max-width: 1000px) {
    .messages-container {
      padding-bottom: var(--padding-366xl);
      box-sizing: border-box;
    }
  }
  @media screen and (max-width: 725px) {
    .messages-container {
      padding-bottom: var(--padding-231xl);
      box-sizing: border-box;
    }
  }
  @media screen and (max-width: 450px) {
    .messages {
      font-size: var(--font-size-lg);
      line-height: 13px;
    }
  }
</style>
