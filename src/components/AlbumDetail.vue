<template>
  <el-container id="album-container2">
    <!-- <el-affix target="#album-container2">
      <el-button
        @click="albumDetailReturn"
        id="album-detail-return"
        icon="ArrowLeft"
        size="large"
        ><h1>Return</h1></el-button
      >
    </el-affix> -->
    <el-header id="album-detail-header">
      <el-page-header :icon="ArrowLeft" @back="albumDetailReturn">
        <template #content>
          <span style="color: white; font-size: 24px;">
            {{ this.album.name + " " }}
          </span>
          <span
            style="color: white;"
          >
            <small>{{ this.album.artist }}</small>
          </span>
        </template>
      </el-page-header>
    </el-header>
    <el-main>
      <div v-for="item in album.tracks" :key="item.trackID" id="list-div">
        <el-card class="box-card">
          <div class="card-body">
            <el-button
              @click="handlePlay(item.trackID)"
              icon="CaretRight"
              size="large"
              circle
              type="primary"
            ></el-button>
            <el-divider direction="vertical" />
            <span class="track-name">{{ item.trackName }}</span>
          </div>
        </el-card>
      </div>
      <div id="comment-div">
        <el-input
          v-model="newComment"
          maxlength="30"
          placeholder="Comment here"
          show-word-limit
          id="comment-input"
        >
          <template #append>
            <el-button @click="sendComment"
              ><el-icon><Promotion /></el-icon
            ></el-button>
          </template>
        </el-input>
        <el-timeline id="comment-timeline">
          <el-timeline-item
            v-for="(item, index) in album.comments"
            :key="index"
            type="primary"
            hollow="true"
          >
            {{ item.userName }}: {{ item.comment }}
          </el-timeline-item>
          <el-empty
            v-if="album.comments.length == 0"
            description="No Comment"
          />
        </el-timeline>
      </div>
    </el-main>
    <!-- <el-affix offset="20" position="bottom"> -->
    <audio
      controls
      class="audio"
      :src="url"
      @play="recordLastPlay"
      autoplay="true"
    ></audio>
    <!-- </el-affix> -->
    <el-backtop :right="100" :bottom="100" />
  </el-container>
</template>

<script>
import Cookies from "js-cookie";
import { ElMessage } from "element-plus";
import axios from "axios";

export default {
  props: {
    album: Object,
  },
  data() {
    return {
      url: "",
      trackID: "",
      newComment: "",
    };
  },
  methods: {
    async handlePlay(trackID) {
      this.trackID = trackID;
      var csrftoken = Cookies.get("csrftoken");
      let playResult = await axios
        .get("play/?target=" + trackID, {
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
      let statusCode = playResult["status"];
      if (statusCode == "200") {
        this.url = playResult["data"]["url"];
      } else {
        ElMessage.error("Fail to load the track!");
      }
    },
    albumDetailReturn() {
      this.$emit("album-detail-return");
    },
    recordLastPlay() {
      let time = Date.now();
      let trackID = this.trackID;
      var csrftoken = Cookies.get("csrftoken");
      axios
        .post(
          "track-lastplay/",
          {
            id: trackID,
            time: time,
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
    },
    async sendComment() {
      let id = this.album.id;
      let comment = this.newComment;
      var csrftoken = Cookies.get("csrftoken");
      let commentResult = await axios
        .post(
          "comment/",
          {
            id: id,
            comment: comment,
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
      let statusCode = commentResult["status"];
      if (statusCode == "200") {
        ElMessage({
          type: "success",
          message: "Comment sent",
        });
        this.newComment = "";
      } else {
        ElMessage.error("Fail to send the comment!");
      }
    },
  },
};
</script>

<style scoped>
#album-container2 {
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
}
#album-detail-return {
  position: absolute;
  top: 0px;
  left: 0px;
  z-index: 98;
  background-color: hsla(0, 0%, 100%, 0) !important;
  color: white;
  border: 0;
}
#album-detail-header {
  background-color: #4893e0 !important;
  color: white !important;
  /* background-color: hsla(0, 0%, 100%, 0.8) !important; */
  border-radius: 10px;
}
#list-div {
  background-color: hsla(0, 0%, 100%, 0.8) !important;
  border-radius: 10px;
  padding: 15px;
  margin: 0px;
}
.box-card {
  background-color: hsla(0, 0%, 100%, 0.8) !important;
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 5px 8px 0 rgb(0 0 0 / 14%),
    0 1px 14px 0 rgb(0 0 0 / 12%) !important;
  border-radius: 15px;
}
.box-card:hover {
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.5) !important;
}
.card-body {
  text-align: left;
}
.track-name {
  font-size: 22px;
  font-weight: 500;
}
#comment-timeline {
  /* background-color: hsla(0, 0%, 100%, 0.8) !important; */
  border-radius: 10px;
  padding: 15px;
  text-align: left;
  font-size: 18px;
}
#comment-div {
  background-color: hsla(0, 0%, 100%, 0.9) !important;
  border-radius: 10px;
  padding: 15px;
  margin-top: 10px;
}
.audio {
  width: 95%;
  position: absolute;
  bottom: 20px;
  left: 20px;
}
</style>