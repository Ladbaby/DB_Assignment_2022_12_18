<template>
  <div id="top-bar">
    <el-menu
      default-active="1"
      id="navigator"
      mode="horizontal"
      @select="handleSelect"
      :ellipsis="false"
    >
      <el-menu-item index="1"
        ><el-avatar :size="55" :src="require('@/icons/logo.png')"
      /></el-menu-item>
      <el-menu-item index="2"
        ><el-icon size="55px"> <Setting /> </el-icon
      ></el-menu-item>
      <el-menu-item index="3"
        ><el-icon size="55px"> <Plus /> </el-icon
      ></el-menu-item>
      <div class="flex-grow" />
      <el-menu-item index="4">
        <el-icon size="55px" color="#FF0000"><SwitchButton /></el-icon>
      </el-menu-item>
    </el-menu>
    <transition name="el-zoom-in-center">
      <el-input
        v-model="searchInput"
        placeholder="Search..."
        id="search-box"
        v-if="ifSearchShow"
      >
        <template #prepend>
          <el-select v-model="searchCat" placeholder="All" style="width: 115px">
            <el-option label="All" value="All" />
            <el-option label="Artist" value="Artist" />
            <el-option label="Album" value="Album" />
          </el-select>
        </template>
        <template #append>
          <el-button @click="handleSearch"><el-icon><Search/></el-icon></el-button>
        </template>
      </el-input>
    </transition>
  </div>
  <div id="body">
    <Transition name="add-item-up">
      <el-container id="add-div" v-if="currentTab == 'upload'">
        <el-header height="90px">
          <!-- <audio :src="src" controls></audio> -->
          <el-steps
            :active="stepActive"
            finish-status="success"
            id="step"
            align-center
          >
            <el-step title="Step 1" description="upload files" />
            <el-step title="Step 2" description="specify artist" />
            <el-step title="Step 3" description="specify album" />
          </el-steps>
        </el-header>
        <el-main id="upload-main">
          <Transition name="slide-up" mode="out-in">
            <el-upload
              id="upload-demo"
              drag
              action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
              multiple
              :auto-upload="false"
              :on-change="handleChange"
              v-model:file-list="fileList"
              v-if="stepActive == 0"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                Drop file here or <em>click to upload</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  jpg/png files with a size less than 500kb
                </div>
              </template>
            </el-upload>
            <div v-else-if="stepActive == 1" id="upload-artist-div">
              <el-row :gutter="20">
                <el-col :span="24">
                  <center>
                    <h2>Enter artist's name:</h2>
                  </center>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="24">
                  <center>
                    <input
                      autocomplete="off"
                      tabindex="1"
                      placeholder="artist's name"
                      type="text"
                      class="input"
                      v-model="uploadArtistName"
                    />
                  </center>
                </el-col>
              </el-row>
            </div>
            <div v-else-if="stepActive == 2" id="upload-album-div">
              <el-row :gutter="20">
                <el-col :span="24">
                  <center>
                    <h2>Enter album's name:</h2>
                  </center>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="24">
                  <center>
                    <input
                      autocomplete="off"
                      tabindex="1"
                      placeholder="album's name"
                      type="text"
                      class="input"
                      v-model="uploadAlbumName"
                    />
                  </center>
                </el-col>
              </el-row>
            </div>
          </Transition>
        </el-main>
        <el-footer>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-button
                type="primary"
                icon="DArrowLeft"
                size="large"
                round
                @click="back"
              >
                Back
              </el-button>
            </el-col>
            <el-col :span="12"></el-col>
            <el-col :span="6">
              <el-button type="primary" size="large" round @click="next">
                Next
                <el-icon class="el-icon--right"><DArrowRight /></el-icon>
              </el-button>
            </el-col>
          </el-row>
        </el-footer>
      </el-container>
      <div id="music-list-div" v-else-if="currentTab == 'main'">
        <ul id="music-list-ul">
          <li
            class="music-card"
            v-for="item in musicList"
            :key="item"
            @click="handleAlbumClicked(item)"
          >
            <el-card
              :body-style="{ padding: '5px' }"
              :style="{
                borderRadius: '10px',
              }"
              shadow="always"
              round
            >
              <img
                src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
                class="image"
              />
              <div style="padding: 14px">
                <span style="overflow-wrap: anywhere">{{ item["name"] }}</span>
                <div class="bottom">
                  <span
                    ><small>{{ item["artist"] }}</small></span
                  >
                  <el-button
                    type="warning"
                    icon="Star"
                    circle
                    v-show="ifShowAllAlbum"
                    @click="addToCollection(item.id)"
                  />
                </div>
              </div>
            </el-card>
          </li>
        </ul>
        <div id="album-container" v-if="ifShowAlbumDetail">
          <AlbumDetail
            :album="selectedAlbum"
            @album-detail-return="albumDetailReturn"
          ></AlbumDetail>
        </div>
      </div>
      <div id="notification-div" v-else-if="currentTab == 'notification'">
        <NotificationView :isAdmin="isAdmin"></NotificationView>
      </div>
    </Transition>
  </div>
  <Transition name="add-item-up">
    <div id="tool-bar" v-if="currentTab == 'main'">
      <!-- <Transition name="tool-bar-transition"> -->
      <el-space direction="vertical">
        <Transition name="tool-bar-transition">
          <el-button
            icon="Search"
            size="large"
            circle
            @click="showSearchBox"
            v-if="currentTab == 'main'"
          />
        </Transition>
        <Transition name="tool-bar-transition">
          <el-button
            type="primary"
            icon="Edit"
            size="large"
            circle
            v-if="currentTab == 'main'"
          />
        </Transition>
        <Transition name="tool-bar-transition">
          <el-button
            type="success"
            icon="Check"
            size="large"
            circle
            @click="handleCheck"
            v-if="currentTab == 'upload'"
          />
        </Transition>
        <Transition name="tool-bar-transition">
          <el-button
            type="warning"
            icon="Star"
            size="large"
            circle
            @click="handleStar"
            v-if="currentTab == 'main'"
          />
        </Transition>
        <Transition name="tool-bar-transition">
          <el-button
            type="danger"
            icon="Delete"
            size="large"
            circle
            v-if="currentTab == 'main'"
          />
        </Transition>
      </el-space>
      <!-- </Transition> -->
    </div>
  </Transition>
  <el-backtop :right="100" :bottom="100" />
