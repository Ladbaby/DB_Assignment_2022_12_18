<template>
  <!-- <div id="navigator">
    <div id="logo-div">
      <img alt="Vue logo" src="../icons/logo.png" id="logo" draggable="false" />
      <ul id="user-dropdown">
        <li class="dropdown-item">User</li>
      </ul>
    </div>
    <div id="search-box">
      <input
        autocomplete="off"
        tabindex="1"
        placeholder=" Search..."
        type="text"
        class="search-box-input"
      />
    </div>
    <div id="item-controls">
      <Transition name="buttons-up" mode="out-in">
        <div
          class="button"
          id="add-button"
          @click="addItem()"
          v-if="!ifEditShow"
        >
          <img
            class="icon"
            srcset="
              ../icons/add-32.png  1x,
              ../icons/add-32.png  1.25x,
              ../icons/add-32.png  1.5x,
              ../icons/add-32.png  1.75x,
              ../icons/add-64.png  2x,
              ../icons/add-64.png  2.25x,
              ../icons/add-64.png  2.5x,
              ../icons/add-128.png 3x,
              ../icons/add-128.png 3.5x
            "
            draggable="false"
          />
        </div>
        <div
          class="button"
          id="check-button"
          @click="confirmItem()"
          v-else-if="ifEditShow"
        >
          <img
            class="icon"
            srcset="
              ../icons/check-32.png  1x,
              ../icons/check-32.png  1.25x,
              ../icons/check-32.png  1.5x,
              ../icons/check-32.png  1.75x,
              ../icons/check-64.png  2x,
              ../icons/check-64.png  2.25x,
              ../icons/check-64.png  2.5x,
              ../icons/check-128.png 3x,
              ../icons/check-128.png 3.5x
            "
            draggable="false"
          />
        </div>
      </Transition>
      <Transition name="buttons-up" mode="out-in">
        <div
          class="button"
          id="edit-button"
          @click="editItem()"
          v-if="!ifEditShow"
        >
          <img
            class="icon"
            srcset="
              ../icons/edit-32.png  1x,
              ../icons/edit-32.png  1.25x,
              ../icons/edit-32.png  1.5x,
              ../icons/edit-32.png  1.75x,
              ../icons/edit-64.png  2x,
              ../icons/edit-64.png  2.25x,
              ../icons/edit-64.png  2.5x,
              ../icons/edit-128.png 3x,
              ../icons/edit-128.png 3.5x
            "
            draggable="false"
          />
        </div>
        <div
          class="button"
          id="cancel-button"
          @click="abortNewItem()"
          v-else-if="ifEditShow"
        >
          <img
            class="icon"
            srcset="
              ../icons/cancel-32.png  1x,
              ../icons/cancel-32.png  1.25x,
              ../icons/cancel-32.png  1.5x,
              ../icons/cancel-32.png  1.75x,
              ../icons/cancel-64.png  2x,
              ../icons/cancel-64.png  2.25x,
              ../icons/cancel-64.png  2.5x,
              ../icons/cancel-128.png 3x,
              ../icons/cancel-128.png 3.5x
            "
            draggable="false"
          />
        </div>
      </Transition>
      <Transition name="buttons-up" mode="out-in">
        <div
          class="button"
          id="return-button"
          @click="hideDetail()"
          v-if="ifShowDetail"
        >
          <img
            class="icon"
            srcset="
              ../icons/return-32.png  1x,
              ../icons/return-32.png  1.25x,
              ../icons/return-32.png  1.5x,
              ../icons/return-32.png  1.75x,
              ../icons/return-64.png  2x,
              ../icons/return-64.png  2.25x,
              ../icons/return-64.png  2.5x,
              ../icons/return-128.png 3x,
              ../icons/return-128.png 3.5x
            "
            draggable="false"
          />
        </div>
        <div
          class="button"
          id="settings-button"
          @click="openSettings()"
          v-else-if="!ifShowDetail"
        >
          <img
            class="icon"
            srcset="
              ../icons/settings-32.png  1x,
              ../icons/settings-32.png  1.25x,
              ../icons/settings-32.png  1.5x,
              ../icons/settings-32.png  1.75x,
              ../icons/settings-64.png  2x,
              ../icons/settings-64.png  2.25x,
              ../icons/settings-64.png  2.5x,
              ../icons/settings-128.png 3x,
              ../icons/settings-128.png 3.5x
            "
            draggable="false"
          />
        </div>
      </Transition>
    </div>
  </div> -->
  <el-affix>
    <el-menu
      default-active="1"
      id="navigator"
      mode="horizontal"
      @select="handleSelect"
      :ellipsis="false"
    >
      <!-- <el-space spacer="|"> -->
        <el-menu-item index="1"
          ><el-avatar :size="55" :src="require('@/icons/logo.png')" /></el-menu-item>
        <el-menu-item index="2"
          ><el-icon size="55px"> <Setting /> </el-icon
        ></el-menu-item>
        <el-menu-item index="3"
          ><el-icon size="55px"> <Search /> </el-icon
        ></el-menu-item>
        <div class="flex-grow" />
        <el-menu-item index="3"
          ><el-icon size="55px"> <Plus /> </el-icon
        ></el-menu-item>
      <!-- </el-space> -->
    </el-menu>
    <el-input v-model="input3" placeholder="Please input" id="search-box">
      <template #prepend>
        <el-select v-model="select" placeholder="All" style="width: 115px">
          <el-option label="All" value="1" />
          <el-option label="Artist" value="2" />
          <el-option label="Album" value="3" />
        </el-select>
      </template>
    </el-input>
  </el-affix>
  <div id="body">
    <Transition name="add-item-up">
      <div id="add-div" v-if="ifEditShow"></div>
    </Transition>
  </div>
  <el-backtop :right="100" :bottom="100" />
