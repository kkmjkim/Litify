<template>
  <div class="rectangle-parent">
    <div class="frame-child" ></div>
    <div class="frame-parent">
      <div class="frame-wrapper">
        <div class="remix-iconslinelogosmasterc-parent">
          <img
            class="remix-iconslinelogosmasterc"
            loading="lazy"
            alt=""
            src="/remixiconslinelogosmastercardline.svg"
          />
          <!-- <img
            class="mastercard-logo-icon"
            loading="lazy"
            alt=""
            src="/ellipse-13@2x.png"
          /> -->
        </div>
      </div>
      <div class="frame-group">
        <div class="line-wrapper">
          <div class="frame-item" />
        </div>
        <div class="frame-container">
          <v-btn icon
            v-for="m in menu"
            @click="m.clickHandler"
            :class="m.active?'subtract-wrapper':'fill-1171-wrapper'" 
            variant="text"
          >
            <img 
              :src="'./ls-'+m.name+'-'+(m.active? 'white':'green')+'.svg'" 
            />
          </v-btn>
        </div>
      </div>
    </div>
    <div class="frame-div">
      <v-btn icon class="fill-1171-wrapper" variant="text">
        <img
          class="fill-1172-icon"
          loading="lazy"
          alt=""
          src="/fill-1172.svg"
        />
      </v-btn>
      <v-btn icon class="fill-1171-wrapper" variant="text">
        <img class="shape-icon2" alt="" src="/shape-2.svg" />
      </v-btn>
    </div>
  </div>
</template>
<script>
  import { defineComponent } from "vue";

  export default defineComponent({
    name: "LeftSideBar",
    data() {
      return {
        // selected: 'chatroom',
        menu: [
          { name: "chatroom", title: "Profile", active: true, clickHandler: this.createNewChat },
          { name: "newchat", title: "Home"},
          { name: "calander", title: "Settings"},
          // { icon: "mdi-logout", title: "Logout" },
        ]
      }
    },
    methods: {
      createNewChat() {
        this.$emit('newChat')
      }
    }
    // watch: {
    //   selected(val) {
    //     this.menu.forEach(m => m.active = m.name === val)
    //   }
    // }
  });
</script>
<style scoped>
  .frame-child {
    width: 54px;
    height: 690px;
    position: relative;
    background-color: var(--color-gray-100);
    display: none;
  }
  .remix-iconslinelogosmasterc {
    width: 32px;
    height: 32px;
    position: relative;
    overflow: hidden;
    flex-shrink: 0;
    z-index: 1;
  }
  .mastercard-logo-icon {
    width: 32px;
    height: 32px;
    position: relative;
    border-radius: 50%;
    object-fit: cover;
    z-index: 1;
  }
  .remix-iconslinelogosmasterc-parent {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: var(--gap-sm);
  }
  .frame-wrapper {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px var(--padding-8xs);
  }
  .frame-item {
    height: 1px;
    width: 43px;
    position: relative;
    border-top: 1px solid var(--color-gray-200);
    box-sizing: border-box;
    z-index: 1;
  }
  .line-wrapper {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0px var(--padding-11xs) 0px var(--padding-10xs);
  }
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
  .subtract-wrapper {
    box-shadow: 0px 4px 4px rgba(39, 174, 96, 0.25);
    border-radius: var(--br-base);
    background-color: var(--green-2);
    display: flex;
    flex-direction: row;
    /* align-items: flex-start;
    justify-content: flex-start; */
    padding: var(--padding-xs);
    z-index: 1;
  }
  .shape-icon {
    width: 18px;
    height: 12.5px;
    position: relative;
  }
  .shape-wrapper {
    width: 42px;
    height: 42px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--padding-3xs);
    box-sizing: border-box;
    z-index: 1;
  }
  .fill-901-icon {
    height: 17px;
    width: 15px;
    position: relative;
  }
  .frame-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--gap-7xs);
  }
  .frame-group {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: var(--gap-smi);
  }
  .frame-parent {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--gap-xl);
  }
  .fill-1172-icon {
    height: 18px;
    width: 16.6px;
    position: relative;
  }
  .shape-icon2 {
    height: 18px;
    width: 17px;
    position: relative;
    object-fit: contain;
  }
  .frame-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 48px;
    bottom: 0;
    /* position: fixed; */
  }
  .rectangle-parent {
    background-color: var(--color-gray-100);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-between;
    padding: var(--padding-2xl) var(--padding-7xs) var(--padding-7xs);
    /* gap: var(--gap-211xl); */
    height: 100vh;
  }
</style>