</template>

<script>
import { ElMessage, ElMessageBox } from "element-plus";
import axios from "axios";
import Cookies from "js-cookie";
import AlbumDetail from "./AlbumDetail.vue";
import NotificationView from "./NotificationView.vue";

export default {
  name: "MainUI",
  components: {
    AlbumDetail,
    NotificationView,
  },
  props: {
    ifLoggedIn: Boolean,
    isAdmin: Boolean,
  },
  data() {
    return {
      currentTab: "main", // main, notification, upload
      ifSearchShow: false,
      musicList: [
        {
          id: "1",
          name: "test",
          artist: "?",
          tracks: [{ trackID: "1", trackName: "hello" }],
          comments: [{ userID: "1", comment: "wtf" }],
        },
      ],
      fileList: [],
      stepActive: 0,
      uploadArtistName: "",
      uploadAlbumName: "",
      selectedAlbum: "",
      ifShowAlbumDetail: false,
      ifShowAllAlbum: false,
      src: "",
      searchCat: "All",
      searchInput: "",
    };
  },
  watch: {
    ifLoggedIn: {
      handler(newValue) {
        console.log(newValue);
        if (newValue == true) {
          this.showCollection();
        }
      },
      immediate: true,
    },
  },
  methods: {
    login() {
      this.$emit("login");
    },
    register() {
      this.$emit("register");
    },
    handleSelect(key) {
      if (key == 1) {
        this.currentTab = "main";
      } else if (key == 2) {
        this.currentTab = "notification";
      } else if (key == 3) {
        this.currentTab = "upload";
        this.ifSearchShow = false;
      } else if (key == 4) {
        ElMessageBox.confirm("Confirm to logout?", "Warning", {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        })
          .then(() => {
            this.$emit("log-out");
            ElMessage({
              type: "success",
              message: "Successfully logout",
            });
          })
          .catch(() => {
            ElMessage({
              type: "info",
              message: "Logout canceled",
            });
          });
      }
    },
    showSearchBox() {
      this.ifSearchShow = !this.ifSearchShow;
    },
    handleChange(uploadFile) {
      // this.src = URL.createObjectURL(uploadFile.raw);
      this.fileList.push(uploadFile);
    },
    handleCheck() {
      axios
        .post("/upload", {
          data: this.$data,
        })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
          return;
        });
    },
    back() {
      this.stepActive > 0 ? this.stepActive-- : 0;
    },
    async next() {
      if (this.stepActive == 2) {
        const messageResult = await ElMessageBox.confirm(
          "Confirm to upload the Album?",
          "Warning",
          {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            type: "warning",
          }
        )
          .then(() => {
            return "success";
          })
          .catch(() => {
            return "failure";
          });
        var csrftoken = Cookies.get("csrftoken");
        if (messageResult == "success") {
          // let name = this.uploadAlbumName;
          // let artist = this.uploadArtistName;
          // let fileList = this.fileList;
          const formData = new FormData();
          formData.append("name", this.uploadAlbumName);
          formData.append("artist", this.uploadArtistName);
          for (let i = 0; i < this.fileList.length; ++i) {
            formData.append(this.fileList[i].name, this.fileList[i].raw);
          }

          const submitResult = await axios({
            method: "post",
            url: "upload/",
            data: formData,
            headers: {
              "Content-Type": "multipart/form-data",
              "X-CSRFToken": csrftoken,
            },
          })
            .then(function (response) {
              console.log(response);
              return response;
            })
            .catch(function (error) {
              console.log(error);
              return error;
            });
          let statusCode = submitResult["status"];
          if (statusCode == "200") {
            ElMessage({
              type: "success",
              message: "Successfully upload album",
            });
            this.showCollection();
            this.stepActive = 0;
            this.currentTab = "main";
          } else {
            ElMessage.error("Upload failed! Fields' value cannot be empty!");
          }
        } else if (messageResult == "failure") {
          ElMessage({
            type: "info",
            message: "Upload canceled",
          });
        }
      } else {
        this.stepActive < 2 ? this.stepActive++ : 2;
      }
    },
    async showCollection() {
      var csrftoken = Cookies.get("csrftoken");
      let showCollectionResult = await axios
        .get("check-collection/", {
          headers: {
            "Content-Type": "application/json;charset=UTF-8",
            "X-CSRFToken": csrftoken,
          },
        })
        .then(function (response) {
          console.log(response);
          return response;
        })
        .catch(function (error) {
          console.log(error);
          return error;
        });
      let statusCode = showCollectionResult["status"];
      if (statusCode == "200") {
        this.musicList = showCollectionResult["data"]["albums"];
      } else {
        ElMessage.error("Fail to load the albums!");
      }
    },
    handleAlbumClicked(album) {
      this.selectedAlbum = album;
      this.ifShowAlbumDetail = true;
    },
    async handleStar() {
      this.ifShowAllAlbum = !this.ifShowAllAlbum;
      if (this.ifShowAllAlbum) {
        var csrftoken = Cookies.get("csrftoken");
        let showCollectionResult = await axios
          .get("search-album-id/", {
            headers: {
              "Content-Type": "application/json;charset=UTF-8",
              "X-CSRFToken": csrftoken,
            },
          })
          .then(function (response) {
            console.log(response);
            return response;
          })
          .catch(function (error) {
            console.log(error);
            return error;
          });
        let statusCode = showCollectionResult["status"];
        if (statusCode == "200") {
          this.musicList = showCollectionResult["data"]["albums"];
        } else {
          ElMessage.error("Fail to load the albums!");
        }
      } else {
        this.showCollection();
      }
    },
    albumDetailReturn() {
      this.ifShowAlbumDetail = false;
    },
    async addToCollection(albumID) {
      console.log(albumID);
      var csrftoken = Cookies.get("csrftoken");
      let addToCollectionResult = await axios
        .post(
          "add-album/",
          {
            id: albumID,
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
      let statusCode = addToCollectionResult["status"];
      if (statusCode == "200") {
        ElMessage({
          type: "success",
          message: "Waiting for administrator to permit the request",
        });
      } else {
        ElMessage.error("Request fail!");
      }
    },
    async handleSearch() {
      var csrftoken = Cookies.get("csrftoken");
      if (this.searchCat == "Artist") {
        artistName = this.searchInput;
        let searchResult = await axios
          .get(
            "search-artist?target=" + artistName,
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
        let statusCode = searchResult["status"];
        if (statusCode == "200") {
          console.log("wtf");
        } else {
          ElMessage.error("Request fail!");
        }
      }
    }
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
#notification-button {
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
#item-controls #notification-button:hover img {
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
#notification-button:active .icon {
  filter: invert(1);
}
#body {
  width: 100%;
  height: 100%;
  display: flex;
  /* overflow: auto; */
  transition: all 0.2s ease-in-out;
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
  border-radius: 10px;
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
#tool-bar {
  position: fixed;
  bottom: 20px;
  right: 25px;
  background-color: hsla(0, 0%, 100%, 0.5) !important;
  padding: 10px;
  border-radius: 20px;
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.2) !important;
  transition: all 0.5s ease-in-out;
  backdrop-filter: blur(5px);
}
#upload-demo {
  border-radius: 20px;
  /* height: 100%; */
}
#music-list-div {
  width: 100%;
  height: 100%;
  transition: all 0.5s ease-in-out;
  overflow: auto;
}
#music-list-div::-webkit-scrollbar {
  display: block;
  width: 12px;
}
#music-list-div::-webkit-scrollbar-track {
  background: transparent;
}

