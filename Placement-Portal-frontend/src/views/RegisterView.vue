<template>
  <div class="container mt-5">
    <div class="card shadow mx-auto" style="max-width: 850px;">

      <div class="card-header bg-primary text-white text-center py-4">
        <h2 class="mb-1">Next Step</h2>
        <p class="mb-0">Placement Portal</p>
      </div>

      <div class="card-body p-4">

        <h4 class="text-center text-primary mb-4">
          Create Your Account
        </h4>

        <!-- Role Selection -->
        <div class="mb-4">
          <label class="form-label">Register As</label>

          <select
            class="form-select"
            v-model="role"
          >
            <option value="student">Student</option>
            <option value="company">Company</option>
          </select>
        </div>

        <!-- ================= STUDENT FORM ================= -->

        <div v-if="role === 'student'">

          <h5 class="mb-3 text-primary">Student Details</h5>

          <div class="row">

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Username"
                v-model="student.username"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                type="email"
                placeholder="Email"
                v-model="student.email"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                type="password"
                placeholder="Password"
                v-model="student.password"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Full Name"
                v-model="student.full_name"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Branch"
                v-model="student.branch"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Year"
                v-model="student.year"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                type="number"
                step="0.01"
                placeholder="CGPA"
                v-model="student.cgpa"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Phone"
                v-model="student.phone"
              >
            </div>

            <div class="col-12 mb-3">
              <textarea
                class="form-control"
                rows="3"
                placeholder="Skills"
                v-model="student.skills"
              ></textarea>
            </div>

            <div class="col-12 mb-3">
              <input
                class="form-control"
                placeholder="Resume Link"
                v-model="student.resume"
              >
            </div>

          </div>

        </div>

        <!-- ================= COMPANY FORM ================= -->

        <div v-else>

          <h5 class="mb-3 text-primary">Company Details</h5>

          <div class="row">

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Username"
                v-model="company.username"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                type="email"
                placeholder="Email"
                v-model="company.email"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                type="password"
                placeholder="Password"
                v-model="company.password"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Company Name"
                v-model="company.company_name"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Industry"
                v-model="company.industry"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="Location"
                v-model="company.location"
              >
            </div>

            <div class="col-12 mb-3">
              <input
                class="form-control"
                placeholder="Website"
                v-model="company.website"
              >
            </div>

            <div class="col-12 mb-3">
              <textarea
                class="form-control"
                rows="3"
                placeholder="Company Description"
                v-model="company.description"
              ></textarea>
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                placeholder="HR Name"
                v-model="company.hr_name"
              >
            </div>

            <div class="col-md-6 mb-3">
              <input
                class="form-control"
                type="email"
                placeholder="HR Email"
                v-model="company.hr_email"
              >
            </div>

          </div>

        </div>

        <!-- Register Button -->

        <div class="text-center mt-4">
          <button
            class="btn btn-primary px-5"
            @click="register"
          >
            Register
          </button>
        </div>

        <div class="text-center mt-3">
          <router-link to="/">
            Already have an account? Login
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {

  data() {

    return {

      role: "student",

      student: {

        username: "",
        email: "",
        password: "",
        full_name: "",
        branch: "",
        year: "",
        cgpa: "",
        phone: "",
        skills: "",
        resume: ""

      },

      company: {

        username: "",
        email: "",
        password: "",
        company_name: "",
        industry: "",
        location: "",
        website: "",
        description: "",
        hr_name: "",
        hr_email: ""

      }

    };

  },

  methods: {

    async register() {

      try {

        if (this.role === "student") {

          await axios.post(
            "http://127.0.0.1:5000/api/auth/student/register",
            this.student
          );

        } else {

          await axios.post(
            "http://127.0.0.1:5000/api/auth/company/register",
            this.company
          );

        }

        alert("Registration Successful!");

        this.$router.push("/");

      } catch (error) {

        if (error.response) {
          alert(error.response.data.message);
        } else {
          alert("Unable to connect to the server.");
        }

      }

    }

  }

};
</script>