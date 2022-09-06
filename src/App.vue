<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <img
    alt="Vue logo"
    src="./icons/logo.png"
    style="width: 150px"
    draggable="false"
  />
  <Transition name="slide-up" mode="out-in">
    <LoginWindow v-if="currentWindow === 'LoginWindow'" @register="register"/>
    <RegisterWindow v-else-if="currentWindow === 'RegisterWindow'" @cancel="cancel"/>
  </Transition>
</template>

<script>
import LoginWindow from "./components/Login.vue";
import RegisterWindow from "./components/Register.vue";

export default {
  name: "App",
  components: {
    LoginWindow,
    RegisterWindow,
  },
  data() {
    return {
      windowList: ["LoginWindow", "RegisterWindow"],
      currentWindow: "LoginWindow",
    };
  },
  methods: {
    register() {
      this.currentWindow = "RegisterWindow";
    },
    cancel() {
      this.currentWindow = "LoginWindow";
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-image: url("https://cn.bing.com/th?id=OHR.SeitanLimania_ZH-CN3831790369_UHD.jpg&rf=LaDigue_UHD.jpg&w=3840&h=2160&c=8&rs=1&o=3&r=0");
  background-attachment: fixed;
  background-size: cover;
  background-repeat: no-repeat;
  width: 100%;
  height: 100%;
}
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.25s ease-out;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>
