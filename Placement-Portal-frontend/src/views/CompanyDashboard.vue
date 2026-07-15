<template>
    <div class="container mt-4">
        <div class="card shadow mb-4">
            <div class="card-header bg-primary text-white text-center py-3">
                <h2 class="mb-1">Next Step</h2>
                <p class="mb-0">Company Dashboard</p>
            </div>
        </div>

        <<div class="card mb-4">
    <div class="card-body d-flex justify-content-between align-items-center">

        <h5 class="text-primary mb-0">
            Welcome, {{ company.company_name }}
        </h5>

        <button
            class="btn btn-outline-danger"
            @click="logout"
        >
            Logout
        </button>

    </div>
</div>


            <div class="row g-3 mb-4">

    <div class="col-md-3">
        <div class="card shadow text-center h-100">
            <div class="card-body">
                <h3>{{ stats.total_drives }}</h3>
                <p>Total Drives</p>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow text-center h-100">
            <div class="card-body">
                <h3>{{ stats.active_drives }}</h3>
                <p>Active Drives</p>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow text-center h-100">
            <div class="card-body">
                <h3>{{ stats.applications }}</h3>
                <p>Applications</p>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow text-center h-100">
            <div class="card-body">
                <h3>{{ stats.shortlisted }}</h3>
                <p>Shortlisted</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow text-center h-100">
            <div class="card-body">
                <h3>{{ stats.selected }}</h3>
                <p>Selected</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow text-center h-100">
            <div class="card-body">
                <h3>{{ stats.rejected }}</h3>
                <p>Rejected</p>
            </div>
        </div>
    </div>
</div>

            <div class="d-flex justify-content-between align-items-center mt-4">
                
                <h4>Upcoming Drives</h4>

                <div>

                    <router-link
                        to="/company/interviews"
                        class="btn btn-primary me-2"
                    >
                        Interviews
                    </router-link>

                    <router-link
                        to="/company/create-drive"
                        class="btn btn-success"
                    >
                        Create Drive
                    </router-link>

                </div>
            </div>

            <table class="table table-bordered mt-3">
                <thead>
                    <tr>
                        <th>Sr No.</th>
                        <th>Drive Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                    
                <tbody>
                    <tr v-for="(job, index) in upcomingDrives" :key="job.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ job.title }}</td>
                        <td>
                            <button
                                class="btn btn-primary btn-sm me-2"
                                @click="viewApplications(job)"
                            >
                                Applications
                            </button>

                            <button
                                class="btn btn-success btn-sm"
                                @click="markComplete(job.id)"
                            >
                                Mark Complete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <h4 class="mt-5">Closed Drives</h4>

            <table class="table table-bordered mt-3">
                <thead>
                    <tr>
                        <th>Sr No.</th>
                        <th>Drive Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>

               <tbody>

    <tr
        v-for="(job, index) in completedDrives"
        :key="job.id"
    >
        <td>{{ index + 1 }}</td>

        <td>{{ job.title }}</td>

        <td>
            <button
                class="btn btn-primary btn-sm"
                @click="viewApplications(job)"
            >
                Applications
            </button>
        </td>
    </tr>

    <tr v-if="completedDrives.length === 0">
        <td colspan="3" class="text-center text-muted">
            No Closed Drives Available
        </td>
    </tr>

</tbody>
            </table>
        </div>

        
    
</template>

<script>
import axios from "axios";

export default {
    data() {
        
        return {
            company: {},
            jobs: [],
            upcomingDrives: [],
            completedDrives: [],
            stats:{
    total_drives:0,
    active_drives:0,
    closed_drives:0,
    applications:0,
    shortlisted:0,
    rejected:0,
    selected:0,
    waitlisted:0
}
        };
    },

    async mounted() {
    try {
        await this.loadCompany();
        await this.loadJobs();
        await this.loadStats();
    } catch (error) {
        console.error(error);
    }
},

    methods: {

        logout() {

    localStorage.removeItem("token");

    this.$router.push("/");

},

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

        this.jobs = response.data;

        this.upcomingDrives = this.jobs.filter(
            job => job.status === "Open"
        );

        this.completedDrives = this.jobs.filter(
            job => job.status === "Closed"
        );

    }

    catch (error) {

        console.error(error);

        if (error.response && error.response.status === 401) {

            alert("Session expired. Please login again.");

            localStorage.removeItem("token");

            this.$router.push("/login");

        }

    }

},
        async loadStats() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/company/dashboard-stats",

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.stats = response.data;

    }

    catch (error) {

        console.error(error);

        if (error.response && error.response.status === 401) {

            alert("Session expired. Please login again.");

            localStorage.removeItem("token");

            this.$router.push("/login");

        }

    }

},
        async loadCompany() {
                try {
                    const token = localStorage.getItem("token");

                    const response = await axios.get(
                        "http://127.0.0.1:5000/api/company/profile",
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );

                    this.company = response.data;

                } catch (error) {
                    console.error(error);
                }
            },async loadCompany() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/company/profile",

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.company = response.data;

    }

    catch (error) {

        console.error(error);

        if (error.response && error.response.status === 401) {

            alert("Session expired. Please login again.");

            localStorage.removeItem("token");

            this.$router.push("/login");

        }

    }

},


            async markComplete(id) {

    try {

        const token = localStorage.getItem("token");

        await axios.put(

            `http://127.0.0.1:5000/api/company/jobs/${id}/close`,

            {},

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        alert("Drive marked as completed.");

        await this.loadJobs();
        await this.loadStats();

    }

    catch (error) {

        console.error(error);

        if (error.response) {

            alert(error.response.data.message);

        }

        else {

            alert("Unable to complete drive.");

        }

    }

},

        viewApplications(job) {
                this.$router.push(
                    `/company/jobs/${job.id}/applications`
                );
            },

    }
};
</script>