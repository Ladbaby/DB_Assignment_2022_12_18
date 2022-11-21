<template>
  <el-container id="settings-div">
    <!-- <el-scrollbar width="100%"> -->
    <el-tabs
      tab-position="left"
      style="height: 100%; width: 100%"
      class="demo-tabs"
      @tab-change="handleNotification"
    >
      <el-tab-pane>
        <template #label>
          <span class="custom-tabs-label">
            <el-icon><User /></el-icon>
            <span> User</span>
          </span>
        </template>
        <!-- <el-scrollbar> -->
        <el-row :gutter="20">
          <el-col :span="4">
            <el-avatar
              src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
              :size="100"
            />
          </el-col>
          <el-col :span="4">
            <h2>Administrator</h2>
          </el-col>
        </el-row>
        <hr style="width: 95%" />
        <!-- </el-scrollbar> -->
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span class="custom-tabs-label">
            <el-icon><Bell /></el-icon>
            <span> Notification</span>
          </span>
        </template>
        <el-scrollbar>
          <div id="notification-timeline">
            <el-timeline v-for="item in notificationList" :key="item">
              <el-timeline-item placement="top">
                <el-card>
                  <h4>Album name: {{ item.albumName }}</h4>
                  <p>status: {{ item.status }}</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-scrollbar>
      </el-tab-pane>
    </el-tabs>
    <!-- </el-scrollbar> -->
  </el-container>
</template>

<script>
import { ElMessage } from "element-plus";
import axios from "axios";
import Cookies from "js-cookie";

export default {
  name: "NotificationView",
  props: {
    isAdmin: Boolean,
  },
  data() {
    return {
      notificationList: [],
    };
  },
  methods: {
    async handleNotification(name) {
      if (name == "1") {
        var csrftoken = Cookies.get("csrftoken");
        let notificationResult = await axios
          .get("check-upload-notification/", {
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
        let statusCode = notificationResult["status"];
        if (statusCode == "200") {
          this.notificationList = notificationResult["data"]["notification"];
        } else {
          ElMessage.error("Fail to load the albums!");
        }
      }
    },
  },
};
</script>

<style scoped>
#settings-div {
  width: 100%;
  height: 100%;
  display: block !important;
}
#notification-aside {
  border-radius: 10px;
}
#notification-menu {
  border-radius: 10px;
  min-height: 100vh;
}
#notification-main {
  border-radius: 10px;
  background-color: hsla(0, 0%, 100%, 0.9) !important;
  backdrop-filter: blur(5px);
  margin-left: 10px;
}
#notification-timeline {
  background-color: hsla(0, 0%, 100%, 0.9) !important;
  padding: 32px;
}
</style>