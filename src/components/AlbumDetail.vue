<template>
  <el-container id="album-container">
    <el-header style="text-align: center">
      <h1>{{ this.album.name + "——" + this.album.artist }}</h1>
    </el-header>
    <el-main>
      <div v-for="item in album.tracks" :key="item.trackID">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>{{ item.trackName }}</span>
            </div>
          </template>
          <audio class="audio" :src="url" @play="handlePlay(item.id)" controls>
          </audio>
        </el-card>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import Cookies from "js-cookie";
import { ElMessage} from "element-plus";
import axios from "axios";


export default {
  props: {
    album: Object,
  },
  data() {
    return {
      url: "",
    };
  },
  // watch: {
  //   album: {
  //     handler(newValue) {
  //       if (ifShowAlbumDetail == true) {
  //         this.showCollection();
  //       }
  //     },
  //     immediate: true,
  //   },
  // },
  methods: {
    async handlePlay(id) {
      var csrftoken = Cookies.get("csrftoken");
      let playResult = await axios
        .get("play/?target=" + id, {
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
        this.url = statusCode["data"]["url"];
      } else {
        ElMessage.error("Fail to load the track!");
      }
    }
  }
};
</script>

<style scoped>
#album-container {
  width: 100%;
  height: 100%;
}
</style>