<template>
  <div id="register">
    <input
      autocomplete="off"
      tabindex="1"
      placeholder="Name"
      type="text"
      class="input"
      v-model="userName"
    />
    <input
      autocomplete="off"
      tabindex="1"
      placeholder="Password"
      type="password"
      class="input"
      v-model="password"
    />
    <input
      autocomplete="off"
      tabindex="1"
      placeholder="Confirm Password"
      type="password"
      class="input"
      v-model="confirmPassword"
    />
    <div id="button-area">
      <button class="button" id="login-button" type="button" @click="cancel()">
        Cancel
      </button>
      <button
        class="button"
        id="register-button"
        type="button"
        @click="register()"
      >
        Sign up
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { ElMessage } from "element-plus";

export default {
  name: "RegisterWindow",
  data() {
    return {
      userName: "",
      password: "",
      confirmPassword: "",
    };
  },
  methods: {
    cancel() {
      this.$emit("cancel");
    },
    async register() {
      if (this.password != this.confirmPassword) {
        ElMessage.error("Passwords and confirmed password should be the same");
        return;
      }
      let userName = this.userName;
      let password = this.password;
      var csrftoken = Cookies.get("csrftoken");
      const registerResult = await axios
        .post(
          "register/",
          {
            auth: {
              "user-name": userName,
              password: password,
            },
          },
          {
            headers: {
              "Content-Type": "application/json;charset=UTF-8",
              "X-CSRFToken": csrftoken,
            },
          }
        )
        .then(function (response) {
          console.log(response);
          return response;
        })
        .catch(function (error) {
          console.log(error);
          return error;
        });
      let statusCode = registerResult["status"];
      if (statusCode == "200") {
        ElMessage({
          type: "success",
          message: "Successfully register",
        });
        this.$emit("registerSuccess");
      }
      else {
        ElMessage.error("Register failed!");
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#register {
  display: table;
  width: 50%;
  height: calc(100% - 170px);
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
  margin: 25px;
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
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.12) !important;
  border: 0;
  outline: 0;
  color: rgba(0, 0, 0, 0.87);
  min-height: 1em;
  height: 50px;
  width: 25%;
  will-change: box-shadow;
  font-family: Roboto, sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: white;
  position: relative;
  display: inline-block;
  margin: 0 auto;
  margin-left: 20px;
  margin-right: 20px;
}
#login-button {
  background-color: hsla(0, 100%, 59%, 0.75) !important;
}
#register-button {
  background-color: hsla(102, 66%, 44%, 0.75) !important;
}
.button:hover {
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.5) !important;
  transform: scale(1.1) perspective(0px);
}
.button:active {
  filter: invert(0.3);
}
</style>
