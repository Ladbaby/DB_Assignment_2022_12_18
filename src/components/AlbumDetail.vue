<template>
  <el-container id="album-container">
    <el-header style="text-align: center">
      <el-button @click="albumDetailReturn">return</el-button>
      <h1>{{ this.album.name + "——" + this.album.artist }}</h1>
    </el-header>
    <el-main>
      <div v-for="item in album.tracks" :key="item.trackID">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <el-button @click="handlePlay(item.trackID)">Play</el-button>
              <span>{{ item.trackName }}</span>
            </div>
          </template>
        </el-card>
      </div>
      <el-input
        v-model="newComment"
        maxlength="30"
        placeholder="Comment here"
        show-word-limit
      >
        <template #append>
          <el-button @click="sendComment"
            ><el-icon><Promotion /></el-icon
          ></el-button>
        </template>
      </el-input>
      <el-timeline>
        <el-timeline-item
          v-for="(item, index) in album.comments"
          :key="index"
          type="primary"
          hollow="true"
        >
          {{ item.comment }}
        </el-timeline-item>
      </el-timeline>
      <el-backtop :right="100" :bottom="100" />
    </el-main>
    <el-footer>
      <audio class="audio" :src="url" controls @play="recordLastPlay"></audio>
    </el-footer>
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
#album-container {
  width: 100%;
  height: 100%;
}
</style>