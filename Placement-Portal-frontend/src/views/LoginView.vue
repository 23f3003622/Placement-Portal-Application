<template>
  <div class="container mt-5">
    <div class="card shadow mx-auto" style="max-width: 420px;">

      <div class="card-header bg-primary text-white text-center py-4">
        <h2 class="mb-1">Next Step</h2>
        <p class="mb-0">Placement Portal</p>
      </div>

      <div class="card-body p-4">

        <h5 class="text-center mb-4 text-primary">
          Login to continue
        </h5>

        <form @submit.prevent="login">

          <div class="mb-3">
            <label class="form-label">Username</label>
            <input
              v-model="username"
              type="text"
              class="form-control"
              placeholder="Enter username"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Enter password"
            />
          </div>

          <button class="btn btn-primary w-100">
            Login
          </button>

          <div class="text-center mt-3">
            <router-link to="/register">
              Don't have an account? Register
            </router-link>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },

  methods: {
    async login() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/auth/login",
          {
            username: this.username,
            password: this.password
          }
        );

        const user = response.data.user;

        localStorage.setItem("token", response.data.access_token);

        if (user.role === "admin") {
          this.$router.push("/admin");
        } else if (user.role === "company") {
          this.$router.push("/company");
        } else {
          this.$router.push("/student");
        }

      } catch (err) {
        alert(err.response.data.message);
      }
    }
  }
};
</script>