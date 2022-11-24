<template>
  <el-container id="settings-div">
    <!-- <el-scrollbar width="100%"> -->
    <el-tabs
      tab-position="left"
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
            <h2 v-if="isAdmin">Administrator</h2>
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
            <template v-if="!isAdmin">
              <el-timeline
                v-for="(item, index) in notificationList"
                :key="index"
              >
                <el-timeline-item placement="top">
                  <el-descriptions
                    column="3"
                    style="width: 100%; padding: 5px"
                    border
                  >
                    <el-descriptions-item label="Album name">{{
                      item.albumName
                    }}</el-descriptions-item>
                    <el-descriptions-item label="Status"
                      ><el-tag>{{ item.status }}</el-tag>
                    </el-descriptions-item>
                  </el-descriptions>
                </el-timeline-item>
              </el-timeline>
              <el-empty
                v-if="notificationList.length == 0"
                description="No Notification"
              />
            </template>
            <template v-else>
              <el-timeline v-for="(item, index) in userUploadList" :key="index">
                <el-timeline-item placement="top">
                  <el-card>
                    <template #header>
                      <div class="card-header">
                        <span>{{ item.album.name }}</span>
                        <span>{{ item.album.artist }}</span>
                      </div>
                    </template>
                    <el-button
                      size="small"
                      type="success"
                      @click="handleOperation(item.album.id, 1)"
                      >Accept</el-button
                    >
                    <el-button
                      size="small"
                      type="danger"
                      @click="handleOperation(item.album.id, -1)"
                      >Reject</el-button
                    >
                    <el-descriptions
                      column="3"
                      style="width: 100%; padding: 5px"
                      border
                    >
                      <el-descriptions-item label="User name">{{
                        item.userName
                      }}</el-descriptions-item>
                      <el-descriptions-item label="User ID">{{
                        item.userID
                      }}</el-descriptions-item>
                      <el-descriptions-item label="Album ID">{{
                        item.album.id
                      }}</el-descriptions-item>
                    </el-descriptions>
                    <!-- <h4>User name: {{ item.userName }}</h4>
                    <h4>User ID: {{ item.userID }}</h4>
                    <h4>Album ID: {{ item.album.id }}</h4> -->
                    <el-table
                      :data="item.album.tracks"
                      stripe
                      style="width: 100%"
                    >
                      <el-table-column prop="trackName" label="track name" />
                      <el-table-column prop="trackID" label="track ID" />
                    </el-table>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
              <el-empty
                v-if="userUploadList.length == 0"
                description="No Notification"
              />
            </template>
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
      userUploadList: [],
    };
  },
  methods: {
    async handleNotification(name) {
      if (name == "1") {
        var csrftoken = Cookies.get("csrftoken");
        let url = this.isAdmin
          ? "admin/check-upload/"
          : "check-upload-notification/";
        let notificationResult = await axios
          .get(url, {
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
          if (!this.isAdmin) {
            this.notificationList = notificationResult["data"]["notification"];
          } else {
            this.userUploadList = notificationResult["data"]["upload"];
          }
        } else {
          ElMessage.error("Fail to load notifications!");
        }
      }
    },
    async handleOperation(albumID, success) {
      var csrftoken = Cookies.get("csrftoken");
      let acceptResult = await axios
        .post(
          "admin/reply/",
          {
            reply: [
              {
                albumID: albumID,
                success: success,
              },
            ],
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
      let statusCode = acceptResult["status"];
      if (statusCode == "200") {
        ElMessage({
          type: "success",
          message: "Success",
        });
      } else {
        ElMessage.error("Failure!");
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
  /* background-color: hsla(0, 0%, 100%, 1) !important; */
  border-radius: 10px;
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
  border-radius: 10px;
  padding: 10px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
}
.demo-tabs {
  width: calc(100% - 20px);
  height: calc(100% - 20px);
  padding: 10px;
  border-radius: 10px;
  background-color: hsla(0, 0%, 100%, 0.7) !important;
}
</style>