</template>

<script>
// import BaseHeader from "@/components/layouts/BaseHeader.vue"
// import { mdiAccount } from '@mdi/js'
// import SvgIcon from '@jamescoyle/vue-icon'
export default {
  name: "MainUI",
  data() {
    return {
      ifEditShow: false,
      icons: {
        // mdiAccount,
      },
    };
  },
  components: {
    // SvgIcon,
  },
  methods: {
    login() {
      this.$emit("login");
    },
    register() {
      this.$emit("register");
    },
    addItem() {
      this.ifEditShow = true;
      return;
    },
    confirmItem() {
      this.ifEditShow = false;
      return;
    },
    editItem() {
      return;
    },
    abortNewItem() {
      this.ifEditShow = false;
      return;
    },
    hideDetail() {
      return;
    },
    openSettings() {
      return;
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#login {
  display: table;
  width: 50%;
  height: 100%;
  backdrop-filter: blur(5px);
  margin: 0 auto;
  border-radius: 30px;
  background-color: hsla(0, 0%, 100%, 0.5) !important;
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.5) !important;
}

input.input {
  border-radius: 20px;
  background-color: hsla(0, 0%, 100%, 0.75) !important;
  transition: box-shadow 0.2s, transform 0.2s;
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.12) !important;
  border: 0;
  outline: 0;
  color: rgba(0, 0, 0, 0.87);
  min-height: 1em;
  height: 50px;
  width: 50%;
  will-change: box-shadow;
  font-family: Roboto, sans-serif;
  font-size: 16px;
  overflow-x: auto;
  position: relative;
  display: table-row;
  padding-left: 10px;
  margin: 30px;
}
input.input:hover {
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.5) !important;
  transform: scale(1.02) perspective(0px);
}
input.input:focus {
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.7) !important;
}
#button-area {
  display: table-row;
  width: 100%;
}
.button {
  border-radius: 20px;
  transition: box-shadow 0.2s, transform 0.2s;
}
#login-button {
  background-color: hsla(206, 100%, 59%, 0.75) !important;
}
#register-button {
  background-color: hsla(102, 66%, 44%, 0.75) !important;
}
.button:active {
  filter: invert(0.3);
}
#navigator {
  /* height: 32px;
  margin-top: 0px;
  transform: translateY(0px);
  left: 0px;
  right: 0px;
  position: fixed;
  z-index: 100;
  min-height: calc(56px + env(safe-area-inset-top)) !important;
  transition: all 0.225s cubic-bezier(0.165, 0.84, 0.44, 1);
  contain: layout;
  display: block;
  flex: 1 1 auto;
  max-width: 100%;
  font-family: Roboto, sans-serif;
  overflow: visible;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -webkit-text-size-adjust: 100%; */
  background-color: hsla(0, 0%, 100%, 0.5) !important;
  -webkit-backdrop-filter: blur(5px);
  backdrop-filter: blur(5px);
  color: #000 !important;
  /* padding: 5px 10px; */
}
#logo {
  height: 55px;
  transition: box-shadow 0.1s ease-in-out;
  border-radius: 15px;
}
/* #logo:hover {
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 5px 8px 0 rgb(0 0 0 / 50%),
    0 1px 14px 0 rgb(0 0 0 / 70%) !important;
} */
#search-box {
  border-radius: 12px;
  background-color: hsla(0, 0%, 100%, 0.75) !important;
  transition: box-shadow 0.2s ease-in-out, width 0.4s ease-in-out;
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 5px 8px 0 rgb(0 0 0 / 14%),
    0 1px 14px 0 rgb(0 0 0 / 12%) !important;
  border: 0;
  color: rgba(0, 0, 0, 0.87);
  height: 32px;
  width: 20%;
  will-change: box-shadow;
  font-family: Roboto, sans-serif;
  font-size: 16px;
  overflow-x: visible;
  position: relative;
  top: calc(50% - 16px);
  float: left;
  padding-left: 10px;
  margin-left: 20px;
}
#search-select {
  padding: 4px 0 4px 5px;
  min-width: 35px;
  height: 100%;
  border: none;
  outline: none;
  box-shadow: none;
  background-color: transparent;
  background-image: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  -moz-border-radius: 0;
  -webkit-border-radius: 0;
  border-radius: 0;
  border-right: 1px solid #ddd;
  color: #000;
}
input.search-box-input {
  width: 120px;
  -webkit-appearance: none;
  -moz-appearance: none;
  box-shadow: none;
  background: transparent;
  line-height: 20px;
  width: 160px;
  height: 100%;
  border: none;
  -webkit-appearance: caret;
}
input.search-box-input:focus {
  outline: none !important;
}
#search-box:hover {
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 5px 8px 0 rgb(0 0 0 / 14%),
    0 1px 14px 0 rgb(0 0 0 / 70%) !important;
}
#search-box:focus {
  outline: none !important;
  width: 40%;
}
#item-controls {
  display: grid;
  grid-template-columns: repeat(3, 46px);
  position: absolute;
  top: 0;
  right: 10px;
  height: 100%;
  -webkit-app-region: no-drag;
}
#item-controls .button {
  grid-row: 1 / span 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  user-select: none;
}
#add-button {
  grid-column: 1;
}
#check-button {
  grid-column: 1;
}
#cancel-button {
  grid-column: 2;
}
#edit-button {
  grid-column: 2;
}
#return-button {
  grid-column: 3;
}
#settings-button {
  grid-column: 3;
}
@media (-webkit-device-pixel-ratio: 1.5),
  (device-pixel-ratio: 1.5),
  (-webkit-device-pixel-ratio: 2),
  (device-pixel-ratio: 2),
  (-webkit-device-pixel-ratio: 3),
  (device-pixel-ratio: 3) {
  #item-controls .icon {
    width: 32px;
    height: 32px;
  }
}
#item-controls img {
  width: auto;
  height: 50%;
}
#item-controls #add-button:hover img {
  transform-origin: center center;
  animation: scaleRotate 0.2s ease-in-out forwards;
}
#item-controls #cancel-button:hover img {
  transform-origin: center center;
  animation: scaleRotate 0.2s ease-in-out forwards;
}
#item-controls #edit-button:hover img {
  transform-origin: center center;
  animation: scale 0.2s ease-in-out forwards;
}
#item-controls #check-button:hover img {
  transform-origin: center center;
  animation: scale 0.2s ease-in-out forwards;
}
#item-controls #return-button:hover img {
  transform-origin: center center;
  animation: scale 0.2s ease-in-out forwards;
}
#item-controls #settings-button:hover img {
  transform-origin: center center;
  animation: scaleRotate 0.2s ease-in-out forwards;
}
@keyframes scaleRotate {
  0% {
    transform: rotate(0deg) scale(1);
    -webkit-transform: rotate(0deg) scale(1);
  }
  100% {
    transform: rotate(90deg) scale(1.3);
    -webkit-transform: rotate(90deg) scale(1.3);
  }
}
@keyframes scale {
  0% {
    transform: scale(1);
    -webkit-transform: scale(1);
  }
  100% {
    transform: scale(1.3);
    -webkit-transform: scale(1.3);
  }
}
#add-button:active .icon {
  filter: invert(1);
}
#cancel-button:active .icon {
  filter: invert(1);
}
#edit-button:active .icon {
  filter: invert(1);
}
#check-button:active .icon {
  filter: invert(1);
}
#return-button:active .icon {
  filter: invert(1);
}
#settings-button:active .icon {
  filter: invert(1);
}
#body {
  width: 100%;
  height: 100%;
  display: flex;
}
#add-div {
  width: calc(100% - 20px);
  height: calc(100% - 86px);
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: hsla(0, 0%, 100%, 0.7) !important;
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 5px 8px 0 rgb(0 0 0 / 14%),
    0 1px 14px 0 rgb(0 0 0 / 12%) !important;
  border-radius: 30px;
  backdrop-filter: blur(5px);
  transition: all 0.5s ease-in-out;
}
.add-item-up-enter-active .add-item-up-leave-active {
  transition: all 0.5s ease-in-out;
}
.add-item-up-enter-from,
.add-item-up-leave-to {
  transform: translateY(1000px);
  opacity: 0;
}
.buttons-up-enter-active,
.buttons-up-leave-active {
  transition: all 0.2s ease-in-out;
}
.buttons-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
.buttons-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
#logo-div {
  height: 100%;
  float: left;
  overflow: visible;
}
#user-dropdown {
  background-color: hsla(0, 0%, 100%, 1) !important;
  border-radius: 20px;
  will-change: visibility;
  position: absolute;
  z-index: 99;
  width: 20%;
  top: 66px;
  left: 0px;
  visibility: hidden;
  opacity: 0;
  transform: translateY(-4px);
  transition: opacity 0.25s, visibility 0.25s, transform 0.25s;
  margin: 0 auto;
  list-style-type: none;
  padding: 5px;
}
#logo-div:hover #user-dropdown {
  pointer-events: auto;
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
#search-select {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}
.select-item {
  padding: 5px;
}
.flex-grow {
  flex-grow: 1;
}
</style>
