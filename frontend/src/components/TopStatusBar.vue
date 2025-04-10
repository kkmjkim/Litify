<template>
  <header class="top-status-bar" >
    <div class="top-status-bar-child" />
    <div class="status-bar-content">
      <div class="status-bar-left">
        <div class="status-bar-elements">
          <div class="status-icons">
            <!-- <img class="status-icons-child" alt="" src="/profiles/profile-5.jpg" /> -->
            <img class="status-icons-child" alt="" src="/litify_bot_icon.png" />
            <div class="user-name-status">
              <a class="travis-barker1">Lawyer Assistant</a>
              <a class="online">Powered by Solar</a>
            </div>
          </div>
        </div>
        <div class="frame-parent11">
          <v-btn icon class="fill-1171-wrapper" variant="text">
            <img class="fill-1171-icon" loading="lazy" alt="" src="/vector.svg" />
          </v-btn>
        </div>
      </div>
    </div>
    <div class="top-status-bar-item" />
  </header>
</template>
<script>
  import { defineComponent } from "vue";

  export default defineComponent({
    name: "TopStatusBar",
  });
</script>
<style scoped>
  .fill-1171-icon {
    height: 18px;
    width: 18px;
    position: relative;
  }
  .fill-1171-wrapper {
    width: 42px;
    height: 42px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: var(--padding-3xs);
    box-sizing: border-box;
    z-index: 1;
  }
  .top-status-bar-child {
    align-self: stretch;
    height: 61px;
    position: relative;
    background-color: var(--color-white);
    display: none;
  }
  .status-icons-child {
    height: 36px;
    width: 36px;
    position: relative;
    object-fit: cover;
    border-radius: 50%;
  }
  .travis-barker1 {
    text-decoration: none;
    /* width: 100px; */
    position: relative;
    line-height: 16px;
    font-weight: 500;
    color: inherit;
    display: inline-block;
  }
  .online {
    font-size: 13px !important;
    text-decoration: none;
    align-self: stretch;
    position: relative;
    font-size: var(--font-size-sm);
    line-height: 16px;
    color: var(--green-2);
  }
  .user-name-status {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    padding: var(--padding-10xs) 0px;
    gap: var(--gap-9xs);
  }
  .status-icons {
    width: 252px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    padding: 0px var(--padding-xl) 0px 0px;
    box-sizing: border-box;
    gap: var(--gap-xs);
  }
  .status-bar-elements {
    width: 291px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
  }
  .shape-icon4 {
    width: 18px;
    height: 12.5px;
    position: relative;
  }
  .shape-wrapper2 {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--padding-mini-8) var(--padding-xs) var(--padding-mini-7);
    box-sizing: border-box;
    width: 42px;
    height: 42px;
  }
  .vector-icon {
    height: 18px;
    width: 18px;
    position: relative;
  }
  .vector-wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: var(--padding-xs);
    box-sizing: border-box;
    width: 42px;
    height: 42px;
  }
  .frame-parent11 {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
  }
  .status-bar-left {
    flex: 1;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    max-width: 100%;
    gap: var(--gap-xl);
    z-index: 1;
  }
  .status-bar-content {
    align-self: stretch;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-end;
    padding: 0px var(--padding-4xs) 0px var(--padding-xs);
    box-sizing: border-box;
    max-width: 100%;
  }
  .top-status-bar-item {
    align-self: stretch;
    height: 1px;
    position: relative;
    border-top: 1px solid var(--color-whitesmoke-200);
    box-sizing: border-box;
  }
  .top-status-bar {
    align-self: stretch;
    background-color: var(--color-white);
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    padding: var(--padding-4xs) 0px 0px;
    box-sizing: border-box;
    gap: var(--gap-3xs);
    max-width: 100%;
    z-index: 2;
    text-align: left;
    font-size: var(--font-size-base);
    color: var(--black-85);
    font-family: var(--font-sf-pro-display);
  }

  @media screen and (max-width: 450px) {
    .status-bar-left {
      flex-wrap: wrap;
    }
  }
</style>
