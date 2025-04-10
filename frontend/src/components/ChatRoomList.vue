<template>
    <div class="chat-container">
        <div class="active-chat-container2">
            <div class="active-chat-details">
                <div class="active-chat-user-names">
                <div class="travis-barker">{{ message.title }}</div>
                </div>
            </div>
            <div class="active-chat-timestamps">
                <div class="empty-timestamps">{{ message.timestamp }}</div>
            </div>
        </div> 
    </div>
</template>
<script>

  import { defineComponent } from "vue";

  export default defineComponent({
    name: "ChatRomeList",
    props: [ "message" ],
  });
  
</script>
<style scoped>

.active-chat-users {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: var(--gap-9xs);
  }
  .how-are-you {
    align-self: stretch;
    position: relative;
    line-height: 16px;
    color: var(--black-45);
    /* 메시지 생략 */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 180px;
  }
  .active-chat-user-names {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: var(--gap-11xs);
  }
  .active-chat-details {
    width: 180px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: var(--gap-xs);
  }
  .empty-timestamps {
    position: relative;
    line-height: 16px;
  }
  .active-chat-container {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: var(--gap-xl);
  }
  .active-chat-timestamps {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    gap: var(--gap-7xs);
    font-size: var(--font-size-xs);
    color: var(--color-gray-300);
  }
  .active-chat-details-child {
    height: 36px;
    width: 36px;
    position: relative;
    border-radius: 50%;
  }
  .travis-barker {
    width: 150px;
    position: relative;
    line-height: 16px;
    font-weight: 500;
    display: inline-block;
  }
  .is-typing {
    align-self: stretch;
    position: relative;
    line-height: 16px;
    color: var(--green-2);
  }
  .active-chat-container2 {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--gap-xl);
  }
  .chat-container {
    padding: 8px;
    width: 262px;
  }
</style>