<template>
  <div class="container mt-4">

    <h2 class="mb-4">Upcoming Drives</h2>

    <div v-if="jobs.length === 0" class="alert alert-info">
      No upcoming drives found.
    </div>

    <div
      v-for="job in jobs"
      :key="job.id"
      class="card shadow-sm mb-4"
    >
      <div class="card-body">

        <h4>{{ job.title }}</h4>

        <p><strong>Location:</strong> {{ job.location }}</p>

        <p><strong>Salary:</strong> {{ job.salary }} LPA</p>

        <p><strong>Deadline:</strong> {{ job.application_deadline }}</p>

        <p><strong>Status:</strong> {{ job.status }}</p>

        <button
          class="btn btn-primary me-2"
          @click="viewApplications(job.id)"
        >
          Applications
        </button>

        <button
          class="btn btn-success me-2"
          @click="viewStatus(job.id)"
        >
          Candidate Status
        </button>

        <button
          class="btn btn-danger"
          @click="completeDrive(job.id)"
        >
          Mark Complete
        </button>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  data() {
    return {
      jobs: []
    };
  },

  async mounted() {
    this.loadJobs();
  },

  methods: {

    async loadJobs() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/api/company/jobs",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.jobs = response.data.filter(
          job => job.status === "Open"
        );

      } catch (error) {

        console.log(error);

        alert("Unable to load drives.");

      }

    },

    viewApplications(jobId) {

      this.$router.push(`/company/jobs/${jobId}/applications`);

    },

    viewStatus(jobId) {

      this.$router.push(`/company/jobs/${jobId}/status`);

    },

    async completeDrive(jobId) {

      if (!confirm("Mark this drive as completed?")) {
        return;
      }

      try {

        const token = localStorage.getItem("token");

        const response = await axios.put(
          `http://127.0.0.1:5000/api/company/jobs/${jobId}/complete`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert(response.data.message);

        this.loadJobs();

      } catch (error) {

        console.log(error);

        alert("Unable to mark drive complete.");

      }

    }

  }

};
</script>