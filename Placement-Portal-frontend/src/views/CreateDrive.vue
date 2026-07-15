

<template>
  <div class="container mt-4">

    <div class="card shadow">

      <div class="card-header bg-primary text-white">
        <h4>Create Drive</h4>
      </div>

      <div class="card-body">

        <form @submit.prevent="createDrive">

          <div class="mb-3">
            <label class="form-label">Job Title</label>
            <input
              v-model="drive.title"
              type="text"
              class="form-control"
              placeholder="Software Engineer"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Description</label>
            <textarea
              v-model="drive.description"
              rows="2"
              class="form-control"
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Experience Required</label>
            <textarea
              v-model="drive.experience_required"
              rows="2"
              class="form-control"
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Benefits</label>
            <textarea
              v-model="drive.benefits"
              rows="2"
              class="form-control"
            ></textarea>
          </div>

          <div class="row">

            <div class="col-md-6 mb-3">
              <label class="form-label">Location</label>
              <input
                v-model="drive.location"
                class="form-control"
              >
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Salary (LPA)</label>
              <input
                type="number"
                v-model="drive.salary"
                class="form-control"
              >
            </div>

      

          </div>

          <div class="mb-3">
            <label class="form-label">Skills Required</label>
            <input
              v-model="drive.skills_required"
              class="form-control"
              placeholder="Python, SQL, Flask"
            >
          </div>

          <div class="row">

            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Branch</label>

              <input
                  type="text"
                  class="form-control"
                  v-model="drive.eligibility_branch"
                  placeholder="Enter eligible branch (e.g. CSE, ECE, IT or All)"
              >
          </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Minimum CGPA</label>

              <input
                type="number"
                step="0.1"
                min="0"
                max="10"
                v-model="drive.minimum_cgpa"
                class="form-control"
              >

            </div>

          </div>

          <div class="mb-4">
            <label class="form-label">Application Deadline</label>

            <input
              type="date"
              v-model="drive.application_deadline"
              class="form-control"
            >
          </div>

          <button class="btn btn-success">
            Create Drive
          </button>

          <button
            type="button"
            class="btn btn-secondary ms-2"
            @click="$router.back()"
          >
            Cancel
          </button>

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
      drive: {
        title: "",
        description: "",
        location: "",
        salary: "",
        experience_required: "",
        benefits: "",
        skills_required: "",
        eligibility_branch: "",
        minimum_cgpa: "",
        application_deadline: ""
      }
    };
  },

  methods: {

    async createDrive() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.post(
          "http://127.0.0.1:5000/api/company/jobs",
          this.drive,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert(response.data.message);

        this.$router.push("/company");

      } catch (error) {
    console.log(error.response);

    if (error.response) {
        console.log(error.response.data);
        alert(error.response.data.message);
    } else {
        alert(error.message);
    }

      }

    }

  }

};
</script>