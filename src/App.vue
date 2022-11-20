<template>
    <Transition name="slide" mode="out-in">
      <div id="not-logged-in" v-if="!ifLoggedIn">
        <img
          alt="Vue logo"
          :src="require('@/icons/logo.png')"
          style="width: 150px; height: 150px"
          draggable="false"
        />
        <Transition name="slide-up" mode="out-in">
          <LoginWindow
            v-if="currentWindow === 'LoginWindow'"
            @login="login"
            @register="register"
          />
          <RegisterWindow
            v-else-if="currentWindow === 'RegisterWindow'"
            @cancel="cancel"
            @registerSuccess="registerSuccess"
          />
        </Transition>
      </div>
      <div id="logged-in" v-else-if="ifLoggedIn">
        <MainUI @log-out="handleLogout" :ifLoggedIn="ifLoggedIn"/>
        </div>
    </Transition>
</template>

<script>
import LoginWindow from "./components/Login.vue";
import RegisterWindow from "./components/Register.vue";
import MainUI from "./components/MainUI.vue";

export default {
  name: "App",
  components: {
    LoginWindow,
    RegisterWindow,
    MainUI,
  },
  data() {
    return {
      windowList: ["LoginWindow", "RegisterWindow"],
      currentWindow: "LoginWindow",
      ifLoggedIn: false,
    };
  },
  methods: {
    register() {
      this.currentWindow = "RegisterWindow";
    },
    cancel() {
      this.currentWindow = "LoginWindow";
    },
    login() {
      this.ifLoggedIn = true;
    },
    handleLogout() {
      this.ifLoggedIn = false;
    },
    registerSuccess() {
      this.currentWindow = "LoginWindow";
    }
  },
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
  overflow: hidden;
}
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
.slide-up-enter-active {
  animation: bounceIn;
  animation-duration: 0.5s;
}
.slide-enter-active {
  animation: fadeIn;
  animation-duration: 0.5s;
}
.slide-up-leave-active {
  animation: backOutDown;
  animation-duration: 0.2s;
}
.slide-leave-active {
  animation: backOutRight;
  animation-duration: 0.5s;
}
#not-logged-in {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
#logged-in {
  width: 100%;
  height: 100%;
}
</style>
