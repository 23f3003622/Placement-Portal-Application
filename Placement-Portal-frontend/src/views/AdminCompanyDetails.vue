<template>
  <div class="container mt-5">

    <div class="card shadow">

      <div class="card-header bg-primary text-white text-center py-3">
        <h2 class="mb-1">Next Step</h2>
        <p class="mb-0">Company Details</p>
      </div>

      <div class="card-body">

        <button
          class="btn btn-secondary mb-3"
          @click="$router.back()"
        >
          ← Back
        </button>

        <p><strong>Name:</strong> {{ company.company_name }}</p>

        <p><strong>Industry:</strong> {{ company.industry }}</p>

        <p><strong>Website:</strong> {{ company.website }}</p>

        <p><strong>Location:</strong> {{ company.location }}</p>

        <p><strong>HR Name:</strong> {{ company.hr_name }}</p>

        <p><strong>HR Email:</strong> {{ company.hr_email }}</p>

        <p><strong>Description:</strong></p>

        <div class="card bg-light">
          <div class="card-body">
            {{ company.description }}
          </div>
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
      company: {}
    };
  },

  async mounted() {

    const token = localStorage.getItem("token");
    const id = this.$route.params.id;

    const response = await axios.get(
      `http://127.0.0.1:5000/api/admin/company/${id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    this.company = response.data;

  }

}
</script>