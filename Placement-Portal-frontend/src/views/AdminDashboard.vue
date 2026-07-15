

<template>
  <div class="container mt-4">

    <div class="card shadow mb-4">
  <div class="card-header bg-primary text-white text-center py-3">
    <h2 class="mb-1">Next Step</h2>
    <p class="mb-0">Admin Dashboard</p>
  </div>
</div>

    <!-- Welcome -->
    <div class="card mb-4">
      <div class="card-body d-flex justify-content-between align-items-center">
        <h5 class="text-primary mb-0">
    Welcome, Admin
</h5>
      </div>
    </div>

    <div class="row mb-4">

    <div class="col-md-3">
        <div class="card shadow text-center">
            <div class="card-body">
                <h6>Total Students</h6>
                <h2>{{ dashboard.total_students }}</h2>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow text-center">
            <div class="card-body">
                <h6>Total Companies</h6>
                <h2>{{ dashboard.total_companies }}</h2>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow text-center">
            <div class="card-body">
                <h6>Total Placement Drives</h6>
                <h2>{{ dashboard.total_jobs }}</h2>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow text-center">
            <div class="card-body">
                <h6>Total Applications</h6>
                <h2>{{ dashboard.total_applications }}</h2>
            </div>
        </div>
    </div>

</div>

    <!-- Registered Companies -->
    <div class="card mb-4">
      <div class="card-header bg-primary text-white">
        Registered Companies
      </div>
      <div class="card-body">

        <div class="input-group">

          <input
            class="form-control"
            placeholder="Search company..."
            v-model="companySearch"
          >

          <button
            class="btn btn-primary"
            @click="searchCompanies"
          >
            Search
          </button>

        </div>

      </div>

      <ul class="list-group list-group-flush">

        <li
          class="list-group-item d-flex justify-content-between align-items-center"
          v-for="company in companies"
          :key="company.id"
        >

          {{ company.company_name }}

          <div>
                <button
                    class="btn btn-info btn-sm me-2"
                    @click="viewCompany(company.id)"
                >
                    View
                </button>

                <button
                    class="btn btn-danger btn-sm"
                    @click="blacklistCompany(company.id)"
                >
                    Blacklist
                </button>
            </div>

        </li>

      </ul>
    </div>

    <!-- Registered Students -->
    <div class="card mb-4">

      <div class="card-header bg-primary text-white">
        Registered Students
      </div>
      <div class="card-body">

        <div class="input-group">

          <input
            class="form-control"
            placeholder="Search student..."
            v-model="studentSearch"
          >

          <button
            class="btn btn-primary"
            @click="searchStudents"
          >
            Search
          </button>

        </div>

      </div>

      <ul class="list-group list-group-flush">

        <li
          class="list-group-item d-flex justify-content-between align-items-center"
          v-for="student in students"
          :key="student.id"
        >

          {{ student.full_name }}

          <div>
            <button
                class="btn btn-info btn-sm me-2"
                @click="viewStudent(student.id)"
            >
                View
            </button>

            <button
                class="btn btn-danger btn-sm"
                @click="blacklistStudent(student.id)"
            >
                Blacklist
            </button>
        </div>

        </li>

      </ul>

    </div>

    <!-- Pending Companies -->
    <div class="card mb-4">

      <div class="card-header bg-primary text-white">
        Company Applications
      </div>

      <ul class="list-group list-group-flush">

        <li
          class="list-group-item d-flex justify-content-between align-items-center"
          v-for="company in pendingCompanies"
          :key="company.id"
        >

          {{ company.company_name }}

          <button
                class="btn btn-success btn-sm"
                @click="approveCompany(company.id)"
            >
                Approve
            </button>

        </li>

      </ul>

    </div>

    <!-- Placement Drives -->
    <div class="card mb-4">

      <div class="card-header bg-primary text-white">
        Ongoing Drives
      </div>

      <table class="table mb-0">

        <thead>

        <tr>
            <th>ID</th>
            <th>Job Title</th>
            <th>Company</th>
            <th>Location</th>
            <th>Deadline</th>
            <th>Actions</th>
        </tr>

        </thead>

        <tbody>

        <tr
          v-for="drive in drives"
          :key="drive.id"
        >

          <td>{{ drive.id }}</td>
          <td>{{ drive.title }}</td>
          <td>{{ drive.company }}</td>
          <td>{{ drive.location }}</td>
          <td>{{ drive.deadline }}</td>

          <td>

            <button
                class="btn btn-danger btn-sm"
                @click="deleteJob(drive.id)"
            >
                Delete
            </button>

          </td>

        </tr>

        </tbody>

      </table>

    </div>

    

  </div>