#music-list-div::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.804);
  border-right: none;
  border-left: none;
}

#music-list-div::-webkit-scrollbar-track-piece:end {
  background: transparent;
  margin-bottom: 10px;
}

#music-list-div::-webkit-scrollbar-track-piece:start {
  background: transparent;
  margin-top: 64px;
}
#music-list-ul {
  padding: 0;
  padding-top: 80px;
}
.music-card {
  display: inline-block;
  margin: 20px;
  transition: box-shadow 0.2s, transform 0.2s;
  border-radius: 10px;
}
.music-card:hover {
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.5) !important;
  transform: scale(1.03) perspective(0px);
}
#top-bar {
  position: fixed;
  width: 100%;
  z-index: 100;
}
.tool-bar-transition-enter-active {
  transition: all 0.3s ease-in-out;
}
.tool-bar-transition-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

#step {
  margin: 20px;
}
#upload-main {
  margin: 20px;
  border-radius: 10px;
  background-color: hsla(0, 0%, 100%, 0.9) !important;
  overflow: hidden;
}
#upload-artist-div,
#upload-album-div {
  width: 100%;
  height: 100%;
}
input.input {
  border-radius: 20px;
  background-color: hsla(0, 0%, 100%, 0.75) !important;
  transition: box-shadow 0.2s, transform 0.2s, width 0.2s;
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
  width: 50%;
}
.image {
  border-radius: 10px;
}
.slide-up-enter-active {
  animation: flipInY;
  animation-duration: 0.5s;
}
.slide-up-leave-active {
  animation: zoomOut;
  animation-duration: 0.2s;
}
#album-container {
  width: calc(100% - 20px);
  height: calc(100% - 86px);
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: hsla(0, 0%, 100%, 0.7) !important;
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 5px 8px 0 rgb(0 0 0 / 14%),
    0 1px 14px 0 rgb(0 0 0 / 12%) !important;
  border-radius: 10px;
  backdrop-filter: blur(5px);
  transition: all 0.5s ease-in-out;
}
.buttom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
#notification-div {
  /* overflow: hidden; */
  width: calc(100% - 20px);
  height: calc(100% - 86px);
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: hsla(0, 0%, 100%, 0.7) !important;
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 5px 8px 0 rgb(0 0 0 / 14%),
    0 1px 14px 0 rgb(0 0 0 / 12%) !important;
  border-radius: 10px;
  backdrop-filter: blur(5px);
  transition: all 0.5s ease-in-out;
}
</style>