</template>

<script>
import axios from "axios";
export default {

  data() {

    return {

    companySearch: "",

    studentSearch: "",

    dashboard: {
        total_students: 0,
        total_companies: 0,
        total_jobs: 0,
        total_applications: 0
    },

    companies: [],

    students: [],

    pendingCompanies: [],

    drives: [],

    applications: []

}

  },

  mounted() {

    this.fetchDashboard();

    this.fetchCompanies();

    this.fetchStudents();

    this.fetchPendingCompanies();

    this.fetchJobs();

    this.fetchApplications();

},

  methods: {

    async fetchCompanies() {

        try {

            const token = localStorage.getItem("token");

            const response = await axios.get(
                "http://127.0.0.1:5000/api/admin/companies",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            this.companies = response.data;

        } catch (error) {

            console.log(error);

        }

    },

    async fetchDashboard() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/admin/dashboard",

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.dashboard = response.data;

    }

    catch(error) {

        console.log(error);

    }

},

    async approveCompany(companyId) {

    try {

        const token = localStorage.getItem("token");

        await axios.put(
            `http://127.0.0.1:5000/api/admin/approve-company/${companyId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        alert("Company Approved Successfully!");

        // Refresh both lists
        this.fetchCompanies();
        this.fetchPendingCompanies();

    } catch (error) {

        console.log(error);

    }

},
    
    async fetchStudents() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
            "http://127.0.0.1:5000/api/admin/students",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        this.students = response.data;

    } catch(error) {

        console.log(error);

    }

},
    async fetchPendingCompanies() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
            "http://127.0.0.1:5000/api/admin/pending-companies",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        this.pendingCompanies = response.data;

    } catch(error) {

        console.log(error);

    }

},


    async searchCompanies() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/admin/search-companies",

            {
                params: {
                    q: this.companySearch
                },

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.companies = response.data;

    } catch(error) {

        console.log(error);

    }

},

            

    async blacklistCompany(companyId) {

    try {

        const token = localStorage.getItem("token");

        await axios.put(
            `http://127.0.0.1:5000/api/admin/blacklist-company/${companyId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        alert("Company blacklisted.");

            this.fetchCompanies();
            this.fetchJobs();
            this.fetchDashboard();
            this.fetchPendingCompanies();

    } catch(error) {

        console.log(error);

    }

},

    async blacklistStudent(studentId) {

    try {

        const token = localStorage.getItem("token");

        await axios.put(
            `http://127.0.0.1:5000/api/admin/blacklist-student/${studentId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        alert("Student blacklisted.");

        this.fetchStudents();

    } catch(error) {

        console.log(error);

    }

},

    async searchStudents() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/admin/search-students",

            {
                params: {
                    q: this.studentSearch
                },

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.students = response.data;

    }

    catch(error) {

        console.log(error);

    }

},

    async fetchJobs() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/admin/jobs",

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.drives = response.data;

    }

    catch(error) {

        console.log(error);

    }

},

    async deleteJob(jobId) {

    if (!confirm("Delete this job posting?")) {
        return;
    }

    try {

        const token = localStorage.getItem("token");

        await axios.delete(

            `http://127.0.0.1:5000/api/admin/delete-job/${jobId}`,

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        alert("Job deleted successfully.");

        this.fetchJobs();

    }

    catch(error) {

        console.log(error);

        alert("Unable to delete job.");

    }

},

    async fetchApplications() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/admin/applications",

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.applications = response.data;

    }

    catch(error) {

        console.log(error);

    }

},

viewCompany(id) {
    this.$router.push(`/admin/company/${id}`);
},

viewStudent(id) {
    this.$router.push(`/admin/student/${id}`);
}

    

}

}
</script